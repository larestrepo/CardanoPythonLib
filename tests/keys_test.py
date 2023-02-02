import json
import os
import sys
import unittest
import uuid

from cardanopythonlib import base
from cardanopythonlib.path_utils import config, remove_folder

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "cardanopythonlib"))

class TestLibrary(unittest.TestCase):
    def setUp(self):
        self.config_path = "cardanopythonlib/config/cardano_config.ini"
        self.starter = base.Starter(self.config_path)

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

    # def test_min_utxo_lovelace(self):
    #     utxoCostPerWord = 34482  # from protocol params
    #     minUTxOValue = self.starter.min_utxo_lovelace(0, 0, utxoCostPerWord, "")
    #     self.assertEqual(
    #         minUTxOValue, 1275834, "Problem with the min_utxo_lovelace function"
    #     )

    def test_create_all_keys_with_words(self):
        keys = base.Keys()
        mnemonic_size = 24
        wallet_name = str(uuid.uuid1())
        print(
            f"Testing derive all keys with nmemonic size of {mnemonic_size} and wallet name {wallet_name}"
        )
        mnemonic = [
            "dial",
            "ivory",
            "leave",
            "fog",
            "boring",
            "nose",
            "brass",
            "food",
            "kitchen",
            "example",
            "fame",
            "expire",
            "apart",
            "game",
            "pipe",
            "ship",
            "excite",
            "sponsor",
            "bread",
            "place",
            "beach",
            "raven",
            "prevent",
            "stem",
        ]
        key = keys.deriveAllKeys(wallet_name, mnemonic, False)
        self.assertEqual(len(key["mnemonic"]), mnemonic_size, "Problem with mnemonic")
        self.assertTrue(key["root_key"].startswith("root_xsk"), "Problem with root key")
        self.assertTrue(
            key["private_stake_key"].startswith("stake_xsk"),
            "Problem with private stake key",
        )
        self.assertTrue(
            key["private_payment_key"].startswith("addr_xsk"),
            "Problem with private payment key",
        )
        self.assertTrue(
            key["payment_account_key"].startswith("addr_xvk"),
            "Problem with payment account key",
        )
        self.assertTrue(
            key["stake_account_key"].startswith("stake_xvk"),
            "Problem with stake account key",
        )
        self.assertTrue(
            key["payment_addr"].startswith("addr"), "Problem with payment address"
        )
        self.assertEqual(
            key["payment_addr_path"],
            "./.priv/wallets/" + wallet_name + "/" + wallet_name + ".payment.addr",
            "Problem with payment_addr_path",
        )
        self.assertEqual(
            key["payment_skey_path"],
            "./.priv/wallets/" + wallet_name + "/" + wallet_name + ".payment.skey",
            "Problem with payment_skey_path",
        )
        self.assertEqual(
            key["payment_vkey_path"],
            "./.priv/wallets/" + wallet_name + "/" + wallet_name + ".payment.vkey",
            "Problem with payment_vkey_path",
        )
        self.assertEqual(
            key["stake_skey_path"],
            "./.priv/wallets/" + wallet_name + "/" + wallet_name + ".stake.skey",
            "Problem with stake_skey_path",
        )
        self.assertEqual(
            key["stake_vkey_path"],
            "./.priv/wallets/" + wallet_name + "/" + wallet_name + ".stake.vkey",
            "Problem with stake_vkey_path",
        )
        self.assertEqual(
            key["stake_addr_path"],
            "./.priv/wallets/" + wallet_name + "/" + wallet_name + ".stake.addr",
            "Problem with stake_addr_path",
        )
        self.assertTrue(
            key["base_addr"].startswith("addr"), "Problem with base_addr_path"
        )
        self.assertEqual(
            len(key["hash_verification_key"]), 56, "Problem with hash_verification_key"
        )
        remove_folder("./.priv/wallets/" + wallet_name)

    def test_create_all_keys_with_size(self):
        keys = base.Keys()
        mnemonic_size = 24
        wallet_name = str(uuid.uuid1())
        print(
            f"Testing derive all keys with nmemonic size of {mnemonic_size} and wallet name {wallet_name}"
        )
        key = keys.deriveAllKeys(wallet_name, mnemonic_size, False)
        self.assertEqual(len(key["mnemonic"]), mnemonic_size, "Problem with mnemonic")
        self.assertTrue(key["root_key"].startswith("root_xsk"), "Problem with root key")
        self.assertTrue(
            key["private_stake_key"].startswith("stake_xsk"),
            "Problem with private stake key",
        )
        self.assertTrue(
            key["private_payment_key"].startswith("addr_xsk"),
            "Problem with private payment key",
        )
        self.assertTrue(
            key["payment_account_key"].startswith("addr_xvk"),
            "Problem with payment account key",
        )
        self.assertTrue(
            key["stake_account_key"].startswith("stake_xvk"),
            "Problem with stake account key",
        )
        self.assertTrue(
            key["payment_addr"].startswith("addr"), "Problem with payment address"
        )
        self.assertEqual(
            key["payment_addr_path"],
            "./.priv/wallets/" + wallet_name + "/" + wallet_name + ".payment.addr",
            "Problem with payment_addr_path",
        )
        self.assertEqual(
            key["payment_skey_path"],
            "./.priv/wallets/" + wallet_name + "/" + wallet_name + ".payment.skey",
            "Problem with payment_skey_path",
        )
        self.assertEqual(
            key["payment_vkey_path"],
            "./.priv/wallets/" + wallet_name + "/" + wallet_name + ".payment.vkey",
            "Problem with payment_vkey_path",
        )
        self.assertEqual(
            key["stake_skey_path"],
            "./.priv/wallets/" + wallet_name + "/" + wallet_name + ".stake.skey",
            "Problem with stake_skey_path",
        )
        self.assertEqual(
            key["stake_vkey_path"],
            "./.priv/wallets/" + wallet_name + "/" + wallet_name + ".stake.vkey",
            "Problem with stake_vkey_path",
        )
        self.assertEqual(
            key["stake_addr_path"],
            "./.priv/wallets/" + wallet_name + "/" + wallet_name + ".stake.addr",
            "Problem with stake_addr_path",
        )
        self.assertTrue(
            key["base_addr"].startswith("addr"), "Problem with base_addr_path"
        )
        self.assertEqual(
            len(key["hash_verification_key"]), 56, "Problem with hash_verification_key"
        )
        remove_folder("./.priv/wallets/" + wallet_name)


if __name__ == "__main__":
    unittest.main()
