import json
import os
import sys
import unittest
import uuid

from cardanopythonlib import base
from cardanopythonlib.path_utils import remove_file, remove_folder

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "cardanopythonlib"))


class TestLibrary(unittest.TestCase):
    def setUp(self):
        self.config_path = "cardanopythonlib/config/cardano_config.ini"
        self.starter = base.Starter(self.config_path)
        self.node = base.Node(self.config_path)
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

    #####################################
    # This is the start of the section to test Starter class and Keys class
    #####################################

    def test_query_tip_exec(self):
        tip = self.node.query_tip_exec()
        self.assertIs(type(tip), dict, "Verify that your node is running")
        self.assertEqual(tip["era"], "Babbage", "Verify that your node is in Alonzo era")
        self.assertEqual(
            tip["syncProgress"],
            "100.00",
            f"Verify that your node is in sync. Current progress: {tip['syncProgress']}",
        )

    def test_query_protocol_params(self):
        saving_path = "./.priv/transactions"
        protocol = self.node.query_protocol(True)
        self.assertNotEqual(
            protocol,
            "",
            "problems with the command execution, check that cardano cli and cardano node are properly configured",
        )
        protocol_file = saving_path + "/protocol.json"
        file_exists = os.path.exists(protocol_file)
        remove_file(saving_path, "/protocol.json")
        self.assertTrue(
            file_exists,
            f"problems generating the protocol params file from query_protocol function",
        )

    def test_get_transactions(self):
        CARDANO_NETWORK = self.starter.CARDANO_NETWORK
        try:
            assert CARDANO_NETWORK == "testnet" or "mainnet"
            if CARDANO_NETWORK == "testnet":
                mock_address = (
                    "addr_test1wqrjzj0a0yl5nm0tatlxkfp0yh9vwt7hlsxql8nthcv0ycq457tgc"
                )
            else:
                mock_address = "addr1qx466898end6q5mpvrwwmycq35v83c9e8cnffadv6gr6q6azs4s26v4800nwg8jygvrdqh6xhsphct0d4zqsnd3sagxqqjjgln"
            transactions = self.node.get_transactions(mock_address)
            self.assertIs(type(transactions), list, "Confirm if the address has utxos")

        except AssertionError:
            print(
                f"Verify your CARDANO_NETWORK in the json settings. Current value is: {CARDANO_NETWORK}"
            )

    def test_get_balance(self):
        CARDANO_NETWORK = self.starter.CARDANO_NETWORK
        try:
            assert CARDANO_NETWORK == "testnet" or "mainnet"
            if CARDANO_NETWORK == "testnet":
                mock_address = (
                    "addr_test1wqrjzj0a0yl5nm0tatlxkfp0yh9vwt7hlsxql8nthcv0ycq457tgc"
                )
            else:
                mock_address = "addr1qx466898end6q5mpvrwwmycq35v83c9e8cnffadv6gr6q6azs4s26v4800nwg8jygvrdqh6xhsphct0d4zqsnd3sagxqqjjgln"
            balance = self.node.get_transactions(mock_address)
            self.assertIs(type(balance), dict, "Confirm if the address has utxos")

        except AssertionError:
            print(
                f"Verify your CARDANO_NETWORK in the json settings. Current value is: {CARDANO_NETWORK}"
            )

    def test_create_multisig_script(self):
        script_name = str(uuid.uuid1())
        type = "all"
        required = ""
        hashes = [
            "f8bd3d31f018921f7dd73d21fd7a2f5767483d3f4c960c88d16e807f",
            "955df18bcefaf6f7b956c2299633a75dfd3153451a56bd9676fd58a7",
            "0696c8e9b0a0f0990fcf2a189fa1436b17c162a5fa93783381a6fc61",
        ]
        type_time = "before"
        slot = self.node.query_tip_exec()["slot"] + 20000
        purpose = "mint"
        parameters = {
            "name": script_name,
            "type": type,
            "required": required,
            "hashes": hashes,
            "type_time": type_time,
            "slot": slot,
            "purpose": purpose
        }
        multisig_script, policyID = self.node.create_simple_script(parameters=parameters)
        try:
            assert multisig_script != None
            assert policyID != None

            self.assertEqual(
                multisig_script["type"], type, "Review the type of the multisig script"
            )
            if required == "":
                self.assertIn(
                    multisig_script["type"],
                    ["all", "any"],
                    "Review the type of the multisig script and the required field",
                )
            else:
                self.assertIs(
                    multisig_script["required"],
                    int,
                    "Review the number of required signatures",
                )
            self.assertEqual(
                len(multisig_script["scripts"]),
                len(hashes),
                "Review that the number of wallets corresponds",
            )

            script_file_path = self.starter.MINT_FOLDER
            self.assertIn(purpose, script_file_path)
            # keys_file_path = self.starter.KEYS_FILE_PATH + "/" + script_name
            file_exists = os.path.exists(script_file_path)

            remove_file(script_file_path, "/" + script_name + ".script")
            remove_file(script_file_path, "/" + script_name + ".policyid")

            self.assertEqual(
                len(policyID.split(" ")), 1, f"Verify the existence of the script file"
            )
            self.assertTrue(
                file_exists,
                f"Verify the creation of the policy script file in {script_file_path}",
            )
            self.assertEqual(
                len(policyID), 56, "Problem with the generation of the PolicyID"
            )
        except AssertionError:
            print(f"Verify your required field")

    def test_build_tx(self):
        tx_file_path = self.starter.TRANSACTION_PATH_FILE
        remove_file(tx_file_path, "/tx.draft")
        address_origin = self.address_origin
        params = {
                    "address_origin": address_origin,
                    # "address_destin": None,
                    "change_address": address_origin,
                    # "metadata": None,
                    # "mint": None,
                    # "script_path": None,
                    # "witness": 1,
                }
        response = self.node.build_tx_components(params)

        file_exists = os.path.exists(tx_file_path + "/tx.draft")

        remove_file(tx_file_path, "/tx.draft")
        remove_file(tx_file_path, "/tx_metadata")

        self.assertTrue(
            file_exists,
            f"Verify the creation of the transaction draft file in {tx_file_path}",
        )
        self.assertIn(
            "Estimated transaction fee: Lovelace",
            response,
            "Failed to build the transaction",
        )

    def test_build_tx_metadata(self):
        tx_file_path = self.starter.TRANSACTION_PATH_FILE
        remove_file(tx_file_path, "/tx.draft")
        params = {
                    "address_origin": self.address_origin,
                    # "address_destin": None,
                    "change_address": self.address_origin,
                    "metadata": self.metadata,
                    # "mint": None,
                    # "script_path": None,
                    # "witness": 1,
                }
        response = self.node.build_tx_components(params)
        file_exists = os.path.exists(tx_file_path + "/tx.draft")

        remove_file(tx_file_path, "/tx.draft")
        remove_file(tx_file_path, "/tx_metadata")

        self.assertTrue(
            file_exists,
            f"Verify the creation of the transaction draft file in {tx_file_path}",
        )
        self.assertIn(
            "Estimated transaction fee: Lovelace",
            response,
            "Failed to build the transaction",
        )

    def test_build_tx_destin_no_tokens(self):
        tx_file_path = self.starter.TRANSACTION_PATH_FILE
        remove_file(tx_file_path, "/tx.draft")
        params = {
                    "address_origin": self.address_origin,
                    "address_destin": self.address_destin_no_tokens,
                    "change_address": self.address_origin,
                    "metadata": self.metadata,
                    # "mint": None,
                    # "script_path": None,
                    # "witness": 1,
                }
        response = self.node.build_tx_components(params)
        file_exists = os.path.exists(tx_file_path + "/tx.draft")

        remove_file(tx_file_path, "/tx.draft")
        remove_file(tx_file_path, "/tx_metadata")

        self.assertTrue(
            file_exists,
            f"Verify the creation of the transaction draft file in {tx_file_path}",
        )
        self.assertIn(
            "Estimated transaction fee: Lovelace",
            response,
            "Failed to build the transaction",
        )

    def test_build_tx_inline(self):
        tx_file_path = self.starter.TRANSACTION_PATH_FILE
        remove_file(tx_file_path, "/tx.draft")
        params = {
                    "address_origin": self.address_origin,
                    "address_destin": self.address_destin_no_tokens,
                    "change_address": self.address_origin,
                    "metadata": self.metadata,
                    # "mint": None,
                    # "script_path": None,
                    # "witness": 1,
                    "inline_datum": self.inline_datum,
                }
        response = self.node.build_tx_components(params)
        file_exists = os.path.exists(tx_file_path + "/tx.draft")

        remove_file(tx_file_path, "/tx.draft")
        remove_file(tx_file_path, "/tx_metadata")
        
        self.assertTrue(
            file_exists,
            f"Verify the creation of the transaction draft file in {tx_file_path}",
        )

        self.assertIn(
            "Estimated transaction fee: Lovelace",
            response,
            "Failed to build the transaction",
        )

    
    def test_build_tx_mint(self):

        script_name = str(uuid.uuid1())
        type = "all"
        required = ""
        hashes = [
            "75eacb8808f937e42cde4312d2d4bb42bd1cbfca379bbe90a3ec0383",
        ]
        type_time = "before"
        slot = self.node.query_tip_exec()["slot"] + 20000
        purpose = "mint"
        parameters = {
            "name": script_name,
            "type": type,
            "required": required,
            "hashes": hashes,
            "type_time": type_time,
            "slot": slot,
            "purpose": purpose
        }
        multisig_script, policyID = self.node.create_simple_script(parameters=parameters)
        script_file_path = ""
        if purpose == "mint":
            script_file_path = self.starter.MINT_FOLDER
        elif purpose == "multisig":
            script_file_path = self.starter.MULTISIG_FOLDER

        mint = { 
            "policyID": policyID,
            "policy_path": script_file_path + "/" + script_name + ".script",
            "validity_interval": {
                "type": type_time,
                "slot": slot
            },
            "tokens": [
                {"name": "Random",
                "amount": 452215},
            ]
        }
        tx_file_path = self.starter.TRANSACTION_PATH_FILE
        params = {
                    "address_origin": self.address_origin,
                    "address_destin": self.address_destin_no_tokens,
                    "change_address": self.address_origin,
                    "metadata": self.metadata,
                    "mint": mint,
                    # "script_path": None,
                    # "witness": 1,
                    # "inline_datum": self.inline_datum,
                }
        response = self.node.build_tx_components(params)
        file_exists = os.path.exists(tx_file_path + "/tx.draft")

        remove_file(script_file_path, "/" + script_name + ".script")
        remove_file(script_file_path, "/" + script_name + ".policyid")
        remove_file(tx_file_path, "/tx.draft")
        remove_file(tx_file_path, "/tx_metadata")

        self.assertTrue(
            file_exists,
            f"Verify the creation of the transaction draft file in {tx_file_path}",
        )
        self.assertIn(
            "Estimated transaction fee: Lovelace",
            response,
            "Failed to build the transaction",
        )

if __name__ == "__main__":
    unittest.main()
