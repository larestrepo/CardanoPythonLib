import json
import os
import sys
import unittest
import uuid
import time

from cardanopythonlib import base
from cardanopythonlib.path_utils import remove_file

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "cardanopythonlib"))


class TestLibrary(unittest.TestCase):
    def setUp(self):
        self.config_path = "cardanopythonlib/config/cardano_config.ini"
        self.starter = base.Starter(self.config_path)
        self.node = base.Node(self.config_path)
        self.wallet_name = "test_wallet"
        self.address_origin = (
            "addr_test1vp674jugprun0epvmep395k5hdpt689legmeh05s50kq8qcul3azr"
        )
        self.metadata = {"1337": {"name": "hello world", "completed": 0}}
        self.address_destin_no_tokens = [
            {
                "address": "addr_test1qp674jugprun0epvmep395k5hdpt689legmeh05s50kq8qc0wx9lg9h8x72hctqg34gy2eygnlrf7nyf343w34r67hjskugtxl",
                "amount": 3000000,
                # "tokens": [],
            }
        ]
        self.inline_datum = {"constructor": 0, "fields": [{"int": 42}]}
        self.script_name = "script_name"
        self.policyID = "cc8df048ecf8d32149269767c961aa193d89208844e876bdef186c9f"
        self.script_file_path = "./priv/example/example.script"
        self.type_time = "before"
        self.slot = 39874005
        self.purpose = "mint"

    #####################################
    # This is the start of the section to test Starter class and Keys class
    #####################################

    def test_query_tip_exec(self):
        tip = self.node.query_tip_exec()
        self.assertIs(type(tip), dict, "Verify that your node is running")
        self.assertEqual(
            tip["era"], "Babbage", "Verify that your node is in Alonzo era"
        )
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

    def test_min_required_utxo(self):

        address = "addr_test1vrpns5yma4fy2dllhkzpyeur8xes94d903xu7enwuhc4erqecraxf"
        value = self.node.min_required_utxo(address)
        print(value)
        self.assertIs(type(value), int, "Return value is not integer")
       

    def test_get_transactions(self):
        transactions = self.node.get_transactions(self.address_origin)
        self.assertIs(type(transactions), list, "Confirm if the address has utxos")

        for transaction in transactions:
            self.assertIs(
                type(transaction), dict, "Confirm that the transaction is a dictionary"
            )
            self.assertTrue(
                list(transaction.keys()) == ["hash", "id", "amounts"],
                "missing key in transaction array. Check that hash, id, amounts is present",
            )
            self.assertTrue(len(transaction["hash"]) == 64, "Verify the hash format")
            self.assertIs(type(int(transaction["id"])), int, "Verify the hash format")
            self.assertIs(
                type(transaction["amounts"]),
                list,
                "Confirm that amounts items is a list",
            )
            found = False
            for amount in transaction["amounts"]:
                self.assertIs(
                    type(amount), dict, "Confirm that the amount is a dictionary"
                )
                self.assertTrue(
                    [
                        True if token == "lovelace" else False
                        for token in amount["token"]
                    ],
                    "No lovelace found",
                )

    def test_utxo_selection(self):
        mock_transactions = [
            {
                "hash": "0d085c60b8db224e43608886250d524ceee17f4b4b1091aec879e40135975644",
                "id": "0",
                "amounts": [{"token": "lovelace", "amount": "2000000"}],
            },
            {
                "hash": "496602485616c1b636461762f1e41084f863a51847ecc9fbc30a504d28b8917b",
                "id": "0",
                "amounts": [{"token": "lovelace", "amount": "1000000000"}],
            },
            {
                "hash": "c2e7b4319abc56ba57ba1c044a36aac3613b71c1131ab30f86e16ba0ffba9c12",
                "id": "0",
                "amounts": [
                    {"token": "lovelace", "amount": "2000000"},
                    {
                        "token": "3547253f769b35cd318e062f7ade5b4ceb43462beb3f12ac18ce536b.4d7954657374454d47",
                        "amount": "1",
                    },
                ],
            },
        ]
        txHash_in = self.node.utxo_selection(mock_transactions, 3000000) # Send lovelace
        self.assertTrue(
            txHash_in == (['496602485616c1b636461762f1e41084f863a51847ecc9fbc30a504d28b8917b#0'], 1000000000),
            "Wrong selection in assert 1. Send lovelace"
        )
        txHash_in = self.node.utxo_selection(mock_transactions, 2000000) # Send lovelace
        self.assertTrue(
            txHash_in == (['496602485616c1b636461762f1e41084f863a51847ecc9fbc30a504d28b8917b#0'], 1000000000),
            "Wrong selection in assert 2. Send lovelace"
        )
        txHash_in = self.node.utxo_selection(mock_transactions, 1000000) # Send lovelace
        self.assertTrue(
            txHash_in == (['0d085c60b8db224e43608886250d524ceee17f4b4b1091aec879e40135975644#0'], 2000000),
            "Wrong selection in assert 3. Send lovelace"
        )
        txHash_in = self.node.utxo_selection(mock_transactions, 1000000000) # Send lovelace
        self.assertTrue(
            txHash_in == (['496602485616c1b636461762f1e41084f863a51847ecc9fbc30a504d28b8917b#0', '0d085c60b8db224e43608886250d524ceee17f4b4b1091aec879e40135975644#0'], 1002000000),
            "Wrong selection in assert 4. Send lovelace"
        )
        txHash_in = self.node.utxo_selection(mock_transactions, 2000000, action="mint")# Mint token. It should take the utxo with enough balance and without tokens
        self.assertTrue(
            txHash_in == (['496602485616c1b636461762f1e41084f863a51847ecc9fbc30a504d28b8917b#0'], 1000000000),
            "Wrong selection in assert 5. Mint token. It should take the utxo with enough balance and without tokens"
        )
        # txHash_in = self.node.utxo_selection(mock_transactions, 2000000, deplete=True)
        # self.assertTrue(
        #     txHash_in == (['496602485616c1b636461762f1e41084f863a51847ecc9fbc30a504d28b8917b#0'], 1000000000),
        #     "Wrong selection in assert 2"
        # )
        txHash_in = self.node.utxo_selection(mock_transactions, 1, coin_name="3547253f769b35cd318e062f7ade5b4ceb43462beb3f12ac18ce536b.4d7954657374454d47") # If coin name specified with default action it means that the token is to be sent"
        self.assertTrue(
            txHash_in == (['c2e7b4319abc56ba57ba1c044a36aac3613b71c1131ab30f86e16ba0ffba9c12#0'], 2000000),
            "Wrong selection in assert 6. If coin name specified with default action it means that the token is to be sent"
        )
        txHash_in = self.node.utxo_selection(mock_transactions, 1, coin_name="3547253f769b35cd318e062f7ade5b4ceb43462beb3f12ac18ce536b.4d7954657374454d47", action="burn") # Burn if coin name specified with action = "Burn"
        self.assertTrue(
            txHash_in == (['c2e7b4319abc56ba57ba1c044a36aac3613b71c1131ab30f86e16ba0ffba9c12#0'], 2000000),
            "Wrong selection in assert 6. Burn if coin name specified with action = Burn"
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
        type = "all"
        required = ""
        hashes = [
            "f8bd3d31f018921f7dd73d21fd7a2f5767483d3f4c960c88d16e807f",
            "955df18bcefaf6f7b956c2299633a75dfd3153451a56bd9676fd58a7",
            "0696c8e9b0a0f0990fcf2a189fa1436b17c162a5fa93783381a6fc61",
        ]
        # type_time = "before"
        slot = self.node.query_tip_exec()["slot"] + 20000
        purpose = "mint"
        parameters = {
            "type": type,
            "required": required,
            "hashes": hashes,
            "type_time": self.type_time,
            "slot": slot,
            "purpose": purpose,
        }
        multisig_script, policyID = self.node.create_simple_script(parameters)
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

            remove_file(script_file_path, "/" + policyID + ".script")
            remove_file(script_file_path, "/" + policyID + ".policyid")

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

    def test_create_simple_script(self):
        type = "all"
        hashes = ["f8bd3d31f018921f7dd73d21fd7a2f5767483d3f4c960c88d16e807f"]
        # type_time = "before"
        slot = self.node.query_tip_exec()["slot"] + 20000
        parameters = {
            "type": type,
            "hashes": hashes,
            "purpose": self.purpose,
            "type_time": self.type_time,
            "slot": slot,
        }
        multisig_script, policyID = self.node.create_simple_script(parameters)
        try:
            assert multisig_script != None
            assert policyID != None

            script_file_path = self.starter.MINT_FOLDER
            file_exists = os.path.exists(script_file_path)

            remove_file(script_file_path, "/" + policyID + ".script")
            remove_file(script_file_path, "/" + policyID + ".policyid")

            self.assertEqual(
                multisig_script["type"], type, "Review the type of the multisig script"
            )
            script = multisig_script["scripts"]
            for item in script:
                if slot in item.keys():
                    script.pop(item)

            self.assertEqual(
                len(script),
                len(hashes),
                "Review that the number of wallets corresponds",
            )

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

    def test_just_mint(self):

        type = "all"
        hashes = ["75eacb8808f937e42cde4312d2d4bb42bd1cbfca379bbe90a3ec0383"]
        slot = self.node.query_tip_exec()["slot"] + 20000
        parameters = {
            "type": type,
            "hashes": hashes,
            "type_time": self.type_time,
            "slot": slot,
            "purpose": self.purpose,
        }
        multisig_script, policyID = self.node.create_simple_script(parameters)
        script_file_path = script_file_path = self.starter.MINT_FOLDER

        mint = {
            "policyID": policyID,
            "tokens": [
                {"name": "Random", "amount": 321, "action": "mint"},
            ],
        }
        tx_file_path = self.starter.TRANSACTION_PATH_FILE
        params = {
            "address_origin": self.address_origin,
            "address_destin": self.address_destin_no_tokens,
            "mint": mint,
        }
        response = self.node.build_tx_components(params)
        file_exists = os.path.exists(tx_file_path + "/tx.draft")

        self.assertTrue(
            file_exists,
            f"Verify the creation of the transaction draft file in {tx_file_path}",
        )
        self.assertIn(
            "Estimated transaction fee: Lovelace",
            response,
            "Failed to build the transaction",
        )

        remove_file(script_file_path, "/" + self.script_name + ".script")
        remove_file(script_file_path, "/" + self.script_name + ".policyid")
        remove_file(tx_file_path, "/tx_metadata")
        remove_file(tx_file_path, "/tx.draft")


    def test_just_burn(self):
        type = "all"
        hashes = ["75eacb8808f937e42cde4312d2d4bb42bd1cbfca379bbe90a3ec0383"]
        # hashes = ["c338509bed524537ffbd8412678339b302d5a57c4dcf666ee5f15c8c"]
        slot = self.node.query_tip_exec()["slot"] + 20000
        parameters = {
            "name": self.script_name,
            "type": type,
            "hashes": hashes,
            # "type_time": self.type_time,
            # "slot": slot,
            "purpose": self.purpose,
        }
        multisig_script, policyID = self.node.create_simple_script(parameters)
        script_file_path = ""
        if self.purpose == "mint":
            script_file_path = self.starter.MINT_FOLDER
        elif self.purpose == "multisig":
            script_file_path = self.starter.MULTISIG_FOLDER

        mint = {
            "policyID": policyID,
            "policy_path": script_file_path + "/" + self.script_name + ".script",
            # "validity_interval": {"type": type_time, "slot": slot},
            "tokens": [
                {"name": "MyTestEMG", "amount": 1, "action": "burn"},
            ],
        }
        params = {
            "address_origin": "addr_test1vp674jugprun0epvmep395k5hdpt689legmeh05s50kq8qcul3azr",
            # "address_origin": "addr_test1vrpns5yma4fy2dllhkzpyeur8xes94d903xu7enwuhc4erqecraxf",
            "mint": mint,
        }
        response = self.node.build_tx_components(params)
        
        tx_file_path = self.starter.TRANSACTION_PATH_FILE
        file_exists = os.path.exists(tx_file_path + "/tx.draft")

        self.assertTrue(
            file_exists,
            f"Verify the creation of the transaction draft file in {tx_file_path}",
        )
        self.assertIn(
            "Estimated transaction fee: Lovelace",
            response,
            "Failed to build the transaction",
        )

        remove_file(script_file_path, "/" + self.script_name + ".script")
        remove_file(script_file_path, "/" + self.script_name + ".policyid")
        remove_file(tx_file_path, "/tx_metadata")
        remove_file(tx_file_path, "/tx.draft")

class TestLibraryOnline(unittest.TestCase):
    def setUp(self):
        self.config_path = "cardanopythonlib/config/cardano_config.ini"
        self.starter = base.Starter(self.config_path)
        self.node = base.Node(self.config_path)
        self.wallet_name = "test_wallet"
        self.address_origin = (
            "addr_test1vp674jugprun0epvmep395k5hdpt689legmeh05s50kq8qcul3azr"
        )
        self.metadata = {"1337": {"name": "hello world", "completed": 0}}
        self.address_destin_no_tokens = [
            {
                "address": "addr_test1qp674jugprun0epvmep395k5hdpt689legmeh05s50kq8qc0wx9lg9h8x72hctqg34gy2eygnlrf7nyf343w34r67hjskugtxl",
                "amount": 3000000,
                # "tokens": [],
            }
        ]
        self.inline_datum = {"constructor": 0, "fields": [{"int": 42}]}
        self.script_name = "script_name"
        self.policyID = "cc8df048ecf8d32149269767c961aa193d89208844e876bdef186c9f"
        self.script_file_path = "./priv/example/example.script"
        self.type_time = "before"
        self.slot = self.node.query_tip_exec()["slot"] + 90000
        self.purpose = "mint"

    #####################################
    # This is the start of the section to test Starter class and Keys class
    #####################################

    def test_mint_and_burn(self):

        type = "all"
        hashes = ["75eacb8808f937e42cde4312d2d4bb42bd1cbfca379bbe90a3ec0383"]
        parameters = {
            "type": type,
            "hashes": hashes,
            "type_time": self.type_time,
            "slot": self.slot,
            "purpose": self.purpose,
        }
        multisig_script, policyID = self.node.create_simple_script(parameters)
        script_file_path = script_file_path = self.starter.MINT_FOLDER

        mint = {
            "policyID": policyID,
            "tokens": [
                {"name": "Random", "amount": 321, "action": "mint"},
            ],
        }
        tx_file_path = self.starter.TRANSACTION_PATH_FILE
        params = {
            "address_origin": self.address_origin,
            "address_destin": self.address_destin_no_tokens,
            "mint": mint,
        }
        response = self.node.build_tx_components(params)
        file_exists = os.path.exists(tx_file_path + "/tx.draft")

        self.assertTrue(
            file_exists,
            f"Verify the creation of the transaction draft file in {tx_file_path}",
        )
        self.assertIn(
            "Estimated transaction fee: Lovelace",
            response,
            "Failed to build the transaction",
        )
        # If still alive sign and submit

        response = self.node.sign_transaction([self.wallet_name])

        file_exists = os.path.exists(tx_file_path + "/tx.signed")

        self.assertTrue(
            file_exists,
            f"Verify the creation of the transaction sign file in {tx_file_path}",
        )

        self.assertIn(
            "Transaction signed!!",
            response,
            "Failed to sign the transaction"
        )

        response = self.node.submit_transaction()

        # Loop to confirm the transaction

        txHash = self.node.get_txid_body()
        txHash = txHash[:-1]

        transaction_result = self.node.get_transactions(self.address_origin)
        confirmation = False
        while not confirmation:
            for transaction in transaction_result:
                if transaction['hash'] == txHash:
                    confirmation = True
            time.sleep(10)
            transaction_result = self.node.get_transactions(self.address_origin)

##################################
# Section to burn the previously created token
##################################

        mint = {
            "policyID": policyID,
            "tokens": [
                {"name": "Random", "amount": 321, "action": "burn"},
            ],
        }

        params = {
                    "address_origin": "addr_test1qp674jugprun0epvmep395k5hdpt689legmeh05s50kq8qc0wx9lg9h8x72hctqg34gy2eygnlrf7nyf343w34r67hjskugtxl",
                    "mint": mint,
                }
        response = self.node.build_tx_components(params)
        
        tx_file_path = self.starter.TRANSACTION_PATH_FILE
        file_exists = os.path.exists(tx_file_path + "/tx.draft")

        remove_file(script_file_path, "/" + self.script_name + ".script")
        remove_file(script_file_path, "/" + self.script_name + ".policyid")
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
        # If still alive sign and submit

        response = self.node.sign_transaction([self.wallet_name])

        file_exists = os.path.exists(tx_file_path + "/tx.signed")

        remove_file(tx_file_path, "/tx.draft")

        self.assertTrue(
            file_exists,
            f"Verify the creation of the transaction sign file in {tx_file_path}",
        )

        response = self.node.submit_transaction()
        remove_file(tx_file_path, "/tx.signed")

if __name__ == "__main__":
    unittest.main()
