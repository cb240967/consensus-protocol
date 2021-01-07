import random
from eth2spec.test.helpers.block import (
    build_empty_block_for_next_slot,
)
from eth2spec.test.helpers.state import (
    state_transition_and_sign_block,
)
from eth2spec.test.lightclient_patch.helpers import (
    compute_aggregate_sync_committee_signature,
)
from eth2spec.test.context import (
    PHASE0, PHASE1,
    expect_assertion_error,
    with_all_phases_except,
    spec_state_test,
)


@with_all_phases_except([PHASE0, PHASE1])
@spec_state_test
def test_invalid_sync_committee_bits(spec, state):
    committee = spec.get_sync_committee_indices(state, spec.get_current_epoch(state))
    random_participant = random.choice(committee)

    yield 'pre', state

    block = build_empty_block_for_next_slot(spec, state)
    # Exclude one participant whose signature was included.
    block.body.sync_committee_bits = [index != random_participant for index in committee]
    block.body.sync_committee_signature = compute_aggregate_sync_committee_signature(
        spec,
        state,
        block.slot - 1,
        committee,  #  full committee signs
    )

    yield 'blocks', [block]
    expect_assertion_error(lambda: spec.process_sync_committee(state, block.body))
    yield 'post', None


@with_all_phases_except([PHASE0, PHASE1])
@spec_state_test
def test_invalid_sync_committee_signature(spec, state):
    committee = spec.get_sync_committee_indices(state, spec.get_current_epoch(state))
    random_participant = random.choice(committee)

    yield 'pre', state

    block = build_empty_block_for_next_slot(spec, state)
    # Exclude one signature even though the block claims the entire committee participated.
    block.body.sync_committee_bits = [True] * len(committee)
    block.body.sync_committee_signature = compute_aggregate_sync_committee_signature(
        spec,
        state,
        block.slot - 1,
        [index for index in committee if index != random_participant],
    )

    yield 'blocks', [block]
    expect_assertion_error(lambda: spec.process_sync_committee(state, block.body))
    yield 'post', None


def compute_sync_committee_participant_reward(spec, state, participant_index, active_validator_count, committee_size):
    base_reward = spec.get_base_reward(state, participant_index)
    proposer_reward = spec.get_proposer_reward(state, participant_index)
    max_participant_reward = base_reward - proposer_reward
    return max_participant_reward * active_validator_count // committee_size // spec.SLOTS_PER_EPOCH


@with_all_phases_except([PHASE0, PHASE1])
@spec_state_test
def test_sync_committee_rewards(spec, state):
    committee = spec.get_sync_committee_indices(state, spec.get_current_epoch(state))
    committee_size = len(committee)
    active_validator_count = len(spec.get_active_validator_indices(state, spec.get_current_epoch(state)))

    yield 'pre', state

    pre_balances = state.balances.copy()

    block = build_empty_block_for_next_slot(spec, state)
    block.body.sync_committee_bits = [True] * committee_size
    block.body.sync_committee_signature = compute_aggregate_sync_committee_signature(
        spec,
        state,
        block.slot - 1,
        committee,
    )

    signed_block = state_transition_and_sign_block(spec, state, block)

    yield 'blocks', [signed_block]
    yield 'post', state

    for index in range(len(state.validators)):
        expected_reward = 0

        if index == block.proposer_index:
            expected_reward += sum([spec.get_proposer_reward(state, index) for index in committee])

        if index in committee:
            expected_reward += compute_sync_committee_participant_reward(
                spec,
                state,
                index,
                active_validator_count,
                committee_size
            )

        assert state.balances[index] == pre_balances[index] + expected_reward
