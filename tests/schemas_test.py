import json
import os
import sys
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "cardanopythonlib"))

from cardanopythonlib import schemas
from cerberus import Validator


class TestLibrary(unittest.TestCase):
    def setUp(self):
        self.v = Validator()
        self.address_origin = 'addr_test1vp674jugprun0epvmep395k5hdpt689legmeh05s50kq8qcul3azr'
        self.metadata = {"1337": {"name": "hello world", "completed": 0}}
        self.address_destin_no_tokens = [
                                {
                                    "address": "addr_test1qp674jugprun0epvmep395k5hdpt689legmeh05s50kq8qc0wx9lg9h8x72hctqg34gy2eygnlrf7nyf343w34r67hjskugtxl",
                                    "amount": 3000000,
                                    "tokens": [],
                                }]
        self.inline_datum = {
                            "constructor": 0,
                            "fields": [{
                                "int": 42
                            }]

        }

        self.build_tx_components_schema = schemas.build_tx_components_schema
        self.create_simple_script_schema = schemas.create_simple_script_schema
        self.script_name = "script_name"
        self.policyID = "cc8df048ecf8d32149269767c961aa193d89208844e876bdef186c9f"
        self.script_file_path = "./priv/example/example.script"
        self.type_time = "before"
        self.slot = 39874005
        self.purpose = "mint"

    #####################################
    # This is the start of the section to test Starter class and Keys class
    #####################################

    def test_build_tx_components_schema(self):

        # Test build_tx_components_schema
        
        params = {
            "address_origin": self.address_origin,
        }
        self.assertTrue(
            self.v.validate(params, self.build_tx_components_schema), # type: ignore
            self.v.errors, # type: ignore
        )
        params = {
            "address_origin": self.address_origin,
            "change_address": self.address_origin,
        }
        self.assertTrue(
            self.v.validate(params, self.build_tx_components_schema), # type: ignore
            self.v.errors, # type: ignore
        )
        params = {
            "address_origin": self.address_origin,
            "change_address": self.address_origin,
            "metadata": self.metadata,
        }
        self.assertTrue(
            self.v.validate(params, self.build_tx_components_schema), # type: ignore
            self.v.errors, # type: ignore
        )
        params = {
            "address_origin": self.address_origin,
            "address_destin": self.address_destin_no_tokens,
            "change_address": self.address_origin,
            "metadata": self.metadata,
        }
        self.assertTrue(
            self.v.validate(params, self.build_tx_components_schema), # type: ignore
            self.v.errors, # type: ignore
        )
        params = {
            "address_origin": self.address_origin,
            "address_destin": self.address_destin_no_tokens,
            "metadata": self.metadata,
        }
        self.assertTrue(
            self.v.validate(params, self.build_tx_components_schema), # type: ignore
            self.v.errors, # type: ignore
        )
        params = {
            "address_origin": self.address_origin,
            "metadata": self.metadata,
        }
        self.assertTrue(
            self.v.validate(params, self.build_tx_components_schema), # type: ignore
            self.v.errors, # type: ignore
        )
        params = {
            "address_origin": self.address_origin,
            "address_destin": self.address_destin_no_tokens,
            "change_address": self.address_origin,
            "metadata": self.metadata,
            "inline_datum": self.inline_datum,
        }
        self.assertTrue(
            self.v.validate(params, self.build_tx_components_schema), # type: ignore
            self.v.errors, # type: ignore
        )
        mint = { 
            "policyID": self.policyID,
            "policy_path": self.script_file_path,
            "validity_interval": {
                "type": self.type_time,
                "slot": self.slot
            },
            "tokens": [
                {"name": "Random",
                "amount": 452215,
                "action": "mint"},
            ]
        }
        print(mint)
        params = {
            "address_origin": self.address_origin,
            "address_destin": self.address_destin_no_tokens,
            "change_address": self.address_origin,
            "metadata": self.metadata,
            "mint": mint,
        }
        self.assertTrue(
            self.v.validate(params, self.build_tx_components_schema), # type: ignore
            self.v.errors, # type: ignore
        )

    def test_create_simple_script_schema(self):

        # Test build_tx_components_schema
        self.hashes = [
            "f8bd3d31f018921f7dd73d21fd7a2f5767483d3f4c960c88d16e807f"
        ]
        params = {
            "name": self.script_name,
            "hashes": self.hashes,
            "purpose": self.purpose,
            "type": "all"
        }

        self.assertTrue(
            self.v.validate(params, self.create_simple_script_schema), # type: ignore
            self.v.errors, # type: ignore
        )
        self.hashes = [
            "f8bd3d31f018921f7dd73d21fd7a2f5767483d3f4c960c88d16e807f",
            "f8bd3d31f018921f7dd73d21fd7a2f5767483d3f4c960c88d16e807f",
            "f8bd3d31f018921f7dd73d21fd7a2f5767483d3f4c960c88d16e807f",
        ]
        params = {
            "name": self.script_name,
            "hashes": self.hashes,
            "purpose": self.purpose,
            "type": "atLeast",
            "required": 2
        }

        self.assertTrue(
            self.v.validate(params, self.create_simple_script_schema), # type: ignore
            self.v.errors, # type: ignore
        )

        params = {
            "name": self.script_name,
            "hashes": self.hashes,
            "purpose": self.purpose,
            "type": "atLeast",
            "required": 2,
            "type_time": self.type_time,
            "slot": self.slot,

        }

        self.assertTrue(
            self.v.validate(params, self.create_simple_script_schema), # type: ignore
            self.v.errors, # type: ignore
        )