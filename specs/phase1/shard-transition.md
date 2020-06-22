# Ethereum 2.0 Phase 1 -- Shard Transition and Fraud Proofs

**Notice**: This document is a work-in-progress for researchers and implementers.

## Table of contents

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [Introduction](#introduction)
- [Helper functions](#helper-functions)
  - [Shard block verification functions](#shard-block-verification-functions)
- [Shard state transition](#shard-state-transition)
- [Fraud proofs](#fraud-proofs)
  - [Verifying the proof](#verifying-the-proof)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Introduction

This document describes the shard transition function and fraud proofs as part of Phase 1 of Ethereum 2.0.

## Helper functions

### Shard block verification functions

```python
def verify_shard_block_message(beacon_parent_state: BeaconState,
                               shard_parent_state: ShardState,
                               block: ShardBlock) -> bool:
    # Check `shard_parent_root` field
    assert block.shard_parent_root == shard_parent_state.latest_block_root
    # Check `beacon_parent_root` field
    beacon_parent_block_header = beacon_parent_state.latest_block_header.copy()
    if beacon_parent_block_header.state_root == Root():
        beacon_parent_block_header.state_root = hash_tree_root(beacon_parent_state)
    beacon_parent_root = hash_tree_root(beacon_parent_block_header)
    assert block.beacon_parent_root == beacon_parent_root
    # Check `slot` field
    shard = block.shard
    next_slot = Slot(block.slot + 1)
    offset_slots = compute_offset_slots(get_latest_slot_for_shard(beacon_parent_state, shard), next_slot)
    assert block.slot in offset_slots
    # Check `proposer_index` field
    assert block.proposer_index == get_shard_proposer_index(beacon_parent_state, block.slot, shard)
    # Check `body` field
    assert 0 < len(block.body) <= MAX_SHARD_BLOCK_SIZE
    return True
```

```python
def verify_shard_block_signature(beacon_state: BeaconState,
                                 signed_block: SignedShardBlock) -> bool:
    proposer = beacon_state.validators[signed_block.message.proposer_index]
    domain = get_domain(beacon_state, DOMAIN_SHARD_PROPOSAL, compute_epoch_at_slot(signed_block.message.slot))
    signing_root = compute_signing_root(signed_block.message, domain)
    return bls.Verify(proposer.pubkey, signing_root, signed_block.signature)
```

## Shard state transition

```python
def shard_state_transition(shard_state: ShardState,
                           block: ShardBlock,
                           validate_message: bool = True,
                           beacon_parent_state: Optional[BeaconState] = None) -> bool:
    if validate_message:
        assert beacon_parent_state is not None
        assert verify_shard_block_message(beacon_parent_state, shard_state, block)

    process_shard_block(shard_state, block)
    return shard_state
```

```python
def process_shard_block(shard_state: ShardState,
                        block: ShardBlock) -> None:
    """
    Update ``shard_state`` with shard ``block``.
    """
    shard_state.slot = block.slot
    prev_gasprice = shard_state.gasprice
    shard_block_length = len(block.body)
    shard_state.gasprice = compute_updated_gasprice(prev_gasprice, uint64(shard_block_length))
    if shard_block_length == 0:
        latest_block_root = shard_state.latest_block_root
    else:
        latest_block_root = hash_tree_root(block)
    shard_state.latest_block_root = latest_block_root
```

## Fraud proofs

### Verifying the proof

TODO. The intent is to have a single universal fraud proof type, which contains the following parts:

1. An on-time attestation `attestation` on some shard `shard` signing a `transition: ShardTransition`
2. An index `offset_index` of a particular position to focus on
3. The `transition: ShardTransition` itself
4. The full body of the shard block `shard_block`
5. A Merkle proof to the `shard_states` in the parent block the attestation is referencing
6. The `subkey` to generate the custody bit

Call the following function to verify the proof:

```python
def is_valid_fraud_proof(beacon_state: BeaconState,
                         attestation: Attestation,
                         offset_index: uint64,
                         transition: ShardTransition,
                         block: ShardBlock,
                         subkey: BLSPubkey,
                         beacon_parent_block: BeaconBlock) -> bool:
    # 1. Check if `custody_bits[offset_index][j] != generate_custody_bit(subkey, block_contents)` for any `j`.
    custody_bits = attestation.custody_bits_blocks
    for j in range(len(custody_bits[offset_index])):
        if custody_bits[offset_index][j] != generate_custody_bit(subkey, block):
            return True

    # 2. Check if the shard state transition result is wrong between
    # `transition.shard_states[offset_index - 1]` to `transition.shard_states[offset_index]`.
    if offset_index == 0:
        shard_states = beacon_parent_block.body.shard_transitions[attestation.data.shard].shard_states
        shard_state = shard_states[len(shard_states) - 1]
    else:
        shard_state = transition.shard_states[offset_index - 1]  # Not doing the actual state updates here.

    shard_state_transition(shard_state, block, validate_message=False)
    if shard_state != transition.shard_states[offset_index]:
        return True

    return False
```

```python
def generate_custody_bit(subkey: BLSPubkey, block: ShardBlock) -> bool:
    # TODO
    ...
```
