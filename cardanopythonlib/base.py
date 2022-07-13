"""
This submodule defines the main classes representing the following Cardano
objects: Node and Wallet.
"""

# General Imports
import json
import os
import random
import subprocess
from base64 import b16encode
from itertools import groupby, chain
from operator import itemgetter
from cerberus import Validator

# Module Imports
from cardanopythonlib.data_utils import load_configs, parse_inputs
from cardanopythonlib.path_utils import create_folder, save_file, remove_file, save_metadata

WORKING_DIR = os.getcwd()
CARDANO_CONFIGS = f'{WORKING_DIR}/config/cardano_config.json'


class Starter():

    """
    Class that initializes the main env variables and paths and it contains
    some generic functions. Here we can place new functions that are inherited to
    the main classes. 

    Attributes
    ----------
    config_path: str, default=CARDANO_CONFIGS
        Configurations for interacting with Cardano node. Default configuration
        follow our node setup, but it is advisable to be modified based on your
        system needs.
    """

    def __init__(self, config_path):
        params = load_configs(config_path, False)
        if params is not None:
            self.CARDANO_NETWORK_MAGIC = params['node']['CARDANO_NETWORK_MAGIC']
            self.CARDANO_CLI_PATH = params['node']['CARDANO_CLI_PATH']
            self.CARDANO_NETWORK = params['node']['CARDANO_NETWORK']
            self.TRANSACTION_PATH_FILE = params['node']['TRANSACTION_PATH_FILE']
            self.KEYS_FILE_PATH = params['node']['KEYS_FILE_PATH']
            self.URL = params['node']['URL']
        else:
            print('Problems loading the cardano_config file')
        if not os.path.exists(self.TRANSACTION_PATH_FILE):
            os.makedirs(self.TRANSACTION_PATH_FILE)
        if not os.path.exists(self.KEYS_FILE_PATH):
            os.makedirs(self.KEYS_FILE_PATH, exist_ok=True)

    def insert_command(self, index, step, command_string, opt_commands):
        """
        Function to insert commands to be executed in subprocess
        """
        i = 0
        for opt_command in opt_commands:
            command_string.insert(index + i, str(opt_command))
            i += step
        return command_string, i

    def execute_command(self, command_string, stdin):
        output = subprocess.run(command_string, stdin=stdin, capture_output=True)
        try:
            if output.returncode != 0:
                raise Exception()
            else:
                rawResult = output.stdout.decode('utf-8')
        except Exception:
            rawResult = output.stderr.decode('utf-8')

        print(rawResult)
        return(rawResult)

    def validate_address(self, address: str) -> bool:
        """
        Empty docstring
        """
        if not address.startswith('addr' or 'DdzFF'):
            print(f"{address} is not a valid addresss")
            return False
        else:
            return True

    def min_utxo_lovelace(self, num_assets, total_asset_name_len, utxoCostPerWord, era):
        ################################################
        # minAda (u) = max (minUTxOValue, (quot (minUTxOValue, adaOnlyUTxOSize)) * (utxoEntrySizeWithoutVal + \
        #               (size B)))

        POLICYIDSize = 28
        utxo_entry_size = 27
        has_datum = False
        num_policies = 1

        byte_len = num_assets * 12 + total_asset_name_len + num_policies * POLICYIDSize
        # print(byte_len)

        b_size = 6 + (byte_len + 7) // 8
        data_hash_size = 10 if has_datum else 0
        finalized_size = utxo_entry_size + b_size + data_hash_size
        minUTxOValue = finalized_size * utxoCostPerWord

        return minUTxOValue
    
    def min_utxo_lovelace1(self, num_assets, total_asset_name_len, utxoCostPerWord, era):

        #///////////////////////////////////////////////////////
        # minAda (u) = max (minUTxOValue, (quot (minUTxOValue, adaOnlyUTxOSize)) * (utxoEntrySizeWithoutVal + (size B)))

        POLICYIDSize = 28
        utxo_entry_size = 27
        has_datum = False
        num_policies = 1

        byte_len = num_assets * 12 + total_asset_name_len + num_policies * POLICYIDSize
        # print(byte_len)

        b_size = 6 + (byte_len + 7) // 8
        

        data_hash_size = 10 if has_datum else 0
        finalized_size = utxo_entry_size + b_size + data_hash_size
        minUTxOValue = finalized_size * utxoCostPerWord

        return minUTxOValue

    @staticmethod
    def cat_files(path, name):
        # Generate master key
        command_string = [
            'cat', path + name
        ]
        output = subprocess.Popen(command_string, stdout=subprocess.PIPE)
        return output


class Node(Starter):
    """
    Class using primarly Cardano CLI commands
    """

    def __init__(self, config_path=CARDANO_CONFIGS):
        super().__init__(config_path=config_path)

    def id_to_address(self, wallet_name):
        """Get payment address stored locally from wallet_name; if address is
        provided, address is returned

        Args:
            wallet_name (string): id wallet generated by cardano wallet API or
            payment address.

        Returns:
            string: payment address associated to wallet_name
        """
        if not wallet_name.startswith('addr' or 'DdzFF'):
            if os.path.exists(self.KEYS_FILE_PATH + '/' + wallet_name):
                with open(self.KEYS_FILE_PATH + '/' + wallet_name + '/' + wallet_name + '.payment.addr', 'r') as file:
                    address = file.readlines(1)[0]
            else:
                address = ''
        else:
            address = wallet_name
        return address

    def get_txid(self):

        print('Executing get transaction ID from Tx.signed file')
        command_string = [
            self.CARDANO_CLI_PATH,
            'transaction', 'txid',
            '--tx-file', self.TRANSACTION_PATH_FILE + '/tx.signed']
        rawResult = self.execute_command(command_string, None)
        return(rawResult)

    def query_protocol(self, saving_path=''):
        """Execute query protocol parameters.

        Args:
            saving_path (str, optional): path where to save the protocol json
            file. Defaults to ''.
        """
        print('Executing query protocol parameters')
        if saving_path == '':
            TRANSACTION_PATH_FILE = self.TRANSACTION_PATH_FILE
        else:
            TRANSACTION_PATH_FILE = saving_path
        protocol_file = TRANSACTION_PATH_FILE + '/protocol.json'
        command_string = [
            self.CARDANO_CLI_PATH,
            'query', 'protocol-parameters',
            '--out-file', protocol_file]
        if self.CARDANO_NETWORK == 'testnet':
            command_string, index = self.insert_command(3,1,command_string,['--testnet-magic',self.CARDANO_NETWORK_MAGIC])
        else:
            command_string, index = self.insert_command(3,1,command_string,['--mainnet'])

        rawResult = self.execute_command(command_string, None)
        if rawResult == '':
            print("Protocol parameters file stored in '%s'" % (protocol_file))
        return(rawResult)

    def query_tip_exec(self):
        """Execute query tip.

        Returns:
            _type_: json with latest epoch, hash, slot, block, era,
                syncProgress
        """
        print('Executing Query Tip')
        command_string = [
            self.CARDANO_CLI_PATH,
            'query', 'tip']
        if self.CARDANO_NETWORK == 'testnet':
            command_string, index = self.insert_command(3,1,command_string,['--testnet-magic',self.CARDANO_NETWORK_MAGIC])
        else:
            command_string, index = self.insert_command(3,1,command_string,['--mainnet'])

        rawResult = self.execute_command(command_string, None)
        rawResult = json.loads(rawResult)
        return rawResult

    def get_transactions(self, wallet_id):
        """Get the list of transactions from the given addresses.
        Args: Cardano Blockchain address or wallet id to search for UTXOs
        Returns:
            _type_: ada_transactions, token_transactions
            ada_transactions: list of transactions with lovelace only
            token_transactions: list of transactions including custom tokens
        """
        print('Executing Get Transactions')
        # wallet_id = utils.parse_inputs(['wallet_id'], args, kwargs)
        address = self.id_to_address(wallet_id)
        command_string = [
            self.CARDANO_CLI_PATH,
            'query', 'utxo',
            '--address', address]
        if self.CARDANO_NETWORK == 'testnet':
            command_string, index = self.insert_command(5,1,command_string,['--testnet-magic',self.CARDANO_NETWORK_MAGIC])
        else:
            command_string, index = self.insert_command(5,1,command_string,['--mainnet'])

        rawResult = self.execute_command(command_string, None)

        # Unpacking the results
        token_transactions = []
        for line in rawResult.splitlines():
            if 'lovelace' in line:
                transaction = {}
                trans = line.split()
                # if only lovelace
                transaction['hash'] = trans[0]
                transaction['id'] = trans[1]
                transaction['amounts'] = []
                tr_amount = {}
                tr_amount['token'] = trans[3]
                tr_amount['amount'] = trans[2]
                transaction['amounts'].append(tr_amount)
                # for each token
                for i in range(0, int((len(trans) - 4) / 3)):
                    tr_amount = {}
                    tr_amount['token'] = trans[3 + i * 3 + 3]
                    tr_amount['amount'] = trans[3 + i * 3 + 2]
                    transaction['amounts'].append(tr_amount)
                token_transactions.append(transaction)
        return token_transactions

    def get_balance(self, wallet_id):
        """Get the balance in dictionary format at the specified wallet
            address or from address base if wallet id is provided

        Args:
            wallet_id (string): id wallet generated by cardano wallet API or
            payment address.

        Returns:
            dict: balance dictionary listing the balance of the assets
            contained in the wallet
        """
        print('Executing Get Balance')
        # wallet.get_addresses(id)
        # wallet_id = utils.parse_inputs(['wallet_id'], args, kwargs)
        wallet_id = self.id_to_address(wallet_id)
        transactions = self.get_transactions(wallet_id)
        balance_dict = {}
        if transactions == {}:
            balance_dict['lovelace'] = 0
            balance_dict['assets'] = 0
        else:
            amounts = []
            for utxo in transactions:
                for amount in utxo['amounts']:
                    amounts.append(amount)
                amounts = sorted(amounts, key=itemgetter('token'))
                for key, value in groupby(amounts, key=itemgetter('token')):
                    balance = 0
                    for k in value:
                        balance = balance + int(k['amount'])
                    balance_dict[key] = balance
                    print(f'Total balance of "{key}" is "{balance}"')
        return balance_dict

    def utxo_selection(self, addr_origin_tx, quantity, deplete, coin_name):
        """ Function based on the coin selection algorithm to properly handle
        the use of utxos in the wallet.
        Rules are:
        1. If any of your UTXO matches the Target it will be used.
        2. If the "sum of all your UTXO smaller than the Target" happens to
        match the Target, they will be used. (This is the case if you sweep
        a complete wallet.)
        3. If the "sum of all your UTXO smaller than the Target" doesn't
        surpass the target, the smallest UTXO greater than your Target will
        be used.
        4. Else Bitcoin Core does 1000 rounds of randomly combining unspent
        transaction outputs until their sum is greater than or equal to the
        Target. If it happens to find an exact match, it stops early and uses
        that.
            Otherwise it finally settles for the minimum of

                the smallest UTXO greater than the Target
                the smallest combination of UTXO it discovered in Step 4.

        Returns:
            _type_: list of utxos to build the transaction
        """
        # Applying the coin selection algorithm
        minCost = 0
        if coin_name == 'lovelace':
            minCost = 1000000
        TxHash = []
        TxHash_lower = []
        amount_lower = []
        TxHash_greater = []
        amount_greater = []
        utxo_found = False
        amount_equal = 0
        if addr_origin_tx:
            for utxo in addr_origin_tx:
                for amount in utxo.get('amounts'):
                    if amount.get('token') == coin_name:
                        if deplete:
                            # TxHash.append('--tx-in')
                            TxHash.append([utxo.get('hash') + '#' + utxo.get('id')])
                            amount_equal += int(amount.get('amount'))
                            utxo_found = True
                            break
                        if int(amount.get('amount')) == quantity + minCost:
                            # TxHash.append('--tx-in')
                            TxHash.append(utxo.get('hash') + '#' + utxo.get('id'))
                            amount_equal = int(amount.get('amount'))
                            utxo_found = True
                            break
                        elif int(amount.get('amount')) < quantity + minCost:
                            TxHash_lower.append(utxo.get('hash') + '#' + utxo.get('id'))
                            amount_lower.append(int(amount.get('amount')))
                        elif int(amount.get('amount')) > quantity + minCost:
                            TxHash_greater.append(utxo.get('hash') + '#' + utxo.get('id'))
                            amount_greater.append(int(amount.get('amount')))

            if not utxo_found:
                if sum(amount_lower) == quantity + minCost:
                    # TxHash.append('--tx-in')
                    TxHash.append(TxHash_lower)
                    amount_equal = sum(amount_lower)
                elif sum(amount_lower) < quantity + minCost:
                    if amount_greater == []:
                        TxHash = []
                        amount_equal = 0
                    amount_equal = min(amount_greater)
                    index = [i for i, j in enumerate(
                        amount_greater) if j == amount_equal][0]
                    # TxHash.append('--tx-in')
                    TxHash.append(TxHash_greater[index])
                else:
                    utxo_array = []
                    amount_array = []
                    for _ in range(999):
                        index_random = random.randint(0, len(addr_origin_tx) - 1)
                        utxo = addr_origin_tx.pop(index_random)
                        # utxo_array.append('--tx-in')
                        utxo_array.append(utxo.get('hash') + '#' + utxo.get('id'))
                        for amount in utxo.get('amounts'):
                            if amount.get('token') == coin_name:
                                amount_array.append(int(amount.get('amount')))
                        if sum(amount_array) >= quantity + minCost:
                            amount_equal = sum(amount_array)
                            break
                    TxHash = utxo_array

            return TxHash, amount_equal
        else:
            return {}, 0

    def tx_min_fee(self, tx_in_count, tx_out_count): # Deprecated, use build_tx_components instead
        """Calculates the expected min fees .
        Args:
            tx_in_count: number of utxo in input
            tx_out_count: number of utxo in output
        Returns:
            Min fees value
        """
        command_string = [
            self.CARDANO_CLI_PATH,
            'transaction', 'calculate-min-fee',
            '--tx-body-file', self.TRANSACTION_PATH_FILE + '/tx.draft',
            '--tx-in-count', tx_in_count,
            '--tx-out-count', tx_out_count,
            '--witness-count', str(1),
            # '--byron-witness-count', str(0),
            '--protocol-params-file', self.TRANSACTION_PATH_FILE + \
            '/protocol.json']
        if self.CARDANO_NETWORK == 'testnet':
            command_string, index = self.insert_command(11,1,command_string,['--testnet-magic',self.CARDANO_NETWORK_MAGIC])
        else:
            command_string, index = self.insert_command(11,1,command_string,['--mainnet'])

        rawResult = self.execute_command(command_string, None)
        rawResult = rawResult.split()
        rawResult = rawResult[0]
        return rawResult

    def sign_witness(self, signing_key_name):

        print('Executing Sign witness')
        path_skey = self.KEYS_FILE_PATH + '/' + signing_key_name + '/' + signing_key_name
        path_bodyfile = self.TRANSACTION_PATH_FILE + '/tx.draft'
        command_string = [
            self.CARDANO_CLI_PATH,
            'transaction', 'witness',
            '--signing-key-file', path_skey + '.payment.skey',
            '--tx-body-file', path_bodyfile,
            '--out-file', path_skey + '.witness'
        ]
        if self.CARDANO_NETWORK == 'testnet':
            command_string, index = self.insert_command(10,1,command_string,['--testnet-magic',self.CARDANO_NETWORK_MAGIC])
        else:
            command_string, index = self.insert_command(10,1,command_string,['--mainnet'])

        rawResult = self.execute_command(command_string, None)
        if rawResult == '':
            rawResult = "Sign witness file stored in '%s'" % (path_skey)
        return(rawResult)

    def create_multisig_script(self, script_name, type, required, hashes):
        print('Executing Creation of script')
        keys_file_path = self.KEYS_FILE_PATH + '/' + script_name
        script_array = []
        if isinstance(hashes, list):
            for hash in hashes:
                script = {
                    "type": "sig",
                    "keyHash": str(hash)
                }
                script_array.append(script)
            multisig_script = {
                "type": str(type),
                "scripts": script_array
            }
            if type != 'all' and 'any':
                if required == '':
                    print("Type different than all or any must have required field specified")
                    return None
                else:
                    multisig_script['required'] = required
            script_file_path = save_metadata(keys_file_path, script_name + '.script', multisig_script)
            print("Script stored in '%s'\n '%s'" % (script_file_path, multisig_script))
        else:
            multisig_script = None
            print("Check if the hash is a passed as a list type")
        return multisig_script

    def create_policy_id(self, script_name):
        """_summary_
         Args:
            wallet_id: id generated by cardano wallet API or payment address.

        Returns:
            _type_: policyID, policy_script
        """
        print('Executing Creation of Minting Policy ID')
        keys_file_path = self.KEYS_FILE_PATH + '/' + script_name
        if not os.path.exists(keys_file_path):
            os.makedirs(keys_file_path)
        # Generate policyID from the policy script file
        command_string = [
            self.CARDANO_CLI_PATH, 'transaction', 'policyid', '--script-file',
            keys_file_path + '/' + script_name + '.script'
        ]
        rawResult = self.execute_command(command_string, None)
        policyID = str(rawResult).rstrip()
        save_file(keys_file_path + '/', script_name + '.policyid', str(policyID))

        return policyID

    def sign_transaction(self, *args):
        """Sign the transaction based on tx_raw file.
        """
        command_string = [
            self.CARDANO_CLI_PATH,
            'transaction', 'sign',
            '--tx-body-file', self.TRANSACTION_PATH_FILE + '/tx.draft',
            # '--signing-key-file', self.KEYS_FILE_PATH + '/' + sign_address_name + '/' + sign_address_name + '.payment.skey', 
            '--out-file', self.TRANSACTION_PATH_FILE + '/tx.signed']
        index = 5
        for arg in args:
            command_string, index = self.insert_command(index,1,command_string,['--signing-key-file', self.KEYS_FILE_PATH + '/' + arg + '/' + arg + '.payment.skey'])
        if self.CARDANO_NETWORK == 'testnet':
            command_string, index = self.insert_command(index + 5,1,command_string,['--testnet-magic',self.CARDANO_NETWORK_MAGIC])
        else:
            command_string, index = self.insert_command(index + 5,1,command_string,['--mainnet'])

        rawResult = self.execute_command(command_string, None)
        if rawResult == '':
            rawResult = "Sign transaction file stored in '%s'" % (self.TRANSACTION_PATH_FILE + '/tx.signed')
            print(rawResult)
        return(rawResult)

    def submit_transaction(self):
        """Submit the transaction"""
        command_string = [
            self.CARDANO_CLI_PATH,
            'transaction', 'submit',
            '--tx-file', self.TRANSACTION_PATH_FILE + '/tx.signed']
        if self.CARDANO_NETWORK == 'testnet':
            command_string, index = self.insert_command(5,1,command_string,['--testnet-magic',self.CARDANO_NETWORK_MAGIC])
        else:
            command_string, index = self.insert_command(5,1,command_string,['--mainnet'])

        rawResult = self.execute_command(command_string, None)
        print(rawResult)
        return(rawResult)

    def build_tx_components(self, params):

        print('Building the transaction')
        params = params.get('message').get('tx_info')
        schema = {
                'address_origin': {
                    'type': 'string',
                    'required': True,
                },
                'address_destin': {
                    'type': 'list',
                    'nullable': True,
                    'schema':{ 'type': 'dict', 'schema':{
                        'address': {'type': 'string', 'required': True},
                        'amount': {'type': 'dict', 'required': True, 'schema': {'quantity': {'type': 'integer', 'required': True}, 'unit': {'type': 'string', 'allowed': ['lovelace', 'ada']}}},
                        'assets': {'type': 'list', 'nullable': True, 
                            'schema': {'type': 'dict', 'schema':{'asset_name': {'type': 'string', 'required': True}, 'amount': {'type': 'integer', 'required': True}, 'policyID': {'type': 'string', 'required': True}}}}
                }}},
                'change_address': {
                    'type': 'string',
                    'required': True,
                },
                'metadata': {
                    'type': 'dict',
                    'nullable': True,
                },
                'mint': {
                    'type': 'dict',
                    'nullable': True,
                    'schema': {
                    'policyID': {'type': 'string', 'required': True},
                    'policy_path': {'type': 'string', 'required': True},
                    "tokens": {'type': 'list', 'schema':{ 'type': 'dict',
                        'schema':{
                        'name': {'type': 'string', 'required': True},
                        'amount': {'type': 'integer', 'required': True},
                        }
                        }
                    }}
                },
                'script_path': {
                    'type': 'string',
                    'nullable': True,
                },
                'witness': {
                    'type': 'integer',
                    'required': True,
                },
        }
        v = Validator()
        try:
            assert v.validate(params, schema)  # type: ignore
            # Unpacking the minimum required arguments
            address_origin = params.get('address_origin')
            change_address = params.get('change_address')

            # Unpacking optional arguments
            address_destin_array = params.get('address_destin')
            metadata = params.get('metadata')
            mint = params.get('mint')
            script_path = params.get('script_path')
            witness = params.get('witness')

            # Validate address
            address_origin = self.id_to_address(address_origin)
            change_address = self.id_to_address(change_address)

            self.query_protocol()
            with open(self.TRANSACTION_PATH_FILE + '/protocol.json', 'r') as file:
                utxoCostPerWord = json.load(file).get('utxoCostPerWord')
            # min_utxo_value = self.min_utxo_lovelace1(0, 0, utxoCostPerWord, '')
            # quantity_array = [min_utxo_value]

            addr_origin_balance = self.get_balance(address_origin)
            addr_origin_tx = self.get_transactions(address_origin)
            if addr_origin_balance.get('lovelace') is not None:
            # if addr_origin_balance['lovelace'] != 0:
            # if addr_origin_tx != {}:
                # addr_origin_tx = self.get_transactions(address_origin)
                mint_output_string = ''
                addr_output_array = []
                mint_quantity_array = []
                quantity_array = []
                # mint_string = ''
                mint_array = []
                total_mint_name_len = 0
                length_mint = 0
                if mint is not None:
                    length_mint = len(mint.get('tokens'))
                    policyid = mint.get('policyID')
                    policy_path = mint.get('policy_path')
                    for token in mint.get('tokens'):
                        mint_name = token.get('name').encode('utf-8')
                        mint_name = b16encode(mint_name).decode('utf-8')
                        mint_quantity = token.get('amount')
                        mint_quantity_array.append(mint_quantity)
                        total_mint_name_len += len(mint_name)
                        mint_output_string += str(mint_quantity) + ' ' + \
                                str(policyid) + '.' + str(mint_name) + '+'

                    mint_output_string = mint_output_string[:-1]
                    mint_string = '--mint='
                    mint_string = mint_string + mint_output_string
                    mint_output_string = '+' + mint_output_string
                    # min_utxo_value = self.min_utxo_lovelace1(
                    #     len(mint.get('tokens')), total_asset_name_len, utxoCostPerWord, '')
                    # addr_output_array.append('--tx-out')
                    # addr_output_array.append(address_origin + '+' + str(min_utxo_value) + '+' + mint_output_string)

                    # quantity_array = [min_utxo_value]
                    mint_array.append(mint_string)
                    mint_array.append('--minting-script-file')
                    mint_array.append(policy_path)

                length_assets = 0
                total_asset_name_len = 0
                asset_output_string = ''
                TxHash_in_asset = []
                if address_destin_array is not None:
                    for address_destin in address_destin_array:
                        amount = address_destin.get('amount')
                        quantity = amount.get('quantity')
                        if amount.get('unit') == 'ada':
                            quantity = quantity * 1_000_000
                        if address_destin.get('assets') is not None:
                            length_assets = len(address_destin.get('assets'))
                            # addr_output_array.append('--tx-out')
                            # address_full_string = address_destin.get('address') + '+' + str(quantity)
                            for asset in address_destin.get('assets'):
                                asset_name = asset.get('asset_name').encode('utf-8')
                                asset_name = b16encode(asset_name).decode('utf-8')
                                asset_name = asset_name.lower()
                                total_asset_name_len += len(asset_name)
                                amount = asset.get('amount')
                                policyID = asset.get('policyID')
                                asset_full_name = policyID + '.' + asset_name
                                if asset_full_name in addr_origin_balance:
                                    asset_balance = addr_origin_balance.get(asset_full_name)
                                    if amount <= asset_balance:
                                        TxHash_in, amount_equal = self.utxo_selection(
                                            addr_origin_tx, amount, False, asset_full_name)
                                        asset_output_string += str(amount) + ' ' + asset_full_name + '+'
                                        TxHash_in_asset += TxHash_in
                                        # mint_output_string += str(amount) + '+' + 
                                    else:
                                        raise Exception()
                                else:
                                    print(f"{asset_full_name} could not be found in wallet origin")
                                    raise Exception()
                            asset_output_string = asset_output_string[:-1]
                            min_utxo_value = self.min_utxo_lovelace1(
                                length_mint + length_assets, total_mint_name_len + total_asset_name_len, utxoCostPerWord, '')
                            if quantity >= min_utxo_value:
                                quantity_array.append(quantity)
                                addr_output_array.append('--tx-out')
                                addr_output_array.append(address_destin.get('address') + '+' + str(quantity) + '+' + asset_output_string + mint_output_string)
                            else:
                                print(f"Quantity to send less than min_utxo_value of: {min_utxo_value}")
                                raise Exception()
                        else:
                            min_utxo_value = self.min_utxo_lovelace1(
                             length_mint + length_assets, total_mint_name_len + total_asset_name_len, utxoCostPerWord, '')
                            if quantity >= min_utxo_value:
                                quantity_array.append(quantity)
                                addr_output_array.append('--tx-out')
                                addr_output_array.append(address_destin.get('address') + '+' + str(quantity) + mint_output_string)
                            else:
                                print(f"Quantity to send less than min_utxo_value of: {min_utxo_value}")
                                raise Exception()
                            # addr_output_array.append('--tx-out')
                            # addr_output_array.append(address_origin + '+' + str(min_utxo_value) + '+' + mint_output_string)
                        # addr_output_array.append(address_full_string)
                else:
                    min_utxo_value = self.min_utxo_lovelace1(
                        length_mint + length_assets, total_mint_name_len + total_asset_name_len, utxoCostPerWord, '')
                    addr_output_array.append('--tx-out')
                    addr_output_array.append(address_origin + '+' + str(min_utxo_value) + mint_output_string)

                addr_output_array.append('--change-address')
                addr_output_array.append(change_address)

                target_calculated = sum(quantity_array)
                deplete = False
                TxHash_in, amount_equal = self.utxo_selection(
                    addr_origin_tx, target_calculated, deplete, 'lovelace')
                TxHash_in = TxHash_in + TxHash_in_asset
                TxHash_in = list(set(TxHash_in)) # remove utxo duplicates
                tx_in = len(TxHash_in) * ['--tx-in']
                TxHash_in = list(chain(*zip(tx_in, TxHash_in))) # Intercalate elements

                command_string = [
                    self.CARDANO_CLI_PATH,
                    'transaction', 'build',
                    '--witness-override', str(witness),
                    '--out-file', self.TRANSACTION_PATH_FILE + '/tx.draft']
                i = 0
                command_string, index = self.insert_command(
                    3 + i, 1, command_string, TxHash_in
                )
                i = i + index
                command_string, index = self.insert_command(
                    3 + i, 1, command_string, addr_output_array
                )
                i = i + index
                metadata_array = []
                if metadata is not None:
                    metadata_json_file = save_metadata(
                        self.TRANSACTION_PATH_FILE, 'tx_metadata.json', metadata)
                    metadata_array.append('--metadata-json-file')
                    metadata_array.append(metadata_json_file)
                    command_string, index = self.insert_command(
                        3 + i, 1, command_string, metadata_array
                    )
                    i = i + index
                if mint_array != []:
                    command_string, index = self.insert_command(3 + i, 1, command_string, mint_array)
                    i = i + index
                script_path_array = []
                if script_path is not None:
                    script_path_array.append('--tx-in-script-file')
                    script_path_array.append(script_path)
                    command_string, index = self.insert_command(
                        3 + i, 1, command_string, script_path_array
                    )
                    i = i + index
                if self.CARDANO_NETWORK == 'testnet':
                    command_string, index = self.insert_command(3 + i,1,command_string,['--testnet-magic',self.CARDANO_NETWORK_MAGIC])
                else:
                    command_string, index = self.insert_command(3 + i,1,command_string,['--mainnet'])

                print(command_string)
                rawResult = self.execute_command(command_string, None)

            else:
                rawResult = 'Not utxos found in the address provided'
                print(rawResult)

            print("################################")
            return rawResult
        except TypeError:
            print("Missing required arguments")
        except AssertionError:
            print(f"Errors in the message dictionary format. Check {v.errors}")  # type: ignore
        except Exception:
            print(f"Errors while building the transaction. Probably insufficient ada or native asset funds")

    def analyze_tx(self, tx_name_file):
        print('Analyzing the transaction....')
        command_string = [
            self.CARDANO_CLI_PATH,
            'transaction', 'view',
            '--tx-body-file', self.TRANSACTION_PATH_FILE + '/' + tx_name_file]

        rawResult = self.execute_command(command_string, None)
        print(rawResult)
        return rawResult

    def assemble_tx(self, witness_wallet_name_array):
        print('Executing Assemble witness')

        witness_output_array = []
        for witness_key_name in witness_wallet_name_array:

            witness_output_array.append('--witness-file')
            witness_output_array.append(self.KEYS_FILE_PATH + '/' + witness_key_name +
                                        '/' + witness_key_name + '.witness')

        path_bodyfile = self.TRANSACTION_PATH_FILE + '/tx.draft'

        command_string = [
            self.CARDANO_CLI_PATH,
            'transaction', 'assemble',
            '--tx-body-file', path_bodyfile,
            '--out-file', self.TRANSACTION_PATH_FILE + '/tx.signed'
        ]

        i = 0
        command_string, index = self.insert_command(
            5 + i, 1, command_string, witness_output_array
        )

        rawResult = self.execute_command(command_string, None)
        if rawResult == '':
            tx_signed_path = self.TRANSACTION_PATH_FILE
            name = 'tx.signed'
            rawResult = "Transaction signed file stored in '%s' with the name '%s'" % (tx_signed_path, name)

        return(rawResult)

class Keys(Starter):
    def __init__(self, config_path=CARDANO_CONFIGS):
        super().__init__(config_path=config_path)
        self.path = self.KEYS_FILE_PATH
        self.cardano_network = self.CARDANO_NETWORK
        self.cardano_network_magic = self.CARDANO_NETWORK_MAGIC

    def generate_mnemonic(self, size=24, *args, **kwargs):
        """Create mnemonic sentence (list of mnemonic words)
        Input: size number of words: 24 by default"""
        print('Executing Generate New Mnemonic Phrase')
        # Generate mnemonic
        command_string = [
            'cardano-wallet', 'recovery-phrase', 'generate',
            '--size', str(size)
        ]
        rawResult = self.execute_command(command_string, None)
        mnemonic = rawResult.split()
        print("Mnemonics are '%s'" % (mnemonic))
        return mnemonic

    def deriveRootKey(self, mnemonic):
        """Generate root key
            When folder empty, root key is not save locally in a file
        Args:
            mnemonic ([list]): [Phrases passed as array]
        Returns:
            [str]: [Root private key]
        """
        # Save temp mnemonic
        content = ' '.join(mnemonic)
        save_file(self.path, '/temp_mnemonic', content)

        # Generate master key
        output = self.cat_files(self.path, '/temp_mnemonic')
        command_string = [
            'cardano-address', 'key', 'from-recovery-phrase', 'Shelley'
        ]
        rawResult = self.execute_command(command_string, output.stdout)

        # Delete file mnemonic
        print("Root private key: '%s'" % (rawResult))
        remove_file(self.path, '/temp_mnemonic')
        return rawResult

    def deriveExtendedSigningStakeKey(self, root_key):
        """AI is creating summary for deriveExtendedSigningStakeKey

        Args:
            root_key ([str]): [Root private key]

        Returns:
            [str]: [extended stake signing key xsk]
        """
        # Save temp root_key
        save_file(self.path, '/temp_root.xsk', str(root_key))

        output = self.cat_files(self.path, '/temp_root.xsk')
        # Generate extended stake signing key
        command_string = [
            'cardano-address', 'key', 'child', '1852H/1815H/0H/2/0'
        ]
        rawResult = self.execute_command(command_string, output.stdout)

        print("Stake extended signing key: '%s'" % (rawResult))
        # Delete file root key
        remove_file(self.path, '/temp_root.xsk')
        return rawResult

    def deriveExtendedSigningPaymentKey(self, root_key):
        """AI is creating summary for deriveExtendedSigningPaymentKey

        Args:
            root_key ([str]): [Root private key]

        Returns:
            [str]: [extended payment signing key xsk]
        """
        # Save temp root_key
        save_file(self.path, '/temp_root.xsk', str(root_key))

        output = self.cat_files(self.path, '/temp_root.xsk')
        # Generate extended Payment signing key
        command_string = [
            'cardano-address', 'key', 'child', '1852H/1815H/0H/0/0'
        ]
        rawResult = self.execute_command(command_string, output.stdout)

        print("Payment extended signing key: '%s'" % (rawResult))
        # Delete file root key
        remove_file(self.path, '/temp_root.xsk')
        return rawResult

    def deriveExtendedVerificationPaymentKey(self, payment_signing_key):
        """AI is creating summary for deriveExtendedVerificationPaymentKey

        Args:
            payment_signing_key [str]: [extended payment signing key xsk]

        Returns:
            [str]: [extended payment verification key xvk]
        """
        # Save temp root_key
        save_file(
            self.path, '/temp_payment.xsk', str(payment_signing_key)
        )

        output = self.cat_files(self.path, '/temp_payment.xsk')
        # Generate extended public account key xpub
        command_string = [
            'cardano-address', 'key', 'public', '--with-chain-code'
        ]
        rawResult = self.execute_command(command_string, output.stdout)

        print("Payment extended verification key: '%s'" % (rawResult))
        # Delete file root key
        remove_file(self.path, '/temp_payment.xsk')
        return rawResult

    def deriveExtendedVerificationStakeKey(self, stake_signing_key):
        """AI is creating summary for deriveExtendedVerificationStakeKey

        Args:
            stake_signing_key [str]: [extended stake signing key xsk]

        Returns:
            [str]: [extended stake verification key xvk]
        """
        # Save temp root_key
        save_file(
            self.path, '/temp_stake.xsk', str(stake_signing_key)
        )

        output = self.cat_files(self.path, '/temp_stake.xsk')
        # Generate extended public account key xpub
        command_string = [
            'cardano-address', 'key', 'public', '--with-chain-code'
        ]
        rawResult = self.execute_command(command_string, output.stdout)
        print("Stake extended verification key: '%s'" % (rawResult))
        # Delete file root key
        remove_file(self.path, '/temp_stake.xsk')
        return rawResult

    def derivePaymentAddress(self, payment_verification_key):
        """AI is creating summary for derivePaymentAddress
        Args:
            payment_verification_key ([str]):
            [extended payment verification key xvk]

        Returns:
            [str]: [payment public address]
        """
        # Save temp root_key
        save_file(self.path, '/temp_payment.xvk', str(payment_verification_key))

        output = self.cat_files(self.path, '/temp_payment.xvk')
        # Generate extended public account key xpub
        command_string = [
            'cardano-address', 'address', 'payment', '--network-tag',
            self.cardano_network
        ]
        rawResult = self.execute_command(command_string, output.stdout)

        print("Payment extended address: '%s'" % (rawResult))
        # Delete file root key
        remove_file(self.path, '/temp_payment.xvk')
        return rawResult

    def convertPaymentKey(self, payment_signing_key, name):
        """This function converts the cardano wallet payment keys to
        cardano-cli payment keys


        Args:
            payment_signing_key ([str]): [extended payment signing key xsk]

        Returns:
            [str]: [payment_skey, payment_vkey, payment_addr]
        """
        # Save temp root_key
        save_file(self.path, '/temp_payment.xsk', str(payment_signing_key))

        # Generate extended public account key xpub
        command_string = [
            self.CARDANO_CLI_PATH, 'key', 'convert-cardano-address-key',
            '--shelley-payment-key', '--signing-key-file',
            self.path + '/temp_payment.xsk',
            '--out-file',
            self.path + '/' + name + '/' + name + '.payment.skey']

        self.execute_command(command_string, None)
        # if rawResult == '':
        #     print("Generate extended public account key xpub: '%s'" % (self.path + '/' + name + '/' + name + \
        #           '.payment.skey'))

        output = self.cat_files(
            self.path, '/' + name + '/' + name + '.payment.skey'
        )
        payment_skey = output.communicate()[0].decode('utf-8')
        # output.stdout.close()

        # Get verification payment key from signing payment key.
        command_string = [
            self.CARDANO_CLI_PATH, 'key', 'verification-key', '--signing-key-file',
            self.path + '/' + name + '/' + name + '.payment.skey',
            '--verification-key-file',
            self.path + '/' + name + '/' + name + '.payment.evkey'
        ]
        self.execute_command(command_string, None)
        # if rawResult == '':
        #     print("Get verification payment key from signing payment key: '%s'" % (self.path + '/' + name + '/' \
        #               + name + '.payment.evkey'))

        # Get non-extended verification payment key
        # from extended verification payment key.
        command_string = [
            self.CARDANO_CLI_PATH, 'key', 'non-extended-key',
            '--extended-verification-key-file',
            self.path + '/' + name + '/' + name + '.payment.evkey',
            '--verification-key-file',
            self.path + '/' + name + '/' + name + '.payment.vkey'
        ]
        self.execute_command(command_string, None)
        # if rawResult == '':
        #     print("Get non-extended verification payment key: '%s'" % (self.path + '/' + name + '/' + name + \
        #               '.payment.vkey'))

        output = self.cat_files(self.path, '/' + name + '/' + name + '.payment.vkey')
        payment_vkey = output.communicate()[0].decode('utf-8')
        # output.stdout.close()

        # Build payment addresses
        command_string = [
            self.CARDANO_CLI_PATH, 'address', 'build',
            '--payment-verification-key-file',
            self.path + '/' + name + '/' + name + '.payment.vkey',
            '--out-file', self.path + '/' + name + '/' + name + '.payment.addr'
        ]
        if self.CARDANO_NETWORK == 'testnet':
            command_string, index = self.insert_command(5,1,command_string,['--testnet-magic',self.CARDANO_NETWORK_MAGIC])
        else:
            command_string, index = self.insert_command(5,1,command_string,['--mainnet'])
        self.execute_command(command_string, None)

        output = self.cat_files(
            self.path, '/' + name + '/' + name + '.payment.addr'
        )
        payment_addr = output.communicate()[0].decode('utf-8')
        # output.stdout.close()

        print("Payment signing key: '%s' \n Payment verification key: '%s' \n Payment address: '%s" %
              (payment_skey, payment_vkey, payment_addr))
        # Delete files
        remove_file(self.path, '/temp_payment.xsk')

        return payment_skey, payment_vkey, payment_addr

    def convertStakeSigningKey(self, stake_signing_key, name):
        """This function converts the cardano wallet stake keys to
        cardano-cli stake keys


        Args:
            stake_signing_key ([str]): [extended stake signing key xsk]

        Returns:
            [str]: [stake_skey, stake_vkey, stake_addr]
        """
        # Save temp root_key
        save_file(
            self.path, '/temp_stake.xsk', str(stake_signing_key)
        )

        # Generate extended public account key xpub
        command_string = [
            self.CARDANO_CLI_PATH, 'key', 'convert-cardano-address-key',
            '--shelley-stake-key', '--signing-key-file',
            self.path + '/temp_stake.xsk',
            '--out-file',
            self.path + '/' + name + '/' + name + '.stake.skey']
        self.execute_command(command_string, None)
        output = self.cat_files(
            self.path, '/' + name + '/' + name + '.stake.skey'
        )
        stake_skey = output.communicate()[0].decode('utf-8')
        # output.stdout.close()
        # Get verification stake key from signing stake key.
        command_string = [
            self.CARDANO_CLI_PATH, 'key', 'verification-key', '--signing-key-file',
            self.path + '/' + name + '/' + name + '.stake.skey',
            '--verification-key-file',
            self.path + '/' + name + '/' + name + '.stake.evkey'
        ]
        self.execute_command(command_string, None)

        # Get non-extended verification stake key
        # from extended verification stake key.
        command_string = [
            self.CARDANO_CLI_PATH, 'key', 'non-extended-key',
            '--extended-verification-key-file',
            self.path + '/' + name + '/' + name + '.stake.evkey',
            '--verification-key-file',
            self.path + '/' + name + '/' + name + '.stake.vkey'
        ]
        self.execute_command(command_string, None)
        output = self.cat_files(
            self.path, '/' + name + '/' + name + '.stake.vkey'
        )
        stake_vkey = output.communicate()[0].decode('utf-8')
        # output.stdout.close()

        # Build stake addresses
        command_string = [
            self.CARDANO_CLI_PATH, 'stake-address', 'build',
            '--stake-verification-key-file',
            self.path + '/' + name + '/' + name + '.stake.vkey',
            '--out-file',
            self.path + '/' + name + '/' + name + '.stake.addr'
        ]
        if self.CARDANO_NETWORK == 'testnet':
            command_string, index = self.insert_command(5,1,command_string,['--testnet-magic',self.CARDANO_NETWORK_MAGIC])
        else:
            command_string, index = self.insert_command(5,1,command_string,['--mainnet'])
        self.execute_command(command_string, None)
        output = self.cat_files(
            self.path, '/' + name + '/' + name + '.stake.addr'
        )
        stake_addr = output.communicate()[0].decode('utf-8')
        print("Stake signing key: '%s' \n Stake verification key: '%s' \n Stake address: '%s" %
              (stake_skey, stake_vkey, stake_addr))
        # Delete file
        remove_file(self.path, '/temp_stake.xsk')

        # output.stdout.close()

        return stake_skey, stake_vkey, stake_addr

    def deriveBaseAddress(self, name):
        """Derive the base address Cardano cli command

        Args:
        payment_vkey ([str]): [Payment verification key]
        stake_vkey ([str]): [Payment verification key]

        Returns:
            [str]: [Combined base address]
        """
        # Build base addresses
        command_string = [
            self.CARDANO_CLI_PATH, 'address', 'build',
            '--payment-verification-key-file',
            self.path + '/' + name + '/' + name + '.payment.vkey',
            '--stake-verification-key-file',
            self.path + '/' + name + '/' + name + '.stake.vkey',
            '--out-file',
            self.path + '/' + name + '/' + name + '.base.addr'
        ]
        if self.CARDANO_NETWORK == 'testnet':
            command_string, index = self.insert_command(7,1,command_string,['--testnet-magic',self.CARDANO_NETWORK_MAGIC])
        else:
            command_string, index = self.insert_command(7,1,command_string,['--mainnet'])
        self.execute_command(command_string, None)
        output = self.cat_files(
            self.path, '/' + name + '/' + name + '.base.addr'
        )
        base_addr = output.communicate()[0].decode('utf-8')
        # output.stdout.close()
        remove_file(self.path, '/temp_payment.vkey')
        remove_file(self.path, '/temp_stake.vkey')
        print("Base address: '%s'" % (base_addr))
        return base_addr

    def keyHashing(self, name):
        keys_file_path = self.path + '/' + name
        # Build hash from key
        command_string = [
            self.CARDANO_CLI_PATH, 'address', 'key-hash',
            '--payment-verification-key-file',
            keys_file_path + '/' + name + '.payment.vkey'
        ]

        rawResult = self.execute_command(command_string, None)
        key_hash = str(rawResult.rstrip())
        print("Key hash of the verification payment key: '%s'" % (key_hash))
        return key_hash

    def deriveAllKeys(self, name, **kwargs):
        """This function creates all the keys and addresses and save them
        in root_folder/priv/wallet/walletname path


        Args:
            size ([int]): [phrase extension: 24, 15, etc]
            name ([str]): [name of the wallet to save the keys]
        """
        if not os.path.exists(self.path + '/' + name):
            os.makedirs(self.path + '/' + name)
        size = kwargs.get('size')
        if size == None:
            nmemonic = kwargs.get('words')
        else:
            nmemonic = self.generate_mnemonic(size)
        root_key = self.deriveRootKey(nmemonic)
        stake = self.deriveExtendedSigningStakeKey(root_key)
        payment = self.deriveExtendedSigningPaymentKey(root_key)

        payment_public_account_key = self.deriveExtendedVerificationPaymentKey(
            payment)
        stake_public_account_key = self.deriveExtendedVerificationStakeKey(
            stake)

        payment_address = self.derivePaymentAddress(payment_public_account_key)
        # Convert from cardano wallet keys to cardano-cli keys
        """
        Convert payment signing keys
        """
        payment_skey, payment_vkey, payment_addr = self.convertPaymentKey(
            payment, name)
        """
        Convert stake signing keys
        """
        stake_skey, stake_vkey, stake_addr = self.convertStakeSigningKey(stake, name)
        base_addr = self.deriveBaseAddress(name)

        # Hashing the verification keys
        hash_verification_key = self.keyHashing(name)

        # Building the paths
        payment_skey_path = self.path + '/' + name + '/' + name \
            + '.payment.skey'
        payment_vkey_path = self.path + '/' + name + '/' + name \
            + '.payment.vkey'
        payment_addr_path = self.path + '/' + name + '/' + name \
            + '.payment.addr'
        stake_skey_path = self.path + '/' + name + '/' + name \
            + '.stake.skey'
        stake_vkey_path = self.path + '/' + name + '/' + name \
            + '.stake.vkey'
        stake_addr_path = self.path + '/' + name + '/' + name + '.stake.addr'

        # Creating the dict
        keys = {
            'mnemonic': nmemonic,
            'root_key': root_key,
            'private_stake_key': stake,
            'private_payment_key': payment,
            'payment_account_key': payment_public_account_key,
            'stake_account_key': stake_public_account_key,
            'payment_addr': payment_address,
            'payment_addr_path': payment_addr_path,
            'payment_skey_path': payment_skey_path,
            'payment_vkey_path': payment_vkey_path,
            'stake_skey_path': stake_skey_path,
            'stake_vkey_path': stake_vkey_path,
            'stake_addr_path': stake_addr_path,
            'base_addr_path': base_addr,
            'hash_verification_key': hash_verification_key,
        }

        with open(self.path + '/' + name + '/' + name + '.json', 'w') as file:
            json.dump(keys, file, indent=4, ensure_ascii=False)

        print("##################################")
        print("Find all the keys and address details in: %s" %
              (self.path + '/' + name + '/' + name + '.json'))
        print("##################################")
        return keys

    def generateCardanoKeys(self, name):
        keys_file_path = self.path + '/' + name
        create_folder(keys_file_path)
        # Build Cardano keys with Cardano CLI
        command_string = [
            self.CARDANO_CLI_PATH, 'address', 'key-gen',
            '--verification-key-file',
            keys_file_path + '/' + name + '.payment.vkey',
            '--signing-key-file',
            keys_file_path + '/' + name + '.payment.skey'
        ]

        rawResult = self.execute_command(command_string, None)

        command_string = [
            self.CARDANO_CLI_PATH, 'stake-address', 'key-gen',
            '--verification-key-file',
            keys_file_path + '/' + name + '.stake.vkey',
            '--signing-key-file',
            keys_file_path + '/' + name + '.stake.skey'
        ]

        rawResult = self.execute_command(command_string, None)
        if rawResult == '':
            rawResult = "Keys stored in '%s' under the name '%s'" % (keys_file_path, name)
        return(rawResult)

    def create_address_script(self, script_name):
        keys_file_path = self.path + '/' + script_name
        # Build script addresses
        command_string = [
            self.CARDANO_CLI_PATH, 'address', 'build',
            '--payment-script-file',
            keys_file_path + '/' + script_name + '.script',
            '--out-file',
            keys_file_path + '/' + script_name + '.script.addr'
        ]
        if self.CARDANO_NETWORK == 'testnet':
            command_string, index = self.insert_command(5,1,command_string,['--testnet-magic',self.CARDANO_NETWORK_MAGIC])
        else:
            command_string, index = self.insert_command(5,1,command_string,['--mainnet'])
        self.execute_command(command_string, None)
        print("Script address stored in '%s'" % (keys_file_path))
