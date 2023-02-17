"""
This submodule defines the main classes representing the following Cardano
objects: Node and Wallet.
"""

# General Imports
import json
import os
import sys
from typing import Tuple, Union, List
import uuid
from dataclasses import dataclass

from cerberus import Validator

# Module Imports
WORKING_DIR = os.path.dirname(__file__)
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "cardanopythonlib"))

from path_utils import (
    save_file,
    save_metadata,
)
from cardanopythonlib.starter import Starter
from cardanopythonlib.mint import Mint
from cardanopythonlib.source import Source
from cardanopythonlib.destination import Destination


@dataclass()
class Node(Starter):
    """
    Class using primarly Cardano CLI commands
    """

    def get_txid_body(self) -> str:

        """ Get the transaction hash from the tx.draft file
        No need of paramaters as it assumes that the tx.draft is located at
        .priv/transactions

        :return str: TxOutRefId#TxOutRefIdx
        """

        print("Executing get transaction ID from Tx.draft file")
        command_string = [
            self.CARDANO_CLI_PATH,
            "transaction",
            "txid",
            "--tx-body-file",
            self.TRANSACTION_PATH_FILE + "/tx.draft",
        ]
        rawResult = self.execute_command(command_string, None)
        return rawResult

    def get_tx_info(self, txOutRefId: str, txOutRefIdx: int = 0) -> str:

        print("Exploring the transaction info")
        command_string = [
            self.CARDANO_CLI_PATH,
            "query",
            "utxo",
            "--tx-in",
            txOutRefId + "#" + str(txOutRefIdx),
            "--out-file",
            self.TRANSACTION_PATH_FILE + "/tx_info.json",
        ]
        command_string = self.insert_network(command_string, 5, 1)
        rawResult = self.execute_command(command_string, None)
        return rawResult

    def query_tip_exec(self):
        """Execute query tip.

        Returns:
            _type_: json with latest epoch, hash, slot, block, era,
                syncProgress
        """
        print("Executing Query Tip")
        command_string = [self.CARDANO_CLI_PATH, "query", "tip"]
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
        self.LOGGER.info(rawResult)
        return rawResult

    def sign_witness(self, signing_key_name: str)-> Union[str, None]:

        print("Executing Sign witness")
        path_skey = (
            self.KEYS_FILE_PATH + "/" + signing_key_name + "/" + signing_key_name
        )
        path_bodyfile = self.TRANSACTION_PATH_FILE + "/tx.draft"
        command_string = [
            self.CARDANO_CLI_PATH,
            "transaction",
            "witness",
            "--signing-key-file",
            path_skey + ".payment.skey",
            "--tx-body-file",
            path_bodyfile,
            "--out-file",
            path_skey + ".witness",
        ]
        if self.CARDANO_NETWORK == "testnet":
            command_string, index = self.insert_command(
                10, 1, command_string, ["--testnet-magic", self.CARDANO_NETWORK_MAGIC]
            )
        else:
            command_string, index = self.insert_command(
                10, 1, command_string, ["--mainnet"]
            )

        rawResult = self.execute_command(command_string, None)

        if rawResult == "":
            self.LOGGER.info(f"Sign witness file stored in {path_skey + '.witness'}")
        else:
            self.LOGGER.error(
                f"Error executing command sign: {rawResult} {command_string}"
            )
            rawResult = None
        return rawResult

    def create_simple_script(self, params: dict) -> Tuple[Union[dict, None], Union[str, None]]:
        print("Executing Creation of script")
        from schemas import create_simple_script_schema as schema

        v = Validator()

        try:
            assert v.validate(params, schema)  # type: ignore
            # Unpacking required params
            script_name = str(uuid.uuid1())
            hashes = params["hashes"]
            purpose = params["purpose"]
            type = params["type"]

            # Unpacking optional params
            required = params.get("required", None)
            type_time = params.get("type_time", None)
            slot = params.get("slot", None)

            # Assertions
            if type == "atLeast":
                assert isinstance(required, int)

            script_array = []
            simple_script = None
            policyID = None
            for hash in hashes:
                script = {"type": "sig", "keyHash": str(hash)}
                script_array.append(script)

            if type_time is not None and slot is not None:
                script_array.append({"type": type_time, "slot": slot})
            simple_script = {"type": str(type), "scripts": script_array}

            script_file_path = ""
            if purpose == "mint":
                script_file_path = self.MINT_FOLDER
            elif purpose == "multisig":
                script_file_path = self.MULTISIG_FOLDER

            save_metadata(script_file_path, script_name + ".script", simple_script)
            policyID = self.create_policy_id(purpose, script_name)
            old_name = script_file_path + '/' + script_name + ".script"
            new_name = script_file_path + '/' + str(policyID) + ".script"
            os.rename(old_name, new_name)
            self.LOGGER.info(f"Script stored in {script_file_path}, {simple_script}")

        except AssertionError:
            msg = f"Errors in the parameters. Check {v.errors}"  # type: ignore
            self.LOGGER.error(msg)
            simple_script = None
            policyID = None
        except Exception:
            self.LOGGER.error(f"Problems creating the script or policyID")
            simple_script = None
            policyID = None

        return simple_script, policyID

    def create_policy_id(self, purpose: str, script_name: str) -> Union[str, None]:
        """_summary_
         Args:
            wallet_id: id generated by cardano wallet API or payment address.

        Returns:
            _type_: policyID, policy_script
        """
        print("Executing Creation of Minting Policy ID")

        # Generate policyID from the policy script file
        if purpose == "mint":
            script_file_path = self.MINT_FOLDER
        elif purpose == "multisig":
            script_file_path = self.MULTISIG_FOLDER
        else:
            script_file_path = None

        if script_file_path is not None:
            command_string = [
                self.CARDANO_CLI_PATH,
                "transaction",
                "policyid",
                "--script-file",
                script_file_path + "/" + script_name + ".script",
            ]
            rawResult = self.execute_command(command_string, None)
            policyID = str(rawResult).rstrip()
            save_file(script_file_path + "/", policyID + ".policyid", str(policyID))
        else:
            policyID = None

        self.LOGGER.info(f"PolicyID is: {policyID}")
        return policyID

    def sign_transaction(self, keys_name: List[str]) -> str:
        """Sign the transaction based on tx_raw file.
         *args: represents the number of declared witness keys required to sign the transaction
        Example: sign_transaction(wallet1, wallet2). Two witnesses, transaction will be signed by wallet1 and wallet2.
        """
        command_string = [
            self.CARDANO_CLI_PATH,
            "transaction",
            "sign",
            "--tx-body-file",
            self.TRANSACTION_PATH_FILE + "/tx.draft",
            "--out-file",
            self.TRANSACTION_PATH_FILE + "/tx.signed",
        ]
        index = 5
        i = 0
        for key in keys_name:
            command_string, index = self.insert_command(
                i + 5,
                1,
                command_string,
                [
                    "--signing-key-file",
                    self.KEYS_FILE_PATH + "/" + key + "/" + key + ".payment.skey",
                ],
            )
            i = i + index
        if self.CARDANO_NETWORK == "testnet":
            command_string, index = self.insert_command(
                i + 5,
                1,
                command_string,
                ["--testnet-magic", self.CARDANO_NETWORK_MAGIC],
            )
        else:
            command_string, index = self.insert_command(
                i + 5, 1, command_string, ["--mainnet"]
            )

        self.LOGGER.info(command_string)
        rawResult = self.execute_command(command_string, None)

        if rawResult == "":
            self.LOGGER.info(
                f"Sign witness file stored in {self.TRANSACTION_PATH_FILE + '/tx.signed'}"
            )
            rawResult = "Transaction signed!!"
        else:
            rawResult = f"Error executing command sign: {rawResult} {command_string}"
            self.LOGGER.error(
                rawResult
            )
        return rawResult

    def submit_transaction(self):
        """Submit the transaction"""
        command_string = [
            self.CARDANO_CLI_PATH,
            "transaction",
            "submit",
            "--tx-file",
            self.TRANSACTION_PATH_FILE + "/tx.signed",
        ]
        if self.CARDANO_NETWORK == "testnet":
            command_string, index = self.insert_command(
                5, 1, command_string, ["--testnet-magic", self.CARDANO_NETWORK_MAGIC]
            )
        else:
            command_string, index = self.insert_command(
                5, 1, command_string, ["--mainnet"]
            )

        self.LOGGER.info(command_string)
        rawResult = self.execute_command(command_string, None)
        self.LOGGER.info(rawResult)
        return rawResult

    def build_tx_components(self, params: dict) -> str:

        print("Building the transaction")
        # Import schema for validation
        from schemas import build_tx_components_schema as schema

        v = Validator()
        # try:
        assert v.validate(params, schema)  # type: ignore
        # Unpacking the minimum required arguments
        address_origin = str(params.get("address_origin"))
        address_source = Source(address_origin)
        address_source_check = address_source.check()

        # Unpacking optional arguments
        change_address = params.get("change_address")
        address_destin_array = params.get("address_destin", None)
        metadata = params.get("metadata", None)
        mint = params.get("mint", None)
        script_path = params.get("script_path", None)
        witness = params.get("witness", None)
        inline_datum = params.get("inline_datum", None)
        inline_datum_array = []

        if inline_datum is not None:
            inline_datum_json_file = save_metadata(
                self.TRANSACTION_PATH_FILE, "tx_inline_datum.json", inline_datum
            )
            inline_datum_array.append("--tx-out-inline-datum-file")
            inline_datum_array.append(inline_datum_json_file)

        if not os.path.exists(self.TRANSACTION_PATH_FILE + "/protocol.json"):
            self.query_protocol(True)
        if address_source_check:
            qDestination = 0
            addr_output_array = []
            mint_array = []
            ttl_validity = ""
            ttl_slot = ""
            action = "send"

            # Mint part
            mint = Mint(mint)
            mint_array, mint_output_string, action = mint.string()
            ttl_validity, ttl_slot = mint.ttl()
            mint_utxo_value = mint.min_utxo(mint_output_string)
            if mint.mint is not None:
                if address_destin_array == None:
                    address_destin_array = [
                        {
                            "address": address_source.address,
                            "tokens": mint.tokens 
                        }
                    ]
            # End of mint part

            # Output part
            address_destin = Destination(address_destin_array)
            if address_destin.adestins != []:
                tx_out_address, qDestination, asset_output_string = address_destin.string(inline_datum_array)
                assets = ""
                if action == "send" or action == "burn":
                    assets = asset_output_string
                source_flag = address_destin.check(address_source, qDestination, assets)
                if source_flag and action != "burn":
                    addr_output_array = address_destin.add(tx_out_address, qDestination, asset_output_string)

            # End of output part
            
            # Total lovelace required
            qLovelace = mint_utxo_value + qDestination
            source_tokens = address_destin.tokenList()
            TxHash, amount_equal = address_source.utxo(qLovelace, action, source_tokens)
            if TxHash != []:
                TxHash_in = address_source.add(TxHash)
            
                if change_address is not None:
                    change_address = self.id_to_address(change_address)
                else:
                    change_address = address_origin
                addr_output_array.append("--change-address")
                addr_output_array.append(change_address)

                if witness is not None:
                    witness = str(witness)
                else:
                    witness = str(1)
                #########################################################
                command_string = [
                    self.CARDANO_CLI_PATH,
                    "transaction",
                    "build",
                    "--witness-override",
                    witness,
                    "--out-file",
                    self.TRANSACTION_PATH_FILE + "/tx.draft",
                ]
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
                        self.TRANSACTION_PATH_FILE, "tx_metadata.json", metadata
                    )
                    metadata_array.append("--metadata-json-file")
                    metadata_array.append(metadata_json_file)
                    command_string, index = self.insert_command(
                        3 + i, 1, command_string, metadata_array
                    )
                    i = i + index
                if mint_array != []:
                    command_string, index = self.insert_command(
                        3 + i, 1, command_string, mint_array
                    )
                    i = i + index
                    if ttl_validity != "" and ttl_slot != "":
                        invalid = None
                        if ttl_validity == "before":
                            invalid = "--invalid-hereafter"
                        elif ttl_validity == "after":
                            invalid = "--invalid-before"
                        else:
                            self.LOGGER.error(
                                f"Not supported type validity in the minting script {ttl_validity}"
                            )
                            raise TypeError()
                        command_string, index = self.insert_command(
                            3 + i, 1, command_string, [invalid, ttl_slot]
                        )
                        i = i + index

                script_path_array = []
                if script_path is not None:
                    script_path_array.append("--tx-in-script-file")
                    script_path_array.append(script_path)
                    command_string, index = self.insert_command(
                        3 + i, 1, command_string, script_path_array
                    )
                    i = i + index

                inline_datum_array = []
                if inline_datum is not None:
                    inline_datum_json_file = save_metadata(
                        self.TRANSACTION_PATH_FILE, "tx_inline_datum.json", inline_datum
                    )
                    inline_datum_array.append("--tx-out-inline-datum-file")
                    inline_datum_array.append(inline_datum_json_file)
                    command_string, index = self.insert_command(
                        3 + i, 1, command_string, inline_datum_array
                    )
                    i = i + index

                if self.CARDANO_NETWORK == "testnet":
                    command_string, index = self.insert_command(
                        3 + i,
                        1,
                        command_string,
                        ["--testnet-magic", self.CARDANO_NETWORK_MAGIC],
                    )
                    i = i + index
                    command_string, index = self.insert_command(
                        3 + i, 1, command_string, ["--" + str(self.CARDANO_ERA)]
                    )
                else:
                    command_string, index = self.insert_command(
                        3 + i, 1, command_string, ["--mainnet"]
                    )
                    i = i + index
                    command_string, index = self.insert_command(
                        3 + i, 1, command_string, ["--" + str(self.CARDANO_ERA)]
                    )

                self.LOGGER.info(command_string)
                rawResult = self.execute_command(command_string, None)
                self.LOGGER.info(rawResult)
                if "Estimated transaction fee: Lovelace" not in rawResult:
                    raise TypeError()
            else:
                msg = "Not utxos found in the address provided"
                self.LOGGER.error(msg)
                rawResult = msg
        else:
            msg = "Not utxos found in the address provided"
            self.LOGGER.error(msg)
            rawResult = msg
    # except TypeError:
    #     msg = "Missing required arguments"
    #     self.LOGGER.error(msg)
    #     rawResult = msg
    # except AssertionError:
    #     msg = f"Errors in the message dictionary format. Check {v.errors}"  # type: ignore
    #     self.LOGGER.error(msg)
    #     rawResult = msg
    # except Exception:
    #     msg = f"Errors while building the transaction. Probably insufficient ada or native asset funds"
    #     self.LOGGER.error(msg)
    #     rawResult = msg

        return rawResult

    def analyze_tx_body(self)-> str:
        print("Analyzing the transaction....")
        command_string = [
            self.CARDANO_CLI_PATH,
            "transaction",
            "view",
            "--tx-body-file",
            self.TRANSACTION_PATH_FILE + "/tx.draft",
        ]

        rawResult = self.execute_command(command_string, None)
        self.LOGGER.info(rawResult)
        return rawResult

    def analyze_tx_signed(self)-> str:
        print("Analyzing the transaction....")
        command_string = [
            self.CARDANO_CLI_PATH,
            "transaction",
            "view",
            "--tx-file",
            self.TRANSACTION_PATH_FILE + "/tx.signed",
        ]

        rawResult = self.execute_command(command_string, None)
        self.LOGGER.info(rawResult)
        return rawResult

    def assemble_tx(self, witness_wallet_name_array: list[str])-> str:
        print("Executing Assemble witness")

        witness_output_array = []
        for witness_key_name in witness_wallet_name_array:

            witness_output_array.append("--witness-file")
            witness_output_array.append(
                self.KEYS_FILE_PATH
                + "/"
                + witness_key_name
                + "/"
                + witness_key_name
                + ".witness"
            )

        path_bodyfile = self.TRANSACTION_PATH_FILE + "/tx.draft"

        command_string = [
            self.CARDANO_CLI_PATH,
            "transaction",
            "assemble",
            "--tx-body-file",
            path_bodyfile,
            "--out-file",
            self.TRANSACTION_PATH_FILE + "/tx.signed",
        ]

        i = 0
        command_string, index = self.insert_command(
            5 + i, 1, command_string, witness_output_array
        )

        rawResult = self.execute_command(command_string, None)
        if rawResult == "":
            tx_signed_path = self.TRANSACTION_PATH_FILE
            name = "tx.signed"
            rawResult = "Transaction signed file stored in '%s' with the name '%s'" % (
                tx_signed_path,
                name,
            )

        return rawResult