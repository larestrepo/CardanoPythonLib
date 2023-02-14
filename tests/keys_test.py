import os
import sys
import unittest
import uuid

from cardanopythonlib.keys import Keys
from cardanopythonlib.path_utils import remove_folder

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "cardanopythonlib"))

class TestLibrary(unittest.TestCase):
    def setUp(self):
        self.key = Keys()

    #####################################
    # This is the start of the section to test Starter class and Keys class
    #####################################

    def test_create_all_keys_with_words(self):
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
        key = self.key.deriveAllKeys(wallet_name, mnemonic, False)
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
        mnemonic_size = 24
        wallet_name = str(uuid.uuid1())
        print(
            f"Testing derive all keys with nmemonic size of {mnemonic_size} and wallet name {wallet_name}"
        )
        key = self.key.deriveAllKeys(wallet_name, mnemonic_size, False)
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
