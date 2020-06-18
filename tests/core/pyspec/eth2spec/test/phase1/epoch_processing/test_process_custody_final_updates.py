from eth2spec.test.context import (
    PHASE0,
)
from eth2spec.test.helpers.custody import (
    get_valid_chunk_challenge,
    get_valid_custody_chunk_response,
    get_valid_custody_key_reveal,
    get_sample_shard_transition
)
from eth2spec.test.helpers.attestations import (
    get_valid_on_time_attestation,
)
from eth2spec.test.helpers.state import next_epoch_via_block, transition_to
from eth2spec.test.context import (
    with_all_phases_except,
    spec_state_test,
)
from eth2spec.test.phase0.block_processing.test_process_attestation import run_attestation_processing
from eth2spec.test.phase0.epoch_processing.run_epoch_process_base import run_epoch_processing_with

from eth2spec.test.phase1.block_processing.test_process_chunk_challenge import (
    run_chunk_challenge_processing,
    run_custody_chunk_response_processing,
)
from eth2spec.test.phase1.block_processing.test_process_custody_key_reveal import run_custody_key_reveal_processing


def run_process_custody_final_updates(spec, state):
    yield from run_epoch_processing_with(spec, state, 'process_custody_final_updates')


@with_all_phases_except([PHASE0])
@spec_state_test
def test_validator_withdrawal_delay(spec, state):
    spec.initiate_validator_exit(state, 0)
    assert state.validators[0].withdrawable_epoch < spec.FAR_FUTURE_EPOCH

    yield from run_process_custody_final_updates(spec, state)

    assert state.validators[0].withdrawable_epoch == spec.FAR_FUTURE_EPOCH


@with_all_phases_except([PHASE0])
@spec_state_test
def test_validator_withdrawal_reenable_after_custody_reveal(spec, state):
    spec.initiate_validator_exit(state, 0)
    assert state.validators[0].withdrawable_epoch < spec.FAR_FUTURE_EPOCH

    next_epoch_via_block(spec, state)

    assert state.validators[0].withdrawable_epoch == spec.FAR_FUTURE_EPOCH

    while spec.get_current_epoch(state) < state.validators[0].exit_epoch:
        next_epoch_via_block(spec, state)

    while (state.validators[0].next_custody_secret_to_reveal
           <= spec.get_custody_period_for_validator(0, state.validators[0].exit_epoch - 1)):
        custody_key_reveal = get_valid_custody_key_reveal(spec, state, validator_index=0)
        _, _, _ = run_custody_key_reveal_processing(spec, state, custody_key_reveal)

    yield from run_process_custody_final_updates(spec, state)

    assert state.validators[0].withdrawable_epoch < spec.FAR_FUTURE_EPOCH


@with_all_phases_except([PHASE0])
@spec_state_test
def test_validator_withdrawal_suspend_after_chunk_challenge(spec, state):
    transition_to(spec, state, state.slot + 1)
    shard = 0
    offset_slots = spec.get_offset_slots(state, shard)
    shard_transition = get_sample_shard_transition(spec, state.slot, [2**15 // 3] * len(offset_slots))
    attestation = get_valid_on_time_attestation(spec, state, index=shard, signed=True,
                                                shard_transition=shard_transition)

    transition_to(spec, state, state.slot + spec.MIN_ATTESTATION_INCLUSION_DELAY)

    _, _, _ = run_attestation_processing(spec, state, attestation)

    validator_index = spec.get_beacon_committee(
        state,
        attestation.data.slot,
        attestation.data.index
    )[0]

    spec.initiate_validator_exit(state, validator_index)
    assert state.validators[validator_index].withdrawable_epoch < spec.FAR_FUTURE_EPOCH

    transition_to(spec, state, state.slot + spec.SLOTS_PER_EPOCH)

    assert state.validators[validator_index].withdrawable_epoch == spec.FAR_FUTURE_EPOCH

    while spec.get_current_epoch(state) < state.validators[validator_index].exit_epoch:
        next_epoch_via_block(spec, state)

    while (state.validators[validator_index].next_custody_secret_to_reveal
           <= spec.get_custody_period_for_validator(
               validator_index,
               state.validators[validator_index].exit_epoch - 1)):
        custody_key_reveal = get_valid_custody_key_reveal(spec, state, validator_index=validator_index)
        _, _, _ = run_custody_key_reveal_processing(spec, state, custody_key_reveal)

    next_epoch_via_block(spec, state)

    challenge = get_valid_chunk_challenge(spec, state, attestation, shard_transition)

    _, _, _ = run_chunk_challenge_processing(spec, state, challenge)

    yield from run_process_custody_final_updates(spec, state)

    assert state.validators[validator_index].withdrawable_epoch == spec.FAR_FUTURE_EPOCH


@with_all_phases_except([PHASE0])
@spec_state_test
def test_validator_withdrawal_resume_after_chunk_challenge_response(spec, state):
    transition_to(spec, state, state.slot + 1)
    shard = 0
    offset_slots = spec.get_offset_slots(state, shard)
    shard_transition = get_sample_shard_transition(spec, state.slot, [2**15 // 3] * len(offset_slots))
    attestation = get_valid_on_time_attestation(spec, state, index=shard, signed=True,
                                                shard_transition=shard_transition)

    transition_to(spec, state, state.slot + spec.MIN_ATTESTATION_INCLUSION_DELAY)

    _, _, _ = run_attestation_processing(spec, state, attestation)

    validator_index = spec.get_beacon_committee(
        state,
        attestation.data.slot,
        attestation.data.index
    )[0]

    spec.initiate_validator_exit(state, validator_index)
    assert state.validators[validator_index].withdrawable_epoch < spec.FAR_FUTURE_EPOCH

    next_epoch_via_block(spec, state)

    assert state.validators[validator_index].withdrawable_epoch == spec.FAR_FUTURE_EPOCH

    while spec.get_current_epoch(state) < state.validators[validator_index].exit_epoch:
        next_epoch_via_block(spec, state)

    while (state.validators[validator_index].next_custody_secret_to_reveal
           <= spec.get_custody_period_for_validator(
               validator_index,
               state.validators[validator_index].exit_epoch - 1)):
        custody_key_reveal = get_valid_custody_key_reveal(spec, state, validator_index=validator_index)
        _, _, _ = run_custody_key_reveal_processing(spec, state, custody_key_reveal)

    next_epoch_via_block(spec, state)

    challenge = get_valid_chunk_challenge(spec, state, attestation, shard_transition)

    _, _, _ = run_chunk_challenge_processing(spec, state, challenge)

    next_epoch_via_block(spec, state)

    assert state.validators[validator_index].withdrawable_epoch == spec.FAR_FUTURE_EPOCH

    chunk_challenge_index = state.custody_chunk_challenge_index - 1
    custody_response = get_valid_custody_chunk_response(spec, state, challenge, 2**15 // 3, chunk_challenge_index)

    _, _, _ = run_custody_chunk_response_processing(spec, state, custody_response)

    yield from run_process_custody_final_updates(spec, state)

    assert state.validators[validator_index].withdrawable_epoch < spec.FAR_FUTURE_EPOCH
