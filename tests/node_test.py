import unittest
import os
import json
from cardanopythonlib.path_utils import remove_file
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

    def test_check_if_cardano_cli(self):
        command_string = ['cardano-cli', '--version']
        result = self.starter.execute_command(command_string, None)
        cardano_version = result.split(' ')
        self.assertEqual(cardano_version[0], 'cardano-cli', "Could not find cardano cli")
    
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
        self.assertTrue(file_exists, f"problems generating the protocol params file from query_protocol function")
        remove_file(saving_path, '/protocol.json')

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





if __name__ == '__main__':
    unittest.main()