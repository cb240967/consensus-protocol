from typing import List

# Access constants from spec pkg reference.
import eth2spec.phase0.spec as spec
from eth2spec.phase0.spec import (
    Attestation,
    AttestationData,
    AttestationDataAndCustodyBit,
    get_epoch_start_slot, get_block_root, get_current_epoch, get_previous_epoch, slot_to_epoch, get_shard_delta,
    get_crosslink_committee, get_domain, IndexedAttestation, get_attesting_indices, BeaconState, get_block_root_at_slot)
from eth2spec.phase0.state_transition import (
    state_transition, state_transition_to
)
from eth2spec.test.helpers.bitfields import set_bitfield_bit
from eth2spec.test.helpers.block import build_empty_block_for_next_slot, make_block_signature
from eth2spec.test.helpers.keys import privkeys
from eth2spec.utils.bls import bls_sign, bls_aggregate_signatures


def build_attestation_data(state, slot, shard):
    assert state.slot >= slot

    if slot == state.slot:
        block_root = build_empty_block_for_next_slot(state).previous_block_root
    else:
        block_root = get_block_root_at_slot(state, slot)

    current_epoch_start_slot = get_epoch_start_slot(get_current_epoch(state))
    if slot < current_epoch_start_slot:
        epoch_boundary_root = get_block_root(state, get_previous_epoch(state))
    elif slot == current_epoch_start_slot:
        epoch_boundary_root = block_root
    else:
        epoch_boundary_root = get_block_root(state, get_current_epoch(state))

    if slot < current_epoch_start_slot:
        justified_epoch = state.previous_justified_epoch
        justified_block_root = state.previous_justified_root
    else:
        justified_epoch = state.current_justified_epoch
        justified_block_root = state.current_justified_root

    crosslinks = state.current_crosslinks if slot_to_epoch(slot) == get_current_epoch(
        state) else state.previous_crosslinks
    return AttestationData(
        shard=shard,
        beacon_block_root=block_root,
        source_epoch=justified_epoch,
        source_root=justified_block_root,
        target_epoch=slot_to_epoch(slot),
        target_root=epoch_boundary_root,
        crosslink_data_root=spec.ZERO_HASH,
        previous_crosslink_root=hash_tree_root(crosslinks[shard]),
    )


def get_valid_attestation(state, slot=None):
    if slot is None:
        slot = state.slot

    if slot_to_epoch(slot) == get_current_epoch(state):
        shard = (state.latest_start_shard + slot) % spec.SLOTS_PER_EPOCH
    else:
        previous_shard_delta = get_shard_delta(state, get_previous_epoch(state))
        shard = (state.latest_start_shard - previous_shard_delta + slot) % spec.SHARD_COUNT

    attestation_data = build_attestation_data(state, slot, shard)

    crosslink_committee = get_crosslink_committee(state, attestation_data.target_epoch, attestation_data.shard)

    committee_size = len(crosslink_committee)
    bitfield_length = (committee_size + 7) // 8
    aggregation_bitfield = b'\xC0' + b'\x00' * (bitfield_length - 1)
    custody_bitfield = b'\x00' * bitfield_length
    attestation = Attestation(
        aggregation_bitfield=aggregation_bitfield,
        data=attestation_data,
        custody_bitfield=custody_bitfield,
    )
    make_attestation_signature(state, attestation)
    return attestation


def make_aggregate_attestation_signature(state: BeaconState, data: AttestationData, participants: List[int]):
    signatures = []
    for validator_index in participants:
        privkey = privkeys[validator_index]
        signatures.append(
            get_attestation_signature(
                state,
                data,
                privkey
            )
        )

    return bls_aggregate_signatures(signatures)


def make_indexed_attestation_signature(state, indexed_attestation: IndexedAttestation):
    participants = indexed_attestation.custody_bit_0_indices + indexed_attestation.custody_bit_1_indices
    indexed_attestation.signature = make_aggregate_attestation_signature(state, indexed_attestation.data, participants)


def make_attestation_signature(state, attestation: Attestation):
    participants = get_attesting_indices(
        state,
        attestation.data,
        attestation.aggregation_bitfield,
    )

    attestation.signature = make_aggregate_attestation_signature(state, attestation.data, participants)


def get_attestation_signature(state, attestation_data, privkey, custody_bit=0b0):
    message_hash = AttestationDataAndCustodyBit(
        data=attestation_data,
        custody_bit=custody_bit,
    ).hash_tree_root()

    return bls_sign(
        message_hash=message_hash,
        privkey=privkey,
        domain=get_domain(
            state=state,
            domain_type=spec.DOMAIN_ATTESTATION,
            message_epoch=attestation_data.target_epoch,
        )
    )


def fill_aggregate_attestation(state, attestation):
    crosslink_committee = get_crosslink_committee(state, attestation.data.target_epoch, attestation.data.shard)
    for i in range(len(crosslink_committee)):
        attestation.aggregation_bitfield = set_bitfield_bit(attestation.aggregation_bitfield, i)


def add_attestation_to_state(state, attestation, slot):
    block = build_empty_block_for_next_slot(state)
    block.slot = slot
    block.body.attestations.append(attestation)
    state_transition_to(state, block.slot)
    make_block_signature(state, block)
    state_transition(state, block)
