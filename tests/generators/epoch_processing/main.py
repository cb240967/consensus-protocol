from eth2spec.gen_helpers.gen_from_tests.gen import run_state_test_generators, combine_mods
from eth2spec.test.helpers.constants import PHASE0, ALTAIR, BELLATRIX, CAPELLA, EIP4844


if __name__ == "__main__":
    phase_0_mods = {key: 'eth2spec.test.phase0.epoch_processing.test_process_' + key for key in [
        'justification_and_finalization',
        'rewards_and_penalties',
        'registry_updates',
        'slashings',
        'eth1_data_reset',
        'effective_balance_updates',
        'slashings_reset',
        'randao_mixes_reset',
        'historical_roots_update',
        'participation_record_updates',
    ]}

    _new_altair_mods = {key: 'eth2spec.test.altair.epoch_processing.test_process_' + key for key in [
        'inactivity_updates',
        'participation_flag_updates',
        'sync_committee_updates',
    ]}
    altair_mods = combine_mods(_new_altair_mods, phase_0_mods)

    # No epoch-processing changes in Bellatrix and previous testing repeats with new types,
    # so no additional tests required.
    bellatrix_mods = altair_mods

    _new_capella_mods = {key: 'eth2spec.test.capella.epoch_processing.test_process_' + key for key in [
        'historical_batches_update',
    ]}
    capella_mods = combine_mods(_new_capella_mods, bellatrix_mods)

    _new_eip4844_mods = {key: 'eth2spec.test.eip4844.epoch_processing.test_process_' + key for key in [
        'historical_batches_update',
    ]}
    eip4844_mods = combine_mods(_new_eip4844_mods, capella_mods)

    # TODO Custody Game testgen is disabled for now
    # custody_game_mods = {**{key: 'eth2spec.test.custody_game.epoch_processing.test_process_' + key for key in [
    #     'reveal_deadlines',
    #     'challenge_deadlines',
    #     'custody_final_updates',
    # ]}, **phase_0_mods}  # also run the previous phase 0 tests (but against custody game spec)

    all_mods = {
        PHASE0: phase_0_mods,
        ALTAIR: altair_mods,
        BELLATRIX: bellatrix_mods,
        CAPELLA: capella_mods,
        EIP4844: eip4844_mods,
    }

    run_state_test_generators(runner_name="epoch_processing", all_mods=all_mods)
