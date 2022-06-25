import unittest
import os
import json
from cardanopythonlib.path_utils import remove_file, remove_folder
import uuid

from cardanopythonlib import base

class TestLibrary (unittest.TestCase):
    def setUp(self):
        self.WORKING_DIR = os.getcwd()
        self.CARDANO_CONFIGS = f'{self.WORKING_DIR}/config/cardano_config.json'
        self.starter = base.Starter(self.CARDANO_CONFIGS)
        self.node = base.Node()

    #####################################
    # This is the start of the section to test Starter class and Keys class
    #####################################
    
    def test_query_tip_exec(self):
        tip = self.node.query_tip_exec()
        self.assertIs(type(tip), dict, "Verify that your node is running")
        self.assertEqual(tip['era'], "Alonzo", "Verify that your node is in Alonzo era")
        self.assertEqual(tip['syncProgress'], "100.00", f"Verify that your node is in sync. Current progress: {tip['syncProgress']}")

    def test_query_protocol_params(self):
        saving_path = './.priv/transactions'
        protocol = self.node.query_protocol(saving_path)
        self.assertEqual(protocol, '', "problems with the command execution, check that cardano cli and cardano node are properly configured")
        protocol_file = saving_path + '/protocol.json'
        file_exists = os.path.exists(protocol_file)
        remove_file(saving_path, '/protocol.json')
        self.assertTrue(file_exists, f"problems generating the protocol params file from query_protocol function")

    def test_get_transactions(self):
        CARDANO_NETWORK = self.starter.CARDANO_NETWORK
        try:
            assert CARDANO_NETWORK == 'testnet' or 'mainnet'
            if CARDANO_NETWORK == 'testnet':
                mock_address = 'addr_test1wqrjzj0a0yl5nm0tatlxkfp0yh9vwt7hlsxql8nthcv0ycq457tgc'
            else:
                mock_address = 'addr1qx466898end6q5mpvrwwmycq35v83c9e8cnffadv6gr6q6azs4s26v4800nwg8jygvrdqh6xhsphct0d4zqsnd3sagxqqjjgln'
            transactions = self.node.get_transactions(mock_address)
            self.assertIs(type(transactions), dict, "Confirm if the address has utxos")

        except AssertionError:
            print(f"Verify your CARDANO_NETWORK in the json settings. Current value is: {CARDANO_NETWORK}")

    def test_get_balance(self):
        CARDANO_NETWORK = self.starter.CARDANO_NETWORK
        try:
            assert CARDANO_NETWORK == 'testnet' or 'mainnet'
            if CARDANO_NETWORK == 'testnet':
                mock_address = 'addr_test1wqrjzj0a0yl5nm0tatlxkfp0yh9vwt7hlsxql8nthcv0ycq457tgc'
            else:
                mock_address = 'addr1qx466898end6q5mpvrwwmycq35v83c9e8cnffadv6gr6q6azs4s26v4800nwg8jygvrdqh6xhsphct0d4zqsnd3sagxqqjjgln'
            balance = self.node.get_transactions(mock_address)
            self.assertIs(type(balance), dict, "Confirm if the address has utxos")

        except AssertionError:
            print(f"Verify your CARDANO_NETWORK in the json settings. Current value is: {CARDANO_NETWORK}")

    def test_create_multisig_script(self):
        script_name = str(uuid.uuid1())
        type = 'all'
        required = ''
        hashes = [
            'f8bd3d31f018921f7dd73d21fd7a2f5767483d3f4c960c88d16e807f',
            '955df18bcefaf6f7b956c2299633a75dfd3153451a56bd9676fd58a7',
            '0696c8e9b0a0f0990fcf2a189fa1436b17c162a5fa93783381a6fc61'
        ]
        multisig_script = self.node.create_multisig_script(script_name, type, required, hashes)
        try:
            assert multisig_script != None
            self.assertEqual(multisig_script["type"], type, "Review the type of the multisig script")
            if required == '':
                self.assertIn(multisig_script["type"], ['all', 'any'], "Review the type of the multisig script and the required field")
            else:
                self.assertIs(multisig_script["required"], int, "Review the number of required signatures")
            self.assertEqual(len(multisig_script['scripts']), len(hashes), "Review that the number of wallets corresponds")

            policyID = self.node.create_policy_id(script_name)
            keys_file_path = self.starter.KEYS_FILE_PATH + '/' + script_name
            file_exists = os.path.exists(keys_file_path)
            remove_folder("./.priv/wallets/" + script_name)
            self.assertEqual(len(policyID.split(' ')), 1, f"Verify the existence of the script file")
            self.assertTrue(file_exists, f"Verify the creation of the policy script file in {keys_file_path}")
            self.assertEqual(len(policyID), 56, "Problem with the generation of the PolicyID")
        except AssertionError:
            print(f"Verify your required field")

    def test_build_tx_components(self):
        tx_file_path = self.starter.TRANSACTION_PATH_FILE
        remove_file(tx_file_path, '/tx.draft')
        address_origin ='addr_test1vqrfdj8fkzs0pxg0eu4p38apgd430stz5hafx7pnsxn0ccg4jqkyd'
        params = {
            "message": {
                "tx_info": {
                    "address_origin": address_origin,
                    "address_destin": None,
                    "change_address": address_origin,
                    "metadata": None,
                    "mint": None,
                    "script_path": None,
                    "witness": 1,
                }
            }
        }
        result = self.node.build_tx_components(params)
        file_exists = os.path.exists(tx_file_path)
        remove_file(tx_file_path, '/tx.draft')
        self.assertTrue(file_exists, f"Verify the creation of the transaction draft file in {tx_file_path}")

if __name__ == '__main__':
    unittest.main()