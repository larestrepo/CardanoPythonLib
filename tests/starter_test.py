import os
import unittest

from cardanopythonlib import starter
from cardanopythonlib.path_utils import remove_file
from cardanopythonlib.path_utils import config

class TestLibrary(unittest.TestCase):
    def setUp(self):
        self.config_path = "cardanopythonlib/config/cardano_config.ini"
        self.starter = starter.Starter()
        self.address_origin = (
            "addr_test1vrpns5yma4fy2dllhkzpyeur8xes94d903xu7enwuhc4erqecraxf"
        )

    #####################################
    # This is the start of the section to test Starter class and Keys class
    #####################################
    def test_cardano_config_json_existence(self):
        file_exists = os.path.exists(self.config_path)
        self.assertTrue(
            file_exists, f"config file does not exists in {self.config_path}"
        )

    def test_env_variables_existence(self):
        keys_list = [
            "cardano_network_magic",
            "cardano_cli_path",
            "cardano_network",
            "transaction_path_file",
            "keys_file_path",
            "scripts_file_path",
            "cardano_era",
            "url",
        ]
        params = config(self.config_path, "node")
        for key in params.keys():
            self.assertIn(key, keys_list, f"Missing value: {key}")

    def test_env_variables_value(self):

        KEYS_FILE_PATH = self.starter.KEYS_FILE_PATH
        SCRIPTS_FILE_PATH = self.starter.SCRIPTS_FILE_PATH
        CARDANO_CLI_PATH = self.starter.CARDANO_CLI_PATH
        CARDANO_NETWORK = self.starter.CARDANO_NETWORK
        TRANSACTION_PATH_FILE = self.starter.TRANSACTION_PATH_FILE
        CARDANO_ERA = self.starter.CARDANO_ERA
        URL = self.starter.URL

        self.assertNotEqual(CARDANO_CLI_PATH, "", f"cardano_cli should not be empty")
        if CARDANO_CLI_PATH is not None:
            self.assertEqual(CARDANO_CLI_PATH.upper(), "CARDANO-CLI")
        network_list = ["testnet", "mainnet"]
        self.assertIn(
            CARDANO_NETWORK,
            network_list,
            f"Cardano_network param should be one of those: {network_list}",
        )
        self.assertNotEqual(TRANSACTION_PATH_FILE, "", f"Transaction_path_file should not be empty")
        self.assertNotEqual(KEYS_FILE_PATH, "", "Keys_file_path should not be empty")
        self.assertNotEqual(URL, "", "URL should not be empty")
        self.assertNotEqual(SCRIPTS_FILE_PATH, "", "SCRIPTS_FILE_PATH should not be empty")
        self.assertNotEqual(CARDANO_ERA, "", "CARDANO_ERA should not be empty")

    def test_query_protocol_params(self):
        saving_path = "./.priv/transactions"
        protocol = self.starter.query_protocol(True)
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
        value = self.starter.min_required_utxo(address)
        print(value)
        self.assertIs(type(value), int, "Return value is not integer")
       

    def test_get_transactions(self):
        transactions = self.starter.get_transactions(self.address_origin)
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
            balance = self.starter.get_transactions(mock_address)
            self.assertIs(type(balance), dict, "Confirm if the address has utxos")

        except AssertionError:
            print(
                f"Verify your CARDANO_NETWORK in the json settings. Current value is: {CARDANO_NETWORK}"
            )