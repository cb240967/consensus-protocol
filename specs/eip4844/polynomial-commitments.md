# EIP-4844 -- Polynomial Commitments

## Table of contents

<!-- TOC -->
<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [Introduction](#introduction)
- [Custom types](#custom-types)
- [Constants](#constants)
- [Preset](#preset)
  - [Trusted setup](#trusted-setup)
- [Helper functions](#helper-functions)
  - [BLS12-381 helpers](#bls12-381-helpers)
    - [`bls_modular_inverse`](#bls_modular_inverse)
    - [`div`](#div)
    - [`lincomb`](#lincomb)
  - [KZG](#kzg)
    - [`blob_to_kzg`](#blob_to_kzg)
    - [`verify_kzg_proof`](#verify_kzg_proof)
  - [Polynomials](#polynomials)
    - [`evaluate_polynomial_in_evaluation_form`](#evaluate_polynomial_in_evaluation_form)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->
<!-- /TOC -->


## Introduction

This document specifies basic polynomial operations and KZG polynomial commitment operations as they are needed for the EIP-4844 specification. The implementations are not optimized for performance, but readability. All practical implementations should optimize the polynomial operations.

## Custom types

| Name | SSZ equivalent | Description |
| - | - | - |
| `G1Point` | `Bytes48` | |
| `G2Point` | `Bytes96` | |
| `BLSFieldElement` | `uint256` | `x < BLS_MODULUS` |
| `KZGCommitment` | `Bytes48` | Same as BLS standard "is valid pubkey" check but also allows `0x00..00` for point-at-infinity |
| `KZGProof` | `Bytes48` | Same as for `KZGCommitment` |

## Constants

| Name | Value | Notes |
| - | - | - |
| `BLS_MODULUS` | `52435875175126190479447740508185965837690552500527637822603658699938581184513` | Scalar field modulus of BLS12-381 |
| `ROOTS_OF_UNITY` | `Vector[BLSFieldElement, FIELD_ELEMENTS_PER_BLOB]` | Roots of unity of order FIELD_ELEMENTS_PER_BLOB over the BLS12-381 field |

## Preset

### Trusted setup

The trusted setup is part of the preset: during testing a `minimal` insecure variant may be used,
but reusing the `mainnet` settings in public networks is a critical security requirement.

| Name | Value |
| - | - |
| `KZG_SETUP_G1` | `Vector[G1Point, FIELD_ELEMENTS_PER_BLOB]`, contents TBD |
| `KZG_SETUP_G2` | `Vector[G2Point, FIELD_ELEMENTS_PER_BLOB]`, contents TBD |
| `KZG_SETUP_LAGRANGE` | `Vector[KZGCommitment, FIELD_ELEMENTS_PER_BLOB]`, contents TBD |

## Helper functions

### BLS12-381 helpers

#### `bls_modular_inverse`

```python
def bls_modular_inverse(x: BLSFieldElement) -> BLSFieldElement:
    """
    Compute the modular inverse of x
    i.e. return y such that x * y % BLS_MODULUS == 1 and return 0 for x == 0
    """
    return pow(x, -1, BLS_MODULUS) if x != 0 else 0
```

#### `div`

```python
def div(x: BLSFieldElement, y: BLSFieldElement) -> BLSFieldElement:
    """Divide two field elements: `x` by `y`"""
    return (int(x) * int(bls_modular_inverse(y))) % BLS_MODULUS
```

#### `lincomb`

```python
def lincomb(points: Sequence[KZGCommitment], scalars: Sequence[BLSFieldElement]) -> KZGCommitment:
    """
    BLS multiscalar multiplication. This function can be optimized using Pippenger's algorithm and variants.
    """
    assert len(points) == len(scalars)
    result = bls.Z1
    for x, a in zip(points, scalars):
        result = bls.add(result, bls.multiply(bls.bytes48_to_G1(x), a))
    return KZGCommitment(bls.G1_to_bytes48(result))
```

#### `matrix_lincomb`

```python
def matrix_lincomb(vectors: Sequence[Sequence[BLSFieldElement]],
                   scalars: Sequence[BLSFieldElement]) -> Sequence[BLSFieldElement]:
    """
    Given a list of ``vectors``, interpret it as a 2D matrix and compute the linear combination
    of each column with `scalars`: return the resulting vector.
    """
    result = [0] * len(vectors[0])
    for v, s in zip(vectors, scalars):
        for i, x in enumerate(v):
            result[i] = (result[i] + int(s) * int(x)) % BLS_MODULUS
    return [BLSFieldElement(x) for x in result]
```

### KZG

KZG core functions. These are also defined in EIP-4844 execution specs.

#### `blob_to_kzg_commitment`

```python
def blob_to_kzg_commitment(blob: Blob) -> KZGCommitment:
    return lincomb(KZG_SETUP_LAGRANGE, blob)
```

#### `verify_kzg_proof`

```python
def verify_kzg_proof(polynomial_kzg: KZGCommitment,
                     z: BLSFieldElement,
                     y: BLSFieldElement,
                     kzg_proof: KZGProof) -> bool:
    """
    Verify KZG proof that ``p(z) == y`` where ``p(z)`` is the polynomial represented by ``polynomial_kzg``.
    """
    # Verify: P - y = Q * (X - z)
    X_minus_z = bls.add(bls.bytes96_to_G2(KZG_SETUP_G2[1]), bls.multiply(bls.G2, BLS_MODULUS - z))
    P_minus_y = bls.add(bls.bytes48_to_G1(polynomial_kzg), bls.multiply(bls.G1, BLS_MODULUS - y))
    return bls.pairing_check([
        [P_minus_y, bls.neg(bls.G2)],
        [bls.bytes48_to_G1(kzg_proof), X_minus_z]
    ])
```

#### `compute_kzg_proof`

```python
def compute_kzg_proof(polynomial: Sequence[BLSFieldElement], z: BLSFieldElement) -> KZGProof:
    """Compute KZG proof at point `z` with `polynomial` being in evaluation form"""

    # To avoid SSZ overflow/underflow, convert element into int
    polynomial = [int(i) for i in polynomial]
    z = int(z)

    # Shift our polynomial first (in evaluation form we can't handle the division remainder)
    y = evaluate_polynomial_in_evaluation_form(polynomial, z)
    polynomial_shifted = [(p - int(y)) % BLS_MODULUS for p in polynomial]

    # Make sure we won't divide by zero during division
    assert z not in ROOTS_OF_UNITY
    denominator_poly = [(x - z) % BLS_MODULUS for x in ROOTS_OF_UNITY]

    # Calculate quotient polynomial by doing point-by-point division
    quotient_polynomial = [div(a, b) for a, b in zip(polynomial_shifted, denominator_poly)]
    return KZGProof(lincomb(KZG_SETUP_LAGRANGE, quotient_polynomial))
```

### Polynomials

#### `evaluate_polynomial_in_evaluation_form`

```python
def evaluate_polynomial_in_evaluation_form(polynomial: Sequence[BLSFieldElement],
                                           z: BLSFieldElement) -> BLSFieldElement:
    """
    Evaluate a polynomial (in evaluation form) at an arbitrary point `z`
    Uses the barycentric formula:
       f(z) = (1 - z**WIDTH) / WIDTH  *  sum_(i=0)^WIDTH  (f(DOMAIN[i]) * DOMAIN[i]) / (z - DOMAIN[i])
    """
    width = len(polynomial)
    assert width == FIELD_ELEMENTS_PER_BLOB
    inverse_width = bls_modular_inverse(width)

    # Make sure we won't divide by zero during division
    assert z not in ROOTS_OF_UNITY

    result = 0
    for i in range(width):
        result += div(int(polynomial[i]) * int(ROOTS_OF_UNITY[i]), (z - ROOTS_OF_UNITY[i]))
    result = result * (pow(z, width, BLS_MODULUS) - 1) * inverse_width % BLS_MODULUS
    return result
```

