"""
This module is generated from the ``random`` test generator.
Please do not edit this file manually.
See the README for that generator for more information.
"""

from eth2spec.test.helpers.constants import ALTAIR
from eth2spec.test.context import (
    misc_balances_in_default_range_with_many_validators,
    with_phases,
    zero_activation_threshold,
)
from eth2spec.test.context import (
    always_bls,
    spec_test,
    with_custom_state,
    single_phase,
)
from eth2spec.test.utils.random import (
    run_generated_randomized_test,
)


@with_phases([ALTAIR])
@with_custom_state(
    balances_fn=misc_balances_in_default_range_with_many_validators,
    threshold_fn=zero_activation_threshold
)
@spec_test
@single_phase
@always_bls
def test_randomized_0(spec, state):
    # scenario as high-level, informal text:
    # epochs:0,slots:0,with-block:no_block
    # epochs:0,slots:0,with-block:no_block
    # epochs:0,slots:last_slot_in_epoch,with-block:no_block
    # epochs:0,slots:0,with-block:random_block_altair
    # epochs:0,slots:0,with-block:no_block
    # epochs:0,slots:last_slot_in_epoch,with-block:no_block
    # epochs:0,slots:0,with-block:random_block_altair
    scenario = {'transitions': [{'validation': '_validate_is_not_leaking', 'epochs_to_skip': 0, 'slots_to_skip': 0, 'block_producer': 'no_block'}, {'epochs_to_skip': 0, 'slots_to_skip': 0, 'block_producer': 'no_block', 'validation': 'no_op_validation'}, {'slots_to_skip': 'last_slot_in_epoch', 'epochs_to_skip': 0, 'block_producer': 'no_block', 'validation': 'no_op_validation'}, {'block_producer': 'random_block_altair', 'epochs_to_skip': 0, 'slots_to_skip': 0, 'validation': 'no_op_validation'}, {'epochs_to_skip': 0, 'slots_to_skip': 0, 'block_producer': 'no_block', 'validation': 'no_op_validation'}, {'slots_to_skip': 'last_slot_in_epoch', 'epochs_to_skip': 0, 'block_producer': 'no_block', 'validation': 'no_op_validation'}, {'block_producer': 'random_block_altair', 'epochs_to_skip': 0, 'slots_to_skip': 0, 'validation': 'no_op_validation'}], 'state_randomizer': 'randomize_state_altair'}
    yield from run_generated_randomized_test(
        spec,
        state,
        scenario,
    )


@with_phases([ALTAIR])
@with_custom_state(
    balances_fn=misc_balances_in_default_range_with_many_validators,
    threshold_fn=zero_activation_threshold
)
@spec_test
@single_phase
@always_bls
def test_randomized_1(spec, state):
    # scenario as high-level, informal text:
    # epochs:0,slots:0,with-block:no_block
    # epochs:0,slots:0,with-block:no_block
    # epochs:0,slots:0,with-block:no_block
    # epochs:0,slots:0,with-block:random_block_altair
    # epochs:0,slots:0,with-block:no_block
    # epochs:0,slots:0,with-block:no_block
    # epochs:0,slots:0,with-block:random_block_altair
    scenario = {'transitions': [{'validation': '_validate_is_not_leaking', 'epochs_to_skip': 0, 'slots_to_skip': 0, 'block_producer': 'no_block'}, {'epochs_to_skip': 0, 'slots_to_skip': 0, 'block_producer': 'no_block', 'validation': 'no_op_validation'}, {'slots_to_skip': 0, 'epochs_to_skip': 0, 'block_producer': 'no_block', 'validation': 'no_op_validation'}, {'block_producer': 'random_block_altair', 'epochs_to_skip': 0, 'slots_to_skip': 0, 'validation': 'no_op_validation'}, {'epochs_to_skip': 0, 'slots_to_skip': 0, 'block_producer': 'no_block', 'validation': 'no_op_validation'}, {'slots_to_skip': 0, 'epochs_to_skip': 0, 'block_producer': 'no_block', 'validation': 'no_op_validation'}, {'block_producer': 'random_block_altair', 'epochs_to_skip': 0, 'slots_to_skip': 0, 'validation': 'no_op_validation'}], 'state_randomizer': 'randomize_state_altair'}
    yield from run_generated_randomized_test(
        spec,
        state,
        scenario,
    )


@with_phases([ALTAIR])
@with_custom_state(
    balances_fn=misc_balances_in_default_range_with_many_validators,
    threshold_fn=zero_activation_threshold
)
@spec_test
@single_phase
@always_bls
def test_randomized_2(spec, state):
    # scenario as high-level, informal text:
    # epochs:0,slots:0,with-block:no_block
    # epochs:0,slots:0,with-block:no_block
    # epochs:0,slots:random_slot_in_epoch,with-block:no_block
    # epochs:0,slots:0,with-block:random_block_altair
    # epochs:0,slots:0,with-block:no_block
    # epochs:0,slots:random_slot_in_epoch,with-block:no_block
    # epochs:0,slots:0,with-block:random_block_altair
    scenario = {'transitions': [{'validation': '_validate_is_not_leaking', 'epochs_to_skip': 0, 'slots_to_skip': 0, 'block_producer': 'no_block'}, {'epochs_to_skip': 0, 'slots_to_skip': 0, 'block_producer': 'no_block', 'validation': 'no_op_validation'}, {'slots_to_skip': 'random_slot_in_epoch', 'epochs_to_skip': 0, 'block_producer': 'no_block', 'validation': 'no_op_validation'}, {'block_producer': 'random_block_altair', 'epochs_to_skip': 0, 'slots_to_skip': 0, 'validation': 'no_op_validation'}, {'epochs_to_skip': 0, 'slots_to_skip': 0, 'block_producer': 'no_block', 'validation': 'no_op_validation'}, {'slots_to_skip': 'random_slot_in_epoch', 'epochs_to_skip': 0, 'block_producer': 'no_block', 'validation': 'no_op_validation'}, {'block_producer': 'random_block_altair', 'epochs_to_skip': 0, 'slots_to_skip': 0, 'validation': 'no_op_validation'}], 'state_randomizer': 'randomize_state_altair'}
    yield from run_generated_randomized_test(
        spec,
        state,
        scenario,
    )


@with_phases([ALTAIR])
@with_custom_state(
    balances_fn=misc_balances_in_default_range_with_many_validators,
    threshold_fn=zero_activation_threshold
)
@spec_test
@single_phase
@always_bls
def test_randomized_3(spec, state):
    # scenario as high-level, informal text:
    # epochs:0,slots:0,with-block:no_block
    # epochs:0,slots:0,with-block:no_block
    # epochs:0,slots:penultimate_slot_in_epoch,with-block:no_block
    # epochs:0,slots:0,with-block:random_block_altair
    # epochs:0,slots:0,with-block:no_block
    # epochs:0,slots:penultimate_slot_in_epoch,with-block:no_block
    # epochs:0,slots:0,with-block:random_block_altair
    scenario = {'transitions': [{'validation': '_validate_is_not_leaking', 'epochs_to_skip': 0, 'slots_to_skip': 0, 'block_producer': 'no_block'}, {'epochs_to_skip': 0, 'slots_to_skip': 0, 'block_producer': 'no_block', 'validation': 'no_op_validation'}, {'slots_to_skip': 'penultimate_slot_in_epoch', 'epochs_to_skip': 0, 'block_producer': 'no_block', 'validation': 'no_op_validation'}, {'block_producer': 'random_block_altair', 'epochs_to_skip': 0, 'slots_to_skip': 0, 'validation': 'no_op_validation'}, {'epochs_to_skip': 0, 'slots_to_skip': 0, 'block_producer': 'no_block', 'validation': 'no_op_validation'}, {'slots_to_skip': 'penultimate_slot_in_epoch', 'epochs_to_skip': 0, 'block_producer': 'no_block', 'validation': 'no_op_validation'}, {'block_producer': 'random_block_altair', 'epochs_to_skip': 0, 'slots_to_skip': 0, 'validation': 'no_op_validation'}], 'state_randomizer': 'randomize_state_altair'}
    yield from run_generated_randomized_test(
        spec,
        state,
        scenario,
    )


@with_phases([ALTAIR])
@with_custom_state(
    balances_fn=misc_balances_in_default_range_with_many_validators,
    threshold_fn=zero_activation_threshold
)
@spec_test
@single_phase
@always_bls
def test_randomized_4(spec, state):
    # scenario as high-level, informal text:
    # epochs:0,slots:0,with-block:no_block
    # epochs:1,slots:0,with-block:no_block
    # epochs:0,slots:last_slot_in_epoch,with-block:no_block
    # epochs:0,slots:0,with-block:random_block_altair
    # epochs:1,slots:0,with-block:no_block
    # epochs:0,slots:last_slot_in_epoch,with-block:no_block
    # epochs:0,slots:0,with-block:random_block_altair
    scenario = {'transitions': [{'validation': '_validate_is_not_leaking', 'epochs_to_skip': 0, 'slots_to_skip': 0, 'block_producer': 'no_block'}, {'epochs_to_skip': 1, 'slots_to_skip': 0, 'block_producer': 'no_block', 'validation': 'no_op_validation'}, {'slots_to_skip': 'last_slot_in_epoch', 'epochs_to_skip': 0, 'block_producer': 'no_block', 'validation': 'no_op_validation'}, {'block_producer': 'random_block_altair', 'epochs_to_skip': 0, 'slots_to_skip': 0, 'validation': 'no_op_validation'}, {'epochs_to_skip': 1, 'slots_to_skip': 0, 'block_producer': 'no_block', 'validation': 'no_op_validation'}, {'slots_to_skip': 'last_slot_in_epoch', 'epochs_to_skip': 0, 'block_producer': 'no_block', 'validation': 'no_op_validation'}, {'block_producer': 'random_block_altair', 'epochs_to_skip': 0, 'slots_to_skip': 0, 'validation': 'no_op_validation'}], 'state_randomizer': 'randomize_state_altair'}
    yield from run_generated_randomized_test(
        spec,
        state,
        scenario,
    )


@with_phases([ALTAIR])
@with_custom_state(
    balances_fn=misc_balances_in_default_range_with_many_validators,
    threshold_fn=zero_activation_threshold
)
@spec_test
@single_phase
@always_bls
def test_randomized_5(spec, state):
    # scenario as high-level, informal text:
    # epochs:0,slots:0,with-block:no_block
    # epochs:1,slots:0,with-block:no_block
    # epochs:0,slots:0,with-block:no_block
    # epochs:0,slots:0,with-block:random_block_altair
    # epochs:1,slots:0,with-block:no_block
    # epochs:0,slots:0,with-block:no_block
    # epochs:0,slots:0,with-block:random_block_altair
    scenario = {'transitions': [{'validation': '_validate_is_not_leaking', 'epochs_to_skip': 0, 'slots_to_skip': 0, 'block_producer': 'no_block'}, {'epochs_to_skip': 1, 'slots_to_skip': 0, 'block_producer': 'no_block', 'validation': 'no_op_validation'}, {'slots_to_skip': 0, 'epochs_to_skip': 0, 'block_producer': 'no_block', 'validation': 'no_op_validation'}, {'block_producer': 'random_block_altair', 'epochs_to_skip': 0, 'slots_to_skip': 0, 'validation': 'no_op_validation'}, {'epochs_to_skip': 1, 'slots_to_skip': 0, 'block_producer': 'no_block', 'validation': 'no_op_validation'}, {'slots_to_skip': 0, 'epochs_to_skip': 0, 'block_producer': 'no_block', 'validation': 'no_op_validation'}, {'block_producer': 'random_block_altair', 'epochs_to_skip': 0, 'slots_to_skip': 0, 'validation': 'no_op_validation'}], 'state_randomizer': 'randomize_state_altair'}
    yield from run_generated_randomized_test(
        spec,
        state,
        scenario,
    )


@with_phases([ALTAIR])
@with_custom_state(
    balances_fn=misc_balances_in_default_range_with_many_validators,
    threshold_fn=zero_activation_threshold
)
@spec_test
@single_phase
@always_bls
def test_randomized_6(spec, state):
    # scenario as high-level, informal text:
    # epochs:0,slots:0,with-block:no_block
    # epochs:1,slots:0,with-block:no_block
    # epochs:0,slots:random_slot_in_epoch,with-block:no_block
    # epochs:0,slots:0,with-block:random_block_altair
    # epochs:1,slots:0,with-block:no_block
    # epochs:0,slots:random_slot_in_epoch,with-block:no_block
    # epochs:0,slots:0,with-block:random_block_altair
    scenario = {'transitions': [{'validation': '_validate_is_not_leaking', 'epochs_to_skip': 0, 'slots_to_skip': 0, 'block_producer': 'no_block'}, {'epochs_to_skip': 1, 'slots_to_skip': 0, 'block_producer': 'no_block', 'validation': 'no_op_validation'}, {'slots_to_skip': 'random_slot_in_epoch', 'epochs_to_skip': 0, 'block_producer': 'no_block', 'validation': 'no_op_validation'}, {'block_producer': 'random_block_altair', 'epochs_to_skip': 0, 'slots_to_skip': 0, 'validation': 'no_op_validation'}, {'epochs_to_skip': 1, 'slots_to_skip': 0, 'block_producer': 'no_block', 'validation': 'no_op_validation'}, {'slots_to_skip': 'random_slot_in_epoch', 'epochs_to_skip': 0, 'block_producer': 'no_block', 'validation': 'no_op_validation'}, {'block_producer': 'random_block_altair', 'epochs_to_skip': 0, 'slots_to_skip': 0, 'validation': 'no_op_validation'}], 'state_randomizer': 'randomize_state_altair'}
    yield from run_generated_randomized_test(
        spec,
        state,
        scenario,
    )


@with_phases([ALTAIR])
@with_custom_state(
    balances_fn=misc_balances_in_default_range_with_many_validators,
    threshold_fn=zero_activation_threshold
)
@spec_test
@single_phase
@always_bls
def test_randomized_7(spec, state):
    # scenario as high-level, informal text:
    # epochs:0,slots:0,with-block:no_block
    # epochs:1,slots:0,with-block:no_block
    # epochs:0,slots:penultimate_slot_in_epoch,with-block:no_block
    # epochs:0,slots:0,with-block:random_block_altair
    # epochs:1,slots:0,with-block:no_block
    # epochs:0,slots:penultimate_slot_in_epoch,with-block:no_block
    # epochs:0,slots:0,with-block:random_block_altair
    scenario = {'transitions': [{'validation': '_validate_is_not_leaking', 'epochs_to_skip': 0, 'slots_to_skip': 0, 'block_producer': 'no_block'}, {'epochs_to_skip': 1, 'slots_to_skip': 0, 'block_producer': 'no_block', 'validation': 'no_op_validation'}, {'slots_to_skip': 'penultimate_slot_in_epoch', 'epochs_to_skip': 0, 'block_producer': 'no_block', 'validation': 'no_op_validation'}, {'block_producer': 'random_block_altair', 'epochs_to_skip': 0, 'slots_to_skip': 0, 'validation': 'no_op_validation'}, {'epochs_to_skip': 1, 'slots_to_skip': 0, 'block_producer': 'no_block', 'validation': 'no_op_validation'}, {'slots_to_skip': 'penultimate_slot_in_epoch', 'epochs_to_skip': 0, 'block_producer': 'no_block', 'validation': 'no_op_validation'}, {'block_producer': 'random_block_altair', 'epochs_to_skip': 0, 'slots_to_skip': 0, 'validation': 'no_op_validation'}], 'state_randomizer': 'randomize_state_altair'}
    yield from run_generated_randomized_test(
        spec,
        state,
        scenario,
    )


@with_phases([ALTAIR])
@with_custom_state(
    balances_fn=misc_balances_in_default_range_with_many_validators,
    threshold_fn=zero_activation_threshold
)
@spec_test
@single_phase
@always_bls
def test_randomized_8(spec, state):
    # scenario as high-level, informal text:
    # epochs:_epochs_until_leak,slots:0,with-block:no_block
    # epochs:0,slots:0,with-block:no_block
    # epochs:0,slots:last_slot_in_epoch,with-block:no_block
    # epochs:0,slots:0,with-block:random_block_altair
    # epochs:0,slots:0,with-block:no_block
    # epochs:0,slots:last_slot_in_epoch,with-block:no_block
    # epochs:0,slots:0,with-block:random_block_altair
    scenario = {'transitions': [{'epochs_to_skip': '_epochs_until_leak', 'validation': '_validate_is_leaking', 'slots_to_skip': 0, 'block_producer': 'no_block'}, {'epochs_to_skip': 0, 'slots_to_skip': 0, 'block_producer': 'no_block', 'validation': 'no_op_validation'}, {'slots_to_skip': 'last_slot_in_epoch', 'epochs_to_skip': 0, 'block_producer': 'no_block', 'validation': 'no_op_validation'}, {'block_producer': 'random_block_altair', 'epochs_to_skip': 0, 'slots_to_skip': 0, 'validation': 'no_op_validation'}, {'epochs_to_skip': 0, 'slots_to_skip': 0, 'block_producer': 'no_block', 'validation': 'no_op_validation'}, {'slots_to_skip': 'last_slot_in_epoch', 'epochs_to_skip': 0, 'block_producer': 'no_block', 'validation': 'no_op_validation'}, {'block_producer': 'random_block_altair', 'epochs_to_skip': 0, 'slots_to_skip': 0, 'validation': 'no_op_validation'}], 'state_randomizer': 'randomize_state_altair'}
    yield from run_generated_randomized_test(
        spec,
        state,
        scenario,
    )


@with_phases([ALTAIR])
@with_custom_state(
    balances_fn=misc_balances_in_default_range_with_many_validators,
    threshold_fn=zero_activation_threshold
)
@spec_test
@single_phase
@always_bls
def test_randomized_9(spec, state):
    # scenario as high-level, informal text:
    # epochs:_epochs_until_leak,slots:0,with-block:no_block
    # epochs:0,slots:0,with-block:no_block
    # epochs:0,slots:0,with-block:no_block
    # epochs:0,slots:0,with-block:random_block_altair
    # epochs:0,slots:0,with-block:no_block
    # epochs:0,slots:0,with-block:no_block
    # epochs:0,slots:0,with-block:random_block_altair
    scenario = {'transitions': [{'epochs_to_skip': '_epochs_until_leak', 'validation': '_validate_is_leaking', 'slots_to_skip': 0, 'block_producer': 'no_block'}, {'epochs_to_skip': 0, 'slots_to_skip': 0, 'block_producer': 'no_block', 'validation': 'no_op_validation'}, {'slots_to_skip': 0, 'epochs_to_skip': 0, 'block_producer': 'no_block', 'validation': 'no_op_validation'}, {'block_producer': 'random_block_altair', 'epochs_to_skip': 0, 'slots_to_skip': 0, 'validation': 'no_op_validation'}, {'epochs_to_skip': 0, 'slots_to_skip': 0, 'block_producer': 'no_block', 'validation': 'no_op_validation'}, {'slots_to_skip': 0, 'epochs_to_skip': 0, 'block_producer': 'no_block', 'validation': 'no_op_validation'}, {'block_producer': 'random_block_altair', 'epochs_to_skip': 0, 'slots_to_skip': 0, 'validation': 'no_op_validation'}], 'state_randomizer': 'randomize_state_altair'}
    yield from run_generated_randomized_test(
        spec,
        state,
        scenario,
    )


@with_phases([ALTAIR])
@with_custom_state(
    balances_fn=misc_balances_in_default_range_with_many_validators,
    threshold_fn=zero_activation_threshold
)
@spec_test
@single_phase
@always_bls
def test_randomized_10(spec, state):
    # scenario as high-level, informal text:
    # epochs:_epochs_until_leak,slots:0,with-block:no_block
    # epochs:0,slots:0,with-block:no_block
    # epochs:0,slots:random_slot_in_epoch,with-block:no_block
    # epochs:0,slots:0,with-block:random_block_altair
    # epochs:0,slots:0,with-block:no_block
    # epochs:0,slots:random_slot_in_epoch,with-block:no_block
    # epochs:0,slots:0,with-block:random_block_altair
    scenario = {'transitions': [{'epochs_to_skip': '_epochs_until_leak', 'validation': '_validate_is_leaking', 'slots_to_skip': 0, 'block_producer': 'no_block'}, {'epochs_to_skip': 0, 'slots_to_skip': 0, 'block_producer': 'no_block', 'validation': 'no_op_validation'}, {'slots_to_skip': 'random_slot_in_epoch', 'epochs_to_skip': 0, 'block_producer': 'no_block', 'validation': 'no_op_validation'}, {'block_producer': 'random_block_altair', 'epochs_to_skip': 0, 'slots_to_skip': 0, 'validation': 'no_op_validation'}, {'epochs_to_skip': 0, 'slots_to_skip': 0, 'block_producer': 'no_block', 'validation': 'no_op_validation'}, {'slots_to_skip': 'random_slot_in_epoch', 'epochs_to_skip': 0, 'block_producer': 'no_block', 'validation': 'no_op_validation'}, {'block_producer': 'random_block_altair', 'epochs_to_skip': 0, 'slots_to_skip': 0, 'validation': 'no_op_validation'}], 'state_randomizer': 'randomize_state_altair'}
    yield from run_generated_randomized_test(
        spec,
        state,
        scenario,
    )


@with_phases([ALTAIR])
@with_custom_state(
    balances_fn=misc_balances_in_default_range_with_many_validators,
    threshold_fn=zero_activation_threshold
)
@spec_test
@single_phase
@always_bls
def test_randomized_11(spec, state):
    # scenario as high-level, informal text:
    # epochs:_epochs_until_leak,slots:0,with-block:no_block
    # epochs:0,slots:0,with-block:no_block
    # epochs:0,slots:penultimate_slot_in_epoch,with-block:no_block
    # epochs:0,slots:0,with-block:random_block_altair
    # epochs:0,slots:0,with-block:no_block
    # epochs:0,slots:penultimate_slot_in_epoch,with-block:no_block
    # epochs:0,slots:0,with-block:random_block_altair
    scenario = {'transitions': [{'epochs_to_skip': '_epochs_until_leak', 'validation': '_validate_is_leaking', 'slots_to_skip': 0, 'block_producer': 'no_block'}, {'epochs_to_skip': 0, 'slots_to_skip': 0, 'block_producer': 'no_block', 'validation': 'no_op_validation'}, {'slots_to_skip': 'penultimate_slot_in_epoch', 'epochs_to_skip': 0, 'block_producer': 'no_block', 'validation': 'no_op_validation'}, {'block_producer': 'random_block_altair', 'epochs_to_skip': 0, 'slots_to_skip': 0, 'validation': 'no_op_validation'}, {'epochs_to_skip': 0, 'slots_to_skip': 0, 'block_producer': 'no_block', 'validation': 'no_op_validation'}, {'slots_to_skip': 'penultimate_slot_in_epoch', 'epochs_to_skip': 0, 'block_producer': 'no_block', 'validation': 'no_op_validation'}, {'block_producer': 'random_block_altair', 'epochs_to_skip': 0, 'slots_to_skip': 0, 'validation': 'no_op_validation'}], 'state_randomizer': 'randomize_state_altair'}
    yield from run_generated_randomized_test(
        spec,
        state,
        scenario,
    )


@with_phases([ALTAIR])
@with_custom_state(
    balances_fn=misc_balances_in_default_range_with_many_validators,
    threshold_fn=zero_activation_threshold
)
@spec_test
@single_phase
@always_bls
def test_randomized_12(spec, state):
    # scenario as high-level, informal text:
    # epochs:_epochs_until_leak,slots:0,with-block:no_block
    # epochs:1,slots:0,with-block:no_block
    # epochs:0,slots:last_slot_in_epoch,with-block:no_block
    # epochs:0,slots:0,with-block:random_block_altair
    # epochs:1,slots:0,with-block:no_block
    # epochs:0,slots:last_slot_in_epoch,with-block:no_block
    # epochs:0,slots:0,with-block:random_block_altair
    scenario = {'transitions': [{'epochs_to_skip': '_epochs_until_leak', 'validation': '_validate_is_leaking', 'slots_to_skip': 0, 'block_producer': 'no_block'}, {'epochs_to_skip': 1, 'slots_to_skip': 0, 'block_producer': 'no_block', 'validation': 'no_op_validation'}, {'slots_to_skip': 'last_slot_in_epoch', 'epochs_to_skip': 0, 'block_producer': 'no_block', 'validation': 'no_op_validation'}, {'block_producer': 'random_block_altair', 'epochs_to_skip': 0, 'slots_to_skip': 0, 'validation': 'no_op_validation'}, {'epochs_to_skip': 1, 'slots_to_skip': 0, 'block_producer': 'no_block', 'validation': 'no_op_validation'}, {'slots_to_skip': 'last_slot_in_epoch', 'epochs_to_skip': 0, 'block_producer': 'no_block', 'validation': 'no_op_validation'}, {'block_producer': 'random_block_altair', 'epochs_to_skip': 0, 'slots_to_skip': 0, 'validation': 'no_op_validation'}], 'state_randomizer': 'randomize_state_altair'}
    yield from run_generated_randomized_test(
        spec,
        state,
        scenario,
    )


@with_phases([ALTAIR])
@with_custom_state(
    balances_fn=misc_balances_in_default_range_with_many_validators,
    threshold_fn=zero_activation_threshold
)
@spec_test
@single_phase
@always_bls
def test_randomized_13(spec, state):
    # scenario as high-level, informal text:
    # epochs:_epochs_until_leak,slots:0,with-block:no_block
    # epochs:1,slots:0,with-block:no_block
    # epochs:0,slots:0,with-block:no_block
    # epochs:0,slots:0,with-block:random_block_altair
    # epochs:1,slots:0,with-block:no_block
    # epochs:0,slots:0,with-block:no_block
    # epochs:0,slots:0,with-block:random_block_altair
    scenario = {'transitions': [{'epochs_to_skip': '_epochs_until_leak', 'validation': '_validate_is_leaking', 'slots_to_skip': 0, 'block_producer': 'no_block'}, {'epochs_to_skip': 1, 'slots_to_skip': 0, 'block_producer': 'no_block', 'validation': 'no_op_validation'}, {'slots_to_skip': 0, 'epochs_to_skip': 0, 'block_producer': 'no_block', 'validation': 'no_op_validation'}, {'block_producer': 'random_block_altair', 'epochs_to_skip': 0, 'slots_to_skip': 0, 'validation': 'no_op_validation'}, {'epochs_to_skip': 1, 'slots_to_skip': 0, 'block_producer': 'no_block', 'validation': 'no_op_validation'}, {'slots_to_skip': 0, 'epochs_to_skip': 0, 'block_producer': 'no_block', 'validation': 'no_op_validation'}, {'block_producer': 'random_block_altair', 'epochs_to_skip': 0, 'slots_to_skip': 0, 'validation': 'no_op_validation'}], 'state_randomizer': 'randomize_state_altair'}
    yield from run_generated_randomized_test(
        spec,
        state,
        scenario,
    )


@with_phases([ALTAIR])
@with_custom_state(
    balances_fn=misc_balances_in_default_range_with_many_validators,
    threshold_fn=zero_activation_threshold
)
@spec_test
@single_phase
@always_bls
def test_randomized_14(spec, state):
    # scenario as high-level, informal text:
    # epochs:_epochs_until_leak,slots:0,with-block:no_block
    # epochs:1,slots:0,with-block:no_block
    # epochs:0,slots:random_slot_in_epoch,with-block:no_block
    # epochs:0,slots:0,with-block:random_block_altair
    # epochs:1,slots:0,with-block:no_block
    # epochs:0,slots:random_slot_in_epoch,with-block:no_block
    # epochs:0,slots:0,with-block:random_block_altair
    scenario = {'transitions': [{'epochs_to_skip': '_epochs_until_leak', 'validation': '_validate_is_leaking', 'slots_to_skip': 0, 'block_producer': 'no_block'}, {'epochs_to_skip': 1, 'slots_to_skip': 0, 'block_producer': 'no_block', 'validation': 'no_op_validation'}, {'slots_to_skip': 'random_slot_in_epoch', 'epochs_to_skip': 0, 'block_producer': 'no_block', 'validation': 'no_op_validation'}, {'block_producer': 'random_block_altair', 'epochs_to_skip': 0, 'slots_to_skip': 0, 'validation': 'no_op_validation'}, {'epochs_to_skip': 1, 'slots_to_skip': 0, 'block_producer': 'no_block', 'validation': 'no_op_validation'}, {'slots_to_skip': 'random_slot_in_epoch', 'epochs_to_skip': 0, 'block_producer': 'no_block', 'validation': 'no_op_validation'}, {'block_producer': 'random_block_altair', 'epochs_to_skip': 0, 'slots_to_skip': 0, 'validation': 'no_op_validation'}], 'state_randomizer': 'randomize_state_altair'}
    yield from run_generated_randomized_test(
        spec,
        state,
        scenario,
    )


@with_phases([ALTAIR])
@with_custom_state(
    balances_fn=misc_balances_in_default_range_with_many_validators,
    threshold_fn=zero_activation_threshold
)
@spec_test
@single_phase
@always_bls
def test_randomized_15(spec, state):
    # scenario as high-level, informal text:
    # epochs:_epochs_until_leak,slots:0,with-block:no_block
    # epochs:1,slots:0,with-block:no_block
    # epochs:0,slots:penultimate_slot_in_epoch,with-block:no_block
    # epochs:0,slots:0,with-block:random_block_altair
    # epochs:1,slots:0,with-block:no_block
    # epochs:0,slots:penultimate_slot_in_epoch,with-block:no_block
    # epochs:0,slots:0,with-block:random_block_altair
    scenario = {'transitions': [{'epochs_to_skip': '_epochs_until_leak', 'validation': '_validate_is_leaking', 'slots_to_skip': 0, 'block_producer': 'no_block'}, {'epochs_to_skip': 1, 'slots_to_skip': 0, 'block_producer': 'no_block', 'validation': 'no_op_validation'}, {'slots_to_skip': 'penultimate_slot_in_epoch', 'epochs_to_skip': 0, 'block_producer': 'no_block', 'validation': 'no_op_validation'}, {'block_producer': 'random_block_altair', 'epochs_to_skip': 0, 'slots_to_skip': 0, 'validation': 'no_op_validation'}, {'epochs_to_skip': 1, 'slots_to_skip': 0, 'block_producer': 'no_block', 'validation': 'no_op_validation'}, {'slots_to_skip': 'penultimate_slot_in_epoch', 'epochs_to_skip': 0, 'block_producer': 'no_block', 'validation': 'no_op_validation'}, {'block_producer': 'random_block_altair', 'epochs_to_skip': 0, 'slots_to_skip': 0, 'validation': 'no_op_validation'}], 'state_randomizer': 'randomize_state_altair'}
    yield from run_generated_randomized_test(
        spec,
        state,
        scenario,
    )
