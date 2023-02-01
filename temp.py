from cardanopythonlib.datatypes.serialization import IndefiniteList
from cardanopythonlib.datatypes.plutus import PlutusData
from dataclasses import dataclass

# empty_datum = PlutusData()
# print(empty_datum)

@dataclass
class MyDatum(PlutusData):
    CONSTR_ID = 1
    a: int
    b: bytes
    c: IndefiniteList
    d: dict

datum = MyDatum(123, b"1234", IndefiniteList([4, 5, 6]), {1: b"1", 2: b"2"})
datum.to_cbor()

@dataclass
class InclusionDatum(PlutusData):
    CONSTR_ID = 1
    beneficiary: bytes
    deadline: int
    other_data: MyDatum

key_hash = bytes.fromhex("c2ff616e11299d9094ce0a7eb5b7284b705147a822f4ffbd471f971a")
deadline = 1643235300000
other_datum = MyDatum(123, b"1234", IndefiniteList([4, 5, 6]), {1: b"1", 2: b"2"})
include_datum = InclusionDatum(key_hash, deadline, other_datum)
print(include_datum.to_cbor())
encoded_json = include_datum.to_json(separators=(",", ":"))
print(encoded_json)