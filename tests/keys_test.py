import unittest
import os
import json
from cardanopythonlib.path_utils import remove_folder
import uuid

from cardanopythonlib import base

def assertIsfile(path):
    file_exists = os.path.exists(path)
    return file_exists

class TestLibrary (unittest.TestCase):
    def setUp(self):
        self.WORKING_DIR = os.getcwd()
        self.CARDANO_CONFIGS = f'{self.WORKING_DIR}/config/cardano_config.json'
        self.starter = base.Starter(self.CARDANO_CONFIGS)
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
        
        CARDANO_NETWORK_MAGIC = self.starter.CARDANO_NETWORK_MAGIC
        CARDANO_CLI_PATH = self.starter.CARDANO_CLI_PATH
        CARDANO_NETWORK = self.starter.CARDANO_NETWORK
        TRANSACTION_PATH_FILE = self.starter.TRANSACTION_PATH_FILE
        KEYS_FILE_PATH = self.starter.KEYS_FILE_PATH
        URL = self.starter.URL
        
        self.assertEqual(CARDANO_CLI_PATH.upper(), 'CARDANO-CLI')
        if CARDANO_NETWORK_MAGIC != '' or None:
            self.assertEqual(CARDANO_NETWORK_MAGIC, 1097911063)
        network_list = ['testnet', 'mainnet']
        self.assertIn(CARDANO_NETWORK, network_list, f"Cardano_network param should be one of those: {network_list}")
        self.assertNotEqual(TRANSACTION_PATH_FILE, '', f"Transaction_path_file should not be empty")
        self.assertNotEqual(KEYS_FILE_PATH, '', "Keys_file_path should not be empty")
        self.assertNotEqual(URL, '', "URL should not be empty")
    
    def test_min_utxo_lovelace(self):
        utxoCostPerWord = 34482 # from protocol params
        minUTxOValue = self.starter.min_utxo_lovelace(0, 0, utxoCostPerWord, '')
        self.assertEqual(minUTxOValue, 1275834, "Problem with the min_utxo_lovelace function")


    def test_create_all_keys(self):
        keys = base.Keys()

        mnemonic_size = 24
        wallet_name = str(uuid.uuid1())
        print (f"Testing derive all keys with nmemonic size of {mnemonic_size} and wallet name {wallet_name}")
        key = keys.deriveAllKeys(mnemonic_size, wallet_name)
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

# def test_create_wallet(self):
#     print(addresses[0]['id'])
#     if test_id==3: # new method
#         def test_delete_wallet(self):
#             list_wallets=wallet.list_wallets()
#             print(list_wallets)
#             for k, v in list_wallets.items():
#                 if k==[id]:
#                     wallet.delete_wallet(k)
#             # list_wallets=wallet.list_wallets()
#             # print(list_wallets)
#             # for k, v in list_wallets.items():
#             #     if k==[id]:
#             #         wallet.delete_wallet(k)
#             id = '8b94dab0fa6c5ff737b19d9dba7faca095ce1480'
#             response = wallet.delete_wallet(id)
#             print(response)
#     if test_id==4: # old method
#         def test_get_balance(self):
#             wallet01 = 'acdc'
#             token = 'ADA'
#             actual_balance01 = lb.get_balance(wallet01,token)
#             print(actual_balance01)


#     if test_id==5: #new method
#         def test_generate_nmemonic(self):
#             wallet.generate_mnemonic(24)
# def test_generate_wallet_from_nmemonic(self):

#     if test_id==7:
#         def test_minting(self):
#             wallet_name = 'Mint_wallet'
#             utils.create_minting_policy(wallet_name)
#             params= {
#                 "seq": 1,
#                 "cmd_id": "mint_asset",
#                 "message": {
#                     "tx_info": {
#                     "mint": {
#                         "id": "6c8eadf91ae46e93d953657ac968fbd4b8f0afed",
#                         "metadata": {},
#                         "address": "addr_test1qpjltzup7mjfk9vhrj4ltv6sduwv427nmjqf623jje7zt5qytthp9vmrx4y8t4kwk73jlxxsqwu75fd4dx5k5uzl54rsh4wu29",
#                         "tokens": [
#                         {
#                             "name": "testtokens2",
#                             "amount": 20,
#                             "policyID": ""
#                         }
#                         ]
#                     }
#                     }
#                 }
#                 }

#     if test_id==8:
#         def test_get_addresses(self):
#             print('executing get address')
#             id='af807b9bf120667b5fadd9e7bdee4a6dab71623f'
#             addresses = wallet.get_addresses(id)
#             print(addresses)

#     if test_id==9:

#         def test_get_balance_new(self):
#             address='addr_test1qpjltzup7mjfk9vhrj4ltv6sduwv427nmjqf623jje7zt5qytthp9vmrx4y8t4kwk73jlxxsqwu75fd4dx5k5uzl54rsh4wu29'
#             balance = node.get_balance(address)
#             print(balance)

        # def test_full_cycle(self):
        #     """ 1. Create wallet
        #     {
        #         "seq": 1,
        #         "cmd_id": "generate_new_mnemonic_phrase",
        #         "message": { 
        #                 "size": 24
        #         }
        #         }

        #     """

        #     # 1.a Create nmemonic
        #     size = 24
        #     mnemonic = wallet.generate_mnemonic(size)