"""
This submodule defines the class Starter. It is the base class of the other classes
objects: Starter
"""

# General Imports
import json
import os
import subprocess
import sys
from base64 import b16encode
from itertools import groupby
from operator import itemgetter
from typing import Tuple, Any
from dataclasses import dataclass


# Module Imports
WORKING_DIR = os.path.dirname(__file__)
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "cardanopythonlib"))
from data_utils import getlogger
from path_utils import (
    config,
    create_folder
)

CARDANO_CONFIGS = f"{WORKING_DIR}/config/cardano_config.ini"



@dataclass
class Starter:

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
    config_path=CARDANO_CONFIGS
    params = config(config_path, section="node")
    if params is not None:
        # Initializing variables
        CARDANO_NETWORK_MAGIC = params.get("cardano_network_magic")
        CARDANO_CLI_PATH = params.get("cardano_cli_path")
        CARDANO_NETWORK = params.get("cardano_network")
        CARDANO_ERA = params.get("cardano_era")
        TRANSACTION_PATH_FILE = str(params.get("transaction_path_file"))
        KEYS_FILE_PATH = str(params.get("keys_file_path"))
        SCRIPTS_FILE_PATH = str(params.get("scripts_file_path"))
        URL = params.get("url")
        PLUTUS_FOLDER = SCRIPTS_FILE_PATH + "/plutus"
        MINT_FOLDER = SCRIPTS_FILE_PATH + "/mint"
        MULTISIG_FOLDER = SCRIPTS_FILE_PATH + "/multisig"

        # Setting up the logger level
        params = config(config_path, section="logger")
        LOGGER = getlogger(__name__, params.get("level"))

        if not os.path.exists(TRANSACTION_PATH_FILE):
            os.makedirs(TRANSACTION_PATH_FILE)
            LOGGER.debug(
                f"Creation of the transaction folder in: {TRANSACTION_PATH_FILE}"
            )
        if not os.path.exists(KEYS_FILE_PATH):
            os.makedirs(KEYS_FILE_PATH, exist_ok=True)
            LOGGER.debug(
                f"Creation of the keys folder in: {KEYS_FILE_PATH}"
            )
        if not os.path.exists(SCRIPTS_FILE_PATH):
            os.makedirs(SCRIPTS_FILE_PATH, exist_ok=True)

            create_folder(
                [PLUTUS_FOLDER, MINT_FOLDER, MULTISIG_FOLDER]
            )
            LOGGER.debug(
                f"Creation of the scripts folder in: {SCRIPTS_FILE_PATH} and subfolders: {PLUTUS_FOLDER}, {MINT_FOLDER} and {MULTISIG_FOLDER}"
            )
        if CARDANO_NETWORK == "testnet":
            LOGGER.debug(
                f"Working on CARDANO_NETWORK: {CARDANO_NETWORK} with CARDANO_NETWORK_MAGIC: {CARDANO_NETWORK_MAGIC}"
            )
        else:
            LOGGER.debug(f"Working on CARDANO_NETWORK: {CARDANO_NETWORK}")
        LOGGER.debug(
            f"If you are using cardano-wallet, this is the default internal url: {URL}"
        )
    else:
        print("Problems loading the cardano_config file")

    def insert_command(self, index: int, step: int, command_string, opt_commands: Any) -> Tuple[list[str], int]: 
        """
        Function to insert commands to be executed in subprocess
        """
        i = 0
        for opt_command in opt_commands:
            command_string.insert(index + i, str(opt_command))
            i += step
        return command_string, i

    def execute_command(self, command_string: list[str], stdin) -> str:
        output = subprocess.run(command_string, stdin=stdin, capture_output=True)
        try:
            if output.returncode != 0:
                raise Exception()
            else:
                rawResult = output.stdout.decode("utf-8")
        except Exception:
            rawResult = output.stderr.decode("utf-8")

        return rawResult

    def validate_address(self, address: str) -> bool:
        """
        Empty docstring
        """
        if not address.startswith("addr" or "DdzFF"):
            self.LOGGER.warning(f"{address} is not a valid addresss")
            return False
        else:
            return True

    def query_protocol(self, save_flag: bool = False) -> dict:
        """Execute query protocol parameters.

        Args:
            saving_path (str, optional): path where to save the protocol json
            file. Defaults to ''.
        """
        print("Executing query protocol parameters")
        protocol_file = self.TRANSACTION_PATH_FILE + "/protocol.json"
        command_string = [self.CARDANO_CLI_PATH, "query", "protocol-parameters"]
        if self.CARDANO_NETWORK == "testnet":
            command_string, index = self.insert_command(
                3, 1, command_string, ["--testnet-magic", self.CARDANO_NETWORK_MAGIC]
            )
        else:
            command_string, index = self.insert_command(
                3, 1, command_string, ["--mainnet"]
            )

        rawResult = self.execute_command(command_string, None)
        rawResult = json.loads(rawResult)
        if save_flag:
            with open(protocol_file, "w") as file:
                json.dump(rawResult, file, indent=4, ensure_ascii=False)
                self.LOGGER.info(f"Protocol parameters file stored in {protocol_file}")
        return rawResult


    def min_required_utxo(self, tx_out_address: str, tx_out_tokens: str = "", *reference_data) -> int:
        """_summary_

        :param str tx_out_address: destination address in bech32 format (addr_....)
        :param str tx_out_tokens: concatenation of tokens to be sent to this address, defaults to ""
        :param dict *reference_data: with Vasil it is possible to add inline datum or reference scripts
        most common options for datum:
        - "--tx-out-datum-hash-file", path to file or
        - "--tx-out-datum-hash-value", hash datum value or
        - "--tx-out-inline-datum-file", path to file or
        - "--tx-out-inline-datum-value", datum value or
        And for Plutus script:
        - "--tx-out-reference-script", reference script input file
        Example:
        min_required_utxo(tx_out_address, mint_output_string,"--tx-out-inline-datum-value", inline_datum
        """
        print("Executing min_required_utxo calculation")
        min_utxo = 0
        if not os.path.exists(self.TRANSACTION_PATH_FILE + "/protocol.json"):
            self.query_protocol(True)
        while True:
            previous_min_utxo = min_utxo
            address = f"{tx_out_address}+{str(min_utxo)}{tx_out_tokens}"
            command_string = [
                self.CARDANO_CLI_PATH,
                "transaction",
                "calculate-min-required-utxo",
                "--tx-out",
                address,
                "--protocol-params-file",
                self.TRANSACTION_PATH_FILE + "/protocol.json",
            ]
            if reference_data:
                command_string, index = self.insert_command(
                    5, 1, command_string, reference_data
                )
            min_utxo = self.execute_command(command_string, None)
            print(command_string)
            min_utxo = int(min_utxo.split(" ")[1][:-1])
            if min_utxo == previous_min_utxo:
                break
        return int(min_utxo)

    @staticmethod
    def cat_files(path, name):
        # Generate master key
        command_string = ["cat", path + name]
        output = subprocess.Popen(command_string, stdout=subprocess.PIPE)
        return output

    def insert_network(self, command_string: list, index: int, step: int) -> list:
        if self.CARDANO_NETWORK == "testnet":
            command_string, index = self.insert_command(
                index,
                step,
                command_string,
                ["--testnet-magic", self.CARDANO_NETWORK_MAGIC],
            )
        else:
            command_string, index = self.insert_command(
                index, step, command_string, ["--mainnet"]
            )
        return command_string

    def get_transactions(self, wallet_id: str) -> list[dict]:
        """Get the list of transactions from the given addresses.
        Args: Cardano Blockchain address or wallet id to search for UTXOs
        Returns:
            _type_: ada_transactions, token_transactions
            ada_transactions: list of transactions with lovelace only
            token_transactions: list of transactions including custom tokens
        """
        address = self.id_to_address(wallet_id)
        self.LOGGER.info(f"Executing Get Transactions for {address}")
        command_string = [self.CARDANO_CLI_PATH, "query", "utxo", "--address", address]
        if self.CARDANO_NETWORK == "testnet":
            command_string, index = self.insert_command(
                5, 1, command_string, ["--testnet-magic", self.CARDANO_NETWORK_MAGIC]
            )
        else:
            command_string, index = self.insert_command(
                5, 1, command_string, ["--mainnet"]
            )

        rawResult = self.execute_command(command_string, None)

        # Unpacking the results
        token_transactions = []
        for line in rawResult.splitlines():
            if "lovelace" in line: # and ("TxOutDatumInline" not in line or "ReferenceTxInsScriptsInlineDatumsInBabbageEra" not in line):
                transaction = {}
                trans = line.split()
                # if only lovelace
                transaction["hash"] = trans[0]
                transaction["id"] = trans[1]
                transaction["amounts"] = []
                tr_amount = {}
                tr_amount["token"] = trans[3]
                tr_amount["amount"] = trans[2]
                transaction["amounts"].append(tr_amount)
                # for each token
                if "TxOutDatumInline" in line:
                    extended_utxo_index = trans.index("TxOutDatumInline")
                    trans = trans[:extended_utxo_index-1]
                for i in range(0, int((len(trans) - 4) / 3)):
                    tr_amount = {}
                    tr_amount["token"] = trans[3 + i * 3 + 3]
                    tr_amount["amount"] = trans[3 + i * 3 + 2]
                    transaction["amounts"].append(tr_amount)
                token_transactions.append(transaction)
        self.LOGGER.info(f"Transactions: {token_transactions}")
        return token_transactions

    def id_to_address(self, wallet_name: str) -> str:
        """Get payment address stored locally from wallet_name; if address is
        provided, address is returned

        Args:
            wallet_name (string): id wallet generated by cardano wallet API or
            payment address.

        Returns:
            string: payment address associated to wallet_name
        """
        if not wallet_name.startswith("addr" or "DdzFF"):
            if os.path.exists(self.KEYS_FILE_PATH + "/" + wallet_name):
                with open(
                    self.KEYS_FILE_PATH
                    + "/"
                    + wallet_name
                    + "/"
                    + wallet_name
                    + ".payment.addr",
                    "r",
                ) as file:
                    address = file.readlines(1)[0]
            else:
                address = ""
        else:
            address = wallet_name
        return address

    def get_balance(self, wallet_id: str) -> dict:
        """Get the balance in dictionary format at the specified wallet
            address or from address base if wallet id is provided

        Args:
            wallet_id (string): id wallet generated by cardano wallet API or
            payment address.

        Returns:
            dict: balance dictionary listing the balance of the assets
            contained in the wallet
        """
        print("Executing Get Balance")
        wallet_id = self.id_to_address(wallet_id)
        transactions = self.get_transactions(wallet_id)
        balance_dict = {}
        if transactions == {}:
            balance_dict["lovelace"] = 0
            balance_dict["assets"] = 0
        else:
            amounts = []
            for utxo in transactions:
                for amount in utxo["amounts"]:
                    amounts.append(amount)
                amounts = sorted(amounts, key=itemgetter("token"))
                for key, value in groupby(amounts, key=itemgetter("token")):
                    balance = 0
                    for k in value:
                        balance = balance + int(k["amount"])
                    if key != "lovelace":
                        asset_namef = key.split(".")
                        policyid = asset_namef[0]
                        asset_name = asset_namef[1]
                        asset_name = bytes.fromhex(asset_name).decode("utf-8")
                        balance_dict[asset_name] = {
                            "policyID": policyid,
                            "balance": balance,
                        }
                    else:
                        balance_dict[key] = balance
        for k, v in balance_dict.items():
            self.LOGGER.info(f"{k} is : {v}")
        return balance_dict

    def string_encode(self, string: str) -> str:
        return b16encode(string.encode("utf-8")).decode("utf-8").lower()

