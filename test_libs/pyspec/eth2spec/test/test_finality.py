from copy import deepcopy

import eth2spec.phase0.spec as spec
from eth2spec.phase0.spec import (
    get_current_epoch,
    get_epoch_start_slot,
)
from .context import spec_state_test, never_bls
from .helpers.state import next_epoch
from .helpers.block import build_empty_block_for_next_slot, apply_empty_block
from .helpers.attestations import get_valid_attestation


def check_finality(state,
                   prev_state,
                   current_justified_changed,
                   previous_justified_changed,
                   finalized_changed):
    if current_justified_changed:
        assert state.current_justified_epoch > prev_state.current_justified_epoch
        assert state.current_justified_root != prev_state.current_justified_root
    else:
        assert state.current_justified_epoch == prev_state.current_justified_epoch
        assert state.current_justified_root == prev_state.current_justified_root

    if previous_justified_changed:
        assert state.previous_justified_epoch > prev_state.previous_justified_epoch
        assert state.previous_justified_root != prev_state.previous_justified_root
    else:
        assert state.previous_justified_epoch == prev_state.previous_justified_epoch
        assert state.previous_justified_root == prev_state.previous_justified_root

    if finalized_changed:
        assert state.finalized_epoch > prev_state.finalized_epoch
        assert state.finalized_root != prev_state.finalized_root
    else:
        assert state.finalized_epoch == prev_state.finalized_epoch
        assert state.finalized_root == prev_state.finalized_root


def next_epoch_with_attestations(state,
                                 fill_cur_epoch,
                                 fill_prev_epoch):
    post_state = deepcopy(state)
    blocks = []
    for _ in range(spec.SLOTS_PER_EPOCH):
        block = build_empty_block_for_next_slot(post_state)
        if fill_cur_epoch:
            slot_to_attest = post_state.slot - spec.MIN_ATTESTATION_INCLUSION_DELAY + 1
            if slot_to_attest >= get_epoch_start_slot(get_current_epoch(post_state)):
                cur_attestation = get_valid_attestation(post_state, slot_to_attest)
                block.body.attestations.append(cur_attestation)

        if fill_prev_epoch:
            slot_to_attest = post_state.slot - spec.SLOTS_PER_EPOCH + 1
            prev_attestation = get_valid_attestation(post_state, slot_to_attest)
            block.body.attestations.append(prev_attestation)

        spec.state_transition(post_state, block)
        blocks.append(block)

    return state, blocks, post_state


@never_bls
@spec_state_test
def test_finality_rule_4(state):
    yield 'pre', state

    blocks = []
    for epoch in range(4):
        prev_state, new_blocks, state = next_epoch_with_attestations(state, True, False)
        blocks += new_blocks

        # justification/finalization skipped at GENESIS_EPOCH
        if epoch == 0:
            check_finality(state, prev_state, False, False, False)
        # justification/finalization skipped at GENESIS_EPOCH + 1
        elif epoch == 1:
            check_finality(state, prev_state, False, False, False)
        elif epoch == 2:
            check_finality(state, prev_state, True, False, False)
        elif epoch >= 3:
            # rule 4 of finality
            check_finality(state, prev_state, True, True, True)
            assert state.finalized_epoch == prev_state.current_justified_epoch
            assert state.finalized_root == prev_state.current_justified_root

    yield 'blocks', blocks, [spec.BeaconBlock]
    yield 'post', state


@never_bls
@spec_state_test
def test_finality_rule_1(state):
    # get past first two epochs that finality does not run on
    next_epoch(state)
    apply_empty_block(state)
    next_epoch(state)
    apply_empty_block(state)

    yield 'pre', state

    blocks = []
    for epoch in range(3):
        prev_state, new_blocks, state = next_epoch_with_attestations(state, False, True)
        blocks += new_blocks

        if epoch == 0:
            check_finality(state, prev_state, True, False, False)
        elif epoch == 1:
            check_finality(state, prev_state, True, True, False)
        elif epoch == 2:
            # finalized by rule 1
            check_finality(state, prev_state, True, True, True)
            assert state.finalized_epoch == prev_state.previous_justified_epoch
            assert state.finalized_root == prev_state.previous_justified_root

    yield 'blocks', blocks, [spec.BeaconBlock]
    yield 'post', state


@never_bls
@spec_state_test
def test_finality_rule_2(state):
    # get past first two epochs that finality does not run on
    next_epoch(state)
    apply_empty_block(state)
    next_epoch(state)
    apply_empty_block(state)

    yield 'pre', state

    blocks = []
    for epoch in range(3):
        if epoch == 0:
            prev_state, new_blocks, state = next_epoch_with_attestations(state, True, False)
            check_finality(state, prev_state, True, False, False)
        elif epoch == 1:
            prev_state, new_blocks, state = next_epoch_with_attestations(state, False, False)
            check_finality(state, prev_state, False, True, False)
        elif epoch == 2:
            prev_state, new_blocks, state = next_epoch_with_attestations(state, False, True)
            # finalized by rule 2
            check_finality(state, prev_state, True, False, True)
            assert state.finalized_epoch == prev_state.previous_justified_epoch
            assert state.finalized_root == prev_state.previous_justified_root

        blocks += new_blocks

    yield 'blocks', blocks, [spec.BeaconBlock]
    yield 'post', state


@never_bls
@spec_state_test
def test_finality_rule_3(state):
    """
    Test scenario described here
    https://github.com/ethereum/eth2.0-specs/issues/611#issuecomment-463612892
    """
    # get past first two epochs that finality does not run on
    next_epoch(state)
    apply_empty_block(state)
    next_epoch(state)
    apply_empty_block(state)

    yield 'pre', state

    blocks = []
    prev_state, new_blocks, state = next_epoch_with_attestations(state, True, False)
    blocks += new_blocks
    check_finality(state, prev_state, True, False, False)

    # In epoch N, JE is set to N, prev JE is set to N-1
    prev_state, new_blocks, state = next_epoch_with_attestations(state, True, False)
    blocks += new_blocks
    check_finality(state, prev_state, True, True, True)

    # In epoch N+1, JE is N, prev JE is N-1, and not enough messages get in to do anything
    prev_state, new_blocks, state = next_epoch_with_attestations(state, False, False)
    blocks += new_blocks
    check_finality(state, prev_state, False, True, False)

    # In epoch N+2, JE is N, prev JE is N, and enough messages from the previous epoch get in to justify N+1.
    # N+1 now becomes the JE. Not enough messages from epoch N+2 itself get in to justify N+2
    prev_state, new_blocks, state = next_epoch_with_attestations(state, False, True)
    blocks += new_blocks
    # rule 2
    check_finality(state, prev_state, True, False, True)

    # In epoch N+3, LJE is N+1, prev LJE is N, and enough messages get in to justify epochs N+2 and N+3.
    prev_state, new_blocks, state = next_epoch_with_attestations(state, True, True)
    blocks += new_blocks
    # rule 3
    check_finality(state, prev_state, True, True, True)
    assert state.finalized_epoch == prev_state.current_justified_epoch
    assert state.finalized_root == prev_state.current_justified_root

    yield 'blocks', blocks, [spec.BeaconBlock]
    yield 'post', state
