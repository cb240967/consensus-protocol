from eth2spec.utils.ssz.ssz_impl import hash_tree_root
from eth2spec.utils.ssz.ssz_typing import (
    SSZValue, uint, Container, Bool
)


def encode(value: SSZValue, include_hash_tree_roots=False):
    if isinstance(value, uint):
        # Larger uints are boxed and the class declares their byte length
        if value.type().byte_len > 8:
            return str(int(value))
        return int(value)
    elif isinstance(value, Bool):
        return value == 1
    elif isinstance(value, list):  # normal python lists, ssz-List, Vector
        return [encode(element, include_hash_tree_roots) for element in value]
    elif isinstance(value, bytes):  # both bytes and BytesN
        return '0x' + value.hex()
    elif isinstance(value, Container):
        ret = {}
        for field_value, field_name in zip(value, value.get_fields().keys()):
            ret[field_name] = encode(field_value, include_hash_tree_roots)
            if include_hash_tree_roots:
                ret[field_name + "_hash_tree_root"] = '0x' + hash_tree_root(field_value).hex()
        if include_hash_tree_roots:
            ret["hash_tree_root"] = '0x' + hash_tree_root(value).hex()
        return ret
    else:
        raise Exception(f"Type not recognized: value={value}, typ={value.type()}")
