import itertools
from random import Random
from typing import Callable
from tests.core.pyspec.eth2spec.test.context import misc_balances_in_default_range, zero_activation_threshold
from eth2spec.test.helpers.multi_operations import (
    build_random_block_from_state,
)
from eth2spec.test.helpers.state import (
    next_epoch,
    next_slot,
    ensure_state_has_validators_across_lifecycle,
    state_transition_and_sign_block,
)
from eth2spec.test.helpers.random import (
    randomize_state,
)
from eth2spec.test.context import (
    with_all_phases,
    always_bls,
    spec_test,
    with_custom_state,
    default_activation_threshold,
    single_phase,
    misc_balances,
)

# May need to make several attempts to find a block that does not correspond to a slashed
# proposer with the randomization helpers...
BLOCK_ATTEMPTS = 32

# primitives
## state

def _randomize_state(spec, state):
    return randomize_state(spec, state, exit_fraction=0.1, slash_fraction=0.1)


## epochs

def _epochs_until_leak(spec):
    return spec.MIN_EPOCHS_TO_INACTIVITY_PENALTY


def _epochs_for_shard_committee_period(spec):
    return spec.config.SHARD_COMMITTEE_PERIOD


## slots

def _last_slot_in_epoch(spec):
    return spec.SLOTS_PER_EPOCH - 1


def _random_slot_in_epoch(rng):
    def f(spec):
        return rng.randrange(1, spec.SLOTS_PER_EPOCH - 2)
    return f


def _penultimate_slot_in_epoch(spec):
    return spec.SLOTS_PER_EPOCH - 2


## blocks

def _no_block(_spec, _pre_state, _signed_blocks):
    return None


def _random_block(spec, state, _signed_blocks):
    """
    Produce a random block.
    NOTE: this helper may mutate state, as it will attempt
    to produce a block over ``BLOCK_ATTEMPTS`` slots in order
    to find a valid block in the event that the proposer has already been slashed.
    """
    block = build_random_block_from_state(spec, state)
    for _ in range(BLOCK_ATTEMPTS):
        proposer = state.validators[block.proposer_index]
        if proposer.slashed:
            next_slot(spec, state)
            block = build_random_block_from_state(spec, state)
        else:
            return block
    else:
        raise AssertionError("could not find a block with an unslashed proposer, check ``state`` input")


## validations

def _no_op_validation(spec, state):
    return True


def _validate_is_leaking(spec, state):
    return spec.is_in_inactivity_leak(state)


# transitions

def _no_op_transition():
    return {}


def _epoch_transition(n=0):
    return {
        "epochs_to_skip": n,
    }


def _slot_transition(n=0):
    return {
        "slots_to_skip": n,
    }


def _transition_to_leaking():
    return {
        "epochs_to_skip": _epochs_until_leak,
        "validation": _validate_is_leaking,
    }


## block transitions

def _transition_with_random_block(epochs=None, slots=None):
    """
    Build a block transition with randomized data.
    Provide optional sub-transitions to advance some
    number of epochs or slots before applying the random block.
    """
    transition = {
        "block_producer": _random_block,
    }
    if epochs:
        transition.update(epochs)
    if slots:
        transition.update(slots)
    return transition


# setup and test gen

def _randomized_scenario_setup():
    """
    Return a sequence of pairs of ("mutator", "validator"),
    a function that accepts (spec, state) arguments and performs some change
    and a function that accepts (spec, state) arguments and validates some change was made.
    """
    def _skip_epochs(epoch_producer):
        def f(spec, state):
            """
            The unoptimized spec implementation is too slow to advance via ``next_epoch``.
            Instead, just overwrite the ``state.slot`` and continue...
            """
            epochs_to_skip = epoch_producer(spec)
            slots_to_skip = epochs_to_skip * spec.SLOTS_PER_EPOCH
            state.slot += slots_to_skip
        return f

    return (
        # NOTE: the block randomization function assumes at least 1 shard committee period
        # so advance the state before doing anything else.
        (_skip_epochs(_epochs_for_shard_committee_period), _no_op_validation),
        (_randomize_state, ensure_state_has_validators_across_lifecycle),
    )


def _normalize_transition(transition):
    """
    Provide "empty" or "no op" sub-transitions
    to a given transition.
    """
    if isinstance(transition, Callable):
        transition = transition()
    if "epochs_to_skip" not in transition:
        transition["epochs_to_skip"] = 0
    if "slots_to_skip" not in transition:
        transition["slots_to_skip"] = 0
    if "block_producer" not in transition:
        transition["block_producer"] = _no_block
    if "validation" not in transition:
        transition["validation"] = _no_op_validation
    return transition


def _normalize_scenarios(scenarios):
    """
    "Normalize" a "scenario" so that a producer of a test case
    does not need to provide every expected key/value.
    """
    for scenario in scenarios:
        if "setup" not in scenario:
            scenario["setup"] = _randomized_scenario_setup()

        transitions = scenario["transitions"]
        for i, transition in enumerate(transitions):
            transitions[i] = _normalize_transition(transition)


def _generate_randomized_scenarios():
    """
    Generates a set of randomized testing scenarios.
    Return a sequence of "scenarios" where each scenario:
    1. Provides some setup
    2. Provides a sequence of transitions that mutate the state in some way,
        possibly yielding blocks along the way
    NOTE: scenarios are "normalized" with empty/no-op elements before returning
    to the test generation to facilitate brevity when writing scenarios by hand.
    NOTE: the main block driver builds a block for the **next** slot, so
    the slot transitions are offset by -1 to target certain boundaries.
    """
    rng = Random(1336)

    # go forward 0 or 1 epochs
    epochs_set = (_epoch_transition(n=0), _epoch_transition(n=1))
    # within those epochs, go forward to:
    slots_set = (
        # the first slot in an epoch (see note in docstring about offsets...)
        _slot_transition(_last_slot_in_epoch),
        # the second slot in an epoch
        _slot_transition(n=0),
        # some random number of slots, but not at epoch boundaries
        _slot_transition(_random_slot_in_epoch(rng)),
        # the last slot in an epoch (see note in docstring about offsets...)
        _slot_transition(_penultimate_slot_in_epoch),
    )
    # build a set of block transitions from combinations of sub-transitions
    block_transitions = list(
        _transition_with_random_block(epochs=epochs, slots=slots)
        for epochs, slots in itertools.product(epochs_set, slots_set)
    )

    # and preface each block transition with the possible leak transitions
    # (... either no leak or transition to a leak before applying the block transition)
    leak_transitions = (_no_op_transition, _transition_to_leaking)
    scenarios = [
        {"transitions": list(t)}
        for t in itertools.product(leak_transitions, block_transitions)
    ]
    _normalize_scenarios(scenarios)
    return scenarios


def _id_from_scenario(test_description):
    """
    Construct a test name for ``pytest`` infra.
    """
    def _to_id_part(prefix, x):
        suffix = str(x)
        if isinstance(x, Callable):
            suffix = x.__name__
        return f"{prefix}{suffix}"

    def _id_from_transition(transition):
        return ",".join((
            _to_id_part("epochs:", transition["epochs_to_skip"]),
            _to_id_part("slots:", transition["slots_to_skip"]),
            _to_id_part("with-block:", transition["block_producer"])
        ))

    return "|".join(map(_id_from_transition, test_description["transitions"]))


def pytest_generate_tests(metafunc):
    """
    Pytest hook to generate test cases from dynamically computed data
    """
    generated_name = "test_description"
    generated_values = _generate_randomized_scenarios()
    metafunc.parametrize(generated_name, generated_values, ids=_id_from_scenario, scope="module")


def pytest_generate_tests_adapter(f):
    """
    Adapter decorator to allow dynamic test case generation
    while leveraging existing decorators specific to spec tests.
    """
    def wrapper(test_description, *args, **kwargs):
        kwargs["test_description"] = test_description
        f(*args, **kwargs)
    return wrapper


def _iter_temporal(spec, callable_or_int):
    """
    Intended to advance some number of {epochs, slots}.
    Caller can provide a constant integer or a callable deriving a number from
    the ``spec`` under consideration.
    """
    numeric = callable_or_int
    if isinstance(callable_or_int, Callable):
        numeric = callable_or_int(spec)
    for i in range(numeric):
        yield i


@pytest_generate_tests_adapter
@with_all_phases
@with_custom_state(balances_fn=misc_balances_in_default_range, threshold_fn=zero_activation_threshold)
@spec_test
@single_phase
@always_bls
def test_harness_for_randomized_blocks(spec, state, test_description):
    for mutation, validation in test_description["setup"]:
        mutation(spec, state)
        validation(spec, state)

    yield "pre", state

    blocks = []
    for transition in test_description["transitions"]:
        epochs_to_skip = _iter_temporal(spec, transition["epochs_to_skip"])
        for _ in epochs_to_skip:
            next_epoch(spec, state)
        slots_to_skip = _iter_temporal(spec, transition["slots_to_skip"])
        for _ in slots_to_skip:
            next_slot(spec, state)

        block = transition["block_producer"](spec, state, blocks)
        if block:
            signed_block = state_transition_and_sign_block(spec, state, block)
            blocks.append(signed_block)

        assert transition["validation"](spec, state)

    yield "blocks", blocks
    yield "post", state
