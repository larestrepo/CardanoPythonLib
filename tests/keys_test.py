import unittest
import os
import json
from cardanopythonlib.path_utils import remove_folder
import uuid

from cardanopythonlib import base

class TestLibrary (unittest.TestCase):
    def setUp(self):
        self.WORKING_DIR = os.getcwd()
        self.CARDANO_CONFIGS = f'{self.WORKING_DIR}/config/cardano_config.json'
        self.starter = base.Starter(self.CARDANO_CONFIGS)

    #####################################
    # This is the start of the section to test Starter class and Keys class
    #####################################
    def test_cardano_config_json_existence(self):
        file_exists = os.path.exists(self.CARDANO_CONFIGS)
        self.assertTrue(file_exists, f"config file does not exists in {self.CARDANO_CONFIGS}")

    def test_env_variables_existence(self):
        with open(self.CARDANO_CONFIGS) as file:
            from_json = json.load(file)
        keys_list = [
            'CARDANO_NETWORK_MAGIC',
            'CARDANO_CLI_PATH',
            'CARDANO_NETWORK',
            'TRANSACTION_PATH_FILE',
            'KEYS_FILE_PATH',
            'URL'
        ]
        for key in from_json['node'].keys():
            self.assertIn(key, keys_list, f"Missing key: {key}")
    
    def test_env_variables_value(self):
        
        CARDANO_CLI_PATH = self.starter.CARDANO_CLI_PATH
        CARDANO_NETWORK = self.starter.CARDANO_NETWORK
        TRANSACTION_PATH_FILE = self.starter.TRANSACTION_PATH_FILE
        KEYS_FILE_PATH = self.starter.KEYS_FILE_PATH
        URL = self.starter.URL
        
        self.assertEqual(CARDANO_CLI_PATH.upper(), 'CARDANO-CLI')
        network_list = ['testnet', 'mainnet']
        self.assertIn(CARDANO_NETWORK, network_list, f"Cardano_network param should be one of those: {network_list}")
        self.assertNotEqual(TRANSACTION_PATH_FILE, '', f"Transaction_path_file should not be empty")
        self.assertNotEqual(KEYS_FILE_PATH, '', "Keys_file_path should not be empty")
        self.assertNotEqual(URL, '', "URL should not be empty")
    
    def test_min_utxo_lovelace(self):
        utxoCostPerWord = 34482 # from protocol params
        minUTxOValue = self.starter.min_utxo_lovelace(0, 0, utxoCostPerWord, '')
        self.assertEqual(minUTxOValue, 1275834, "Problem with the min_utxo_lovelace function")

    def test_create_all_keys_with_words(self):
        keys = base.Keys()
        mnemonic_size = 24
        wallet_name = str(uuid.uuid1())
        print (f"Testing derive all keys with nmemonic size of {mnemonic_size} and wallet name {wallet_name}")
        mnemonic = ['dial','ivory','leave','fog','boring','nose','brass','food','kitchen','example','fame','expire','apart','game','pipe','ship','excite','sponsor','bread','place','beach','raven','prevent','stem']
        key = keys.deriveAllKeys(wallet_name, words=mnemonic)
        self.assertEqual(len(key['mnemonic']), mnemonic_size, "Problem with mnemonic")
        self.assertTrue(key['root_key'].startswith('root_xsk'), "Problem with root key")
        self.assertTrue(key['private_stake_key'].startswith('stake_xsk'), "Problem with private stake key")
        self.assertTrue(key['private_payment_key'].startswith('addr_xsk'), "Problem with private payment key")
        self.assertTrue(key['payment_account_key'].startswith('addr_xvk'), "Problem with payment account key")
        self.assertTrue(key['stake_account_key'].startswith('stake_xvk'), "Problem with stake account key")
        self.assertTrue(key['payment_addr'].startswith('addr'), "Problem with payment address")
        self.assertEqual(key['payment_addr_path'], "./.priv/wallets/" + wallet_name + "/" + wallet_name + ".payment.addr", "Problem with payment_addr_path")
        self.assertEqual(key['payment_skey_path'], "./.priv/wallets/" + wallet_name + "/" + wallet_name + ".payment.skey", "Problem with payment_skey_path")
        self.assertEqual(key['payment_vkey_path'], "./.priv/wallets/" + wallet_name + "/" + wallet_name + ".payment.vkey", "Problem with payment_vkey_path")
        self.assertEqual(key['stake_skey_path'], "./.priv/wallets/" + wallet_name + "/" + wallet_name + ".stake.skey", "Problem with stake_skey_path")
        self.assertEqual(key['stake_vkey_path'], "./.priv/wallets/" + wallet_name + "/" + wallet_name + ".stake.vkey", "Problem with stake_vkey_path")
        self.assertEqual(key['stake_addr_path'], "./.priv/wallets/" + wallet_name + "/" + wallet_name + ".stake.addr", "Problem with stake_addr_path")
        self.assertTrue(key['base_addr_path'].startswith('addr'), "Problem with base_addr_path")
        self.assertEqual(len(key['hash_verification_key']), 56, "Problem with hash_verification_key")
        remove_folder("./.priv/wallets/" + wallet_name)

    def test_create_all_keys_with_size(self):
        keys = base.Keys()
        mnemonic_size = 24
        wallet_name = str(uuid.uuid1())
        print (f"Testing derive all keys with nmemonic size of {mnemonic_size} and wallet name {wallet_name}")
        key = keys.deriveAllKeys(wallet_name, size=mnemonic_size)
        self.assertEqual(len(key['mnemonic']), mnemonic_size, "Problem with mnemonic")
        self.assertTrue(key['root_key'].startswith('root_xsk'), "Problem with root key")
        self.assertTrue(key['private_stake_key'].startswith('stake_xsk'), "Problem with private stake key")
        self.assertTrue(key['private_payment_key'].startswith('addr_xsk'), "Problem with private payment key")
        self.assertTrue(key['payment_account_key'].startswith('addr_xvk'), "Problem with payment account key")
        self.assertTrue(key['stake_account_key'].startswith('stake_xvk'), "Problem with stake account key")
        self.assertTrue(key['payment_addr'].startswith('addr'), "Problem with payment address")
        self.assertEqual(key['payment_addr_path'], "./.priv/wallets/" + wallet_name + "/" + wallet_name + ".payment.addr", "Problem with payment_addr_path")
        self.assertEqual(key['payment_skey_path'], "./.priv/wallets/" + wallet_name + "/" + wallet_name + ".payment.skey", "Problem with payment_skey_path")
        self.assertEqual(key['payment_vkey_path'], "./.priv/wallets/" + wallet_name + "/" + wallet_name + ".payment.vkey", "Problem with payment_vkey_path")
        self.assertEqual(key['stake_skey_path'], "./.priv/wallets/" + wallet_name + "/" + wallet_name + ".stake.skey", "Problem with stake_skey_path")
        self.assertEqual(key['stake_vkey_path'], "./.priv/wallets/" + wallet_name + "/" + wallet_name + ".stake.vkey", "Problem with stake_vkey_path")
        self.assertEqual(key['stake_addr_path'], "./.priv/wallets/" + wallet_name + "/" + wallet_name + ".stake.addr", "Problem with stake_addr_path")
        self.assertTrue(key['base_addr_path'].startswith('addr'), "Problem with base_addr_path")
        self.assertEqual(len(key['hash_verification_key']), 56, "Problem with hash_verification_key")
        remove_folder("./.priv/wallets/" + wallet_name)


if __name__ == '__main__':
    unittest.main()