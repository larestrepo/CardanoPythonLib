"""
This submodule defines the keys class
"""

# General Imports
import json
import os
import sys
from typing import Tuple, Union
from dataclasses import dataclass

# Module Imports

WORKING_DIR = os.path.dirname(__file__)
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "cardanopythonlib"))

from path_utils import (
    create_folder,
    remove_file,
    remove_folder,
    save_file,
)
from cardanopythonlib.starter import Starter


@dataclass()
class Keys(Starter):

    def generate_mnemonic(self, size: int = 24) -> list[str]:
        """Create mnemonic sentence (list of mnemonic words)
        Input: size number of words: 24 by default"""
        print("Executing Generate New Mnemonic Phrase")
        # Generate mnemonic
        command_string = [
            "cardano-address",
            "recovery-phrase",
            "generate",
            "--size",
            str(size),
        ]
        rawResult = self.execute_command(command_string, None)
        mnemonic = rawResult.split()
        print("Mnemonics are '%s'" % (mnemonic))
        return mnemonic

    def deriveRootKey(self, mnemonic: list[str])-> str:
        """Generate root key
            When folder empty, root key is not save locally in a file
        Args:
            mnemonic ([list]): [Phrases passed as array]
        Returns:
            [str]: [Root private key]
        """
        # Save temp mnemonic
        content = " ".join(mnemonic)
        save_file(self.KEYS_FILE_PATH, "/temp_mnemonic", content)

        # Generate master key
        output = self.cat_files(self.KEYS_FILE_PATH, "/temp_mnemonic")
        command_string = ["cardano-address", "key", "from-recovery-phrase", "Shelley"]
        rawResult = self.execute_command(command_string, output.stdout)

        # Delete file mnemonic
        print("Root private key: '%s'" % (rawResult))
        remove_file(self.KEYS_FILE_PATH, "/temp_mnemonic")
        return rawResult

    def deriveExtendedSigningStakeKey(self, root_key: str)-> str:
        """AI is creating summary for deriveExtendedSigningStakeKey

        Args:
            root_key ([str]): [Root private key]

        Returns:
            [str]: [extended stake signing key xsk]
        """
        # Save temp root_key
        save_file(self.KEYS_FILE_PATH, "/temp_root.xsk", str(root_key))

        output = self.cat_files(self.KEYS_FILE_PATH, "/temp_root.xsk")
        # Generate extended stake signing key
        command_string = ["cardano-address", "key", "child", "1852H/1815H/0H/2/0"]
        rawResult = self.execute_command(command_string, output.stdout)

        print("Stake extended signing key: '%s'" % (rawResult))
        # Delete file root key
        remove_file(self.KEYS_FILE_PATH, "/temp_root.xsk")
        return rawResult

    def deriveExtendedSigningPaymentKey(self, root_key: str)-> str:
        """AI is creating summary for deriveExtendedSigningPaymentKey

        Args:
            root_key ([str]): [Root private key]

        Returns:
            [str]: [extended payment signing key xsk]
        """
        # Save temp root_key
        save_file(self.KEYS_FILE_PATH, "/temp_root.xsk", str(root_key))

        output = self.cat_files(self.KEYS_FILE_PATH, "/temp_root.xsk")
        # Generate extended Payment signing key
        command_string = ["cardano-address", "key", "child", "1852H/1815H/0H/0/0"]
        rawResult = self.execute_command(command_string, output.stdout)

        print("Payment extended signing key: '%s'" % (rawResult))
        # Delete file root key
        remove_file(self.KEYS_FILE_PATH, "/temp_root.xsk")
        return rawResult

    def deriveExtendedVerificationPaymentKey(self, payment_signing_key: str)-> str:
        """AI is creating summary for deriveExtendedVerificationPaymentKey

        Args:
            payment_signing_key [str]: [extended payment signing key xsk]

        Returns:
            [str]: [extended payment verification key xvk]
        """
        # Save temp root_key
        save_file(self.KEYS_FILE_PATH, "/temp_payment.xsk", str(payment_signing_key))

        output = self.cat_files(self.KEYS_FILE_PATH, "/temp_payment.xsk")
        # Generate extended public account key xpub
        command_string = ["cardano-address", "key", "public", "--with-chain-code"]
        rawResult = self.execute_command(command_string, output.stdout)

        print("Payment extended verification key: '%s'" % (rawResult))
        # Delete file root key
        remove_file(self.KEYS_FILE_PATH, "/temp_payment.xsk")
        return rawResult

    def deriveExtendedVerificationStakeKey(self, stake_signing_key: str)-> str:
        """AI is creating summary for deriveExtendedVerificationStakeKey

        Args:
            stake_signing_key [str]: [extended stake signing key xsk]

        Returns:
            [str]: [extended stake verification key xvk]
        """
        # Save temp root_key
        save_file(self.KEYS_FILE_PATH, "/temp_stake.xsk", str(stake_signing_key))

        output = self.cat_files(self.KEYS_FILE_PATH, "/temp_stake.xsk")
        # Generate extended public account key xpub
        command_string = ["cardano-address", "key", "public", "--with-chain-code"]
        rawResult = self.execute_command(command_string, output.stdout)
        print("Stake extended verification key: '%s'" % (rawResult))
        # Delete file root key
        remove_file(self.KEYS_FILE_PATH, "/temp_stake.xsk")
        return rawResult

    def derivePaymentAddress(self, payment_verification_key: str)-> str:
        """AI is creating summary for derivePaymentAddress
        Args:
            payment_verification_key ([str]):
            [extended payment verification key xvk]

        Returns:
            [str]: [payment public address]
        """
        # Save temp root_key
        save_file(self.KEYS_FILE_PATH, "/temp_payment.xvk", str(payment_verification_key))

        output = self.cat_files(self.KEYS_FILE_PATH, "/temp_payment.xvk")
        # Generate extended public account key xpub
        command_string = [
            "cardano-address",
            "address",
            "payment",
            "--network-tag",
            self.CARDANO_NETWORK,
        ]
        rawResult = self.execute_command(command_string, output.stdout)

        print("Payment extended address: '%s'" % (rawResult))
        # Delete file root key
        remove_file(self.KEYS_FILE_PATH, "/temp_payment.xvk")
        return rawResult

    def convertPaymentKey(self, payment_signing_key: str, name: str)-> Tuple[str, str, str]:
        """This function converts the cardano wallet payment keys to
        cardano-cli payment keys


        Args:
            payment_signing_key ([str]): [extended payment signing key xsk]

        Returns:
            [str]: [payment_skey, payment_vkey, payment_addr]
        """
        # Save temp root_key
        save_file(self.KEYS_FILE_PATH, "/temp_payment.xsk", str(payment_signing_key))

        # Generate extended public account key xpub
        command_string = [
            self.CARDANO_CLI_PATH,
            "key",
            "convert-cardano-address-key",
            "--shelley-payment-key",
            "--signing-key-file",
            self.KEYS_FILE_PATH + "/temp_payment.xsk",
            "--out-file",
            self.KEYS_FILE_PATH + "/" + name + "/" + name + ".payment.skey",
        ]

        self.execute_command(command_string, None)

        output = self.cat_files(self.KEYS_FILE_PATH, "/" + name + "/" + name + ".payment.skey")
        payment_skey = output.communicate()[0].decode("utf-8")
        payment_skey = json.loads(payment_skey)

        # Get verification payment key from signing payment key.
        command_string = [
            self.CARDANO_CLI_PATH,
            "key",
            "verification-key",
            "--signing-key-file",
            self.KEYS_FILE_PATH + "/" + name + "/" + name + ".payment.skey",
            "--verification-key-file",
            self.KEYS_FILE_PATH + "/" + name + "/" + name + ".payment.evkey",
        ]
        self.execute_command(command_string, None)

        # Get non-extended verification payment key
        # from extended verification payment key.
        command_string = [
            self.CARDANO_CLI_PATH,
            "key",
            "non-extended-key",
            "--extended-verification-key-file",
            self.KEYS_FILE_PATH + "/" + name + "/" + name + ".payment.evkey",
            "--verification-key-file",
            self.KEYS_FILE_PATH + "/" + name + "/" + name + ".payment.vkey",
        ]
        self.execute_command(command_string, None)

        output = self.cat_files(self.KEYS_FILE_PATH, "/" + name + "/" + name + ".payment.vkey")
        payment_vkey = output.communicate()[0].decode("utf-8")
        payment_vkey = json.loads(payment_vkey)

        # Build payment addresses
        command_string = [
            self.CARDANO_CLI_PATH,
            "address",
            "build",
            "--payment-verification-key-file",
            self.KEYS_FILE_PATH + "/" + name + "/" + name + ".payment.vkey",
            "--out-file",
            self.KEYS_FILE_PATH + "/" + name + "/" + name + ".payment.addr",
        ]
        if self.CARDANO_NETWORK == "testnet":
            command_string, index = self.insert_command(
                5, 1, command_string, ["--testnet-magic", self.CARDANO_NETWORK_MAGIC]
            )
        else:
            command_string, index = self.insert_command(
                5, 1, command_string, ["--mainnet"]
            )
        self.execute_command(command_string, None)

        output = self.cat_files(self.KEYS_FILE_PATH, "/" + name + "/" + name + ".payment.addr")
        payment_addr = output.communicate()[0].decode("utf-8")

        print(
            "Payment signing key: '%s' \n Payment verification key: '%s' \n Payment address: '%s"
            % (payment_skey, payment_vkey, payment_addr)
        )
        # Delete files
        remove_file(self.KEYS_FILE_PATH, "/temp_payment.xsk")

        return payment_skey, payment_vkey, payment_addr

    def convertStakeSigningKey(self, stake_signing_key: str, name: str)-> Tuple[str, str, str]:
        """This function converts the cardano wallet stake keys to
        cardano-cli stake keys


        Args:
            stake_signing_key ([str]): [extended stake signing key xsk]

        Returns:
            [str]: [stake_skey, stake_vkey, stake_addr]
        """
        # Save temp root_key
        save_file(self.KEYS_FILE_PATH, "/temp_stake.xsk", str(stake_signing_key))

        # Generate extended public account key xpub
        command_string = [
            self.CARDANO_CLI_PATH,
            "key",
            "convert-cardano-address-key",
            "--shelley-stake-key",
            "--signing-key-file",
            self.KEYS_FILE_PATH + "/temp_stake.xsk",
            "--out-file",
            self.KEYS_FILE_PATH + "/" + name + "/" + name + ".stake.skey",
        ]
        self.execute_command(command_string, None)
        output = self.cat_files(self.KEYS_FILE_PATH, "/" + name + "/" + name + ".stake.skey")
        stake_skey = output.communicate()[0].decode("utf-8")
        stake_skey = json.loads(stake_skey)

        # Get verification stake key from signing stake key.
        command_string = [
            self.CARDANO_CLI_PATH,
            "key",
            "verification-key",
            "--signing-key-file",
            self.KEYS_FILE_PATH + "/" + name + "/" + name + ".stake.skey",
            "--verification-key-file",
            self.KEYS_FILE_PATH + "/" + name + "/" + name + ".stake.evkey",
        ]
        self.execute_command(command_string, None)

        # Get non-extended verification stake key
        # from extended verification stake key.
        command_string = [
            self.CARDANO_CLI_PATH,
            "key",
            "non-extended-key",
            "--extended-verification-key-file",
            self.KEYS_FILE_PATH + "/" + name + "/" + name + ".stake.evkey",
            "--verification-key-file",
            self.KEYS_FILE_PATH + "/" + name + "/" + name + ".stake.vkey",
        ]
        self.execute_command(command_string, None)
        output = self.cat_files(self.KEYS_FILE_PATH, "/" + name + "/" + name + ".stake.vkey")
        stake_vkey = output.communicate()[0].decode("utf-8")
        stake_vkey = json.loads(stake_vkey)

        # Build stake addresses
        command_string = [
            self.CARDANO_CLI_PATH,
            "stake-address",
            "build",
            "--stake-verification-key-file",
            self.KEYS_FILE_PATH + "/" + name + "/" + name + ".stake.vkey",
            "--out-file",
            self.KEYS_FILE_PATH + "/" + name + "/" + name + ".stake.addr",
        ]
        if self.CARDANO_NETWORK == "testnet":
            command_string, index = self.insert_command(
                5, 1, command_string, ["--testnet-magic", self.CARDANO_NETWORK_MAGIC]
            )
        else:
            command_string, index = self.insert_command(
                5, 1, command_string, ["--mainnet"]
            )
        self.execute_command(command_string, None)
        output = self.cat_files(self.KEYS_FILE_PATH, "/" + name + "/" + name + ".stake.addr")
        stake_addr = output.communicate()[0].decode("utf-8")
        print(
            "Stake signing key: '%s' \n Stake verification key: '%s' \n Stake address: '%s"
            % (stake_skey, stake_vkey, stake_addr)
        )
        # Delete file
        remove_file(self.KEYS_FILE_PATH, "/temp_stake.xsk")

        return stake_skey, stake_vkey, stake_addr

    def deriveBaseAddress(self, name:str)-> str:
        """Derive the base address Cardano cli command

        Args:
        payment_vkey ([str]): [Payment verification key]
        stake_vkey ([str]): [Payment verification key]

        Returns:
            [str]: [Combined base address]
        """
        # Build base addresses
        command_string = [
            self.CARDANO_CLI_PATH,
            "address",
            "build",
            "--payment-verification-key-file",
            self.KEYS_FILE_PATH + "/" + name + "/" + name + ".payment.vkey",
            "--stake-verification-key-file",
            self.KEYS_FILE_PATH + "/" + name + "/" + name + ".stake.vkey",
            "--out-file",
            self.KEYS_FILE_PATH + "/" + name + "/" + name + ".base.addr",
        ]
        if self.CARDANO_NETWORK == "testnet":
            command_string, index = self.insert_command(
                7, 1, command_string, ["--testnet-magic", self.CARDANO_NETWORK_MAGIC]
            )
        else:
            command_string, index = self.insert_command(
                7, 1, command_string, ["--mainnet"]
            )
        self.execute_command(command_string, None)
        output = self.cat_files(self.KEYS_FILE_PATH, "/" + name + "/" + name + ".base.addr")
        base_addr = output.communicate()[0].decode("utf-8")

        remove_file(self.KEYS_FILE_PATH, "/temp_payment.vkey")
        remove_file(self.KEYS_FILE_PATH, "/temp_stake.vkey")
        print("Base address: '%s'" % (base_addr))
        return base_addr

    def keyHashing(self, name: str)-> str:
        keys_file_path = self.KEYS_FILE_PATH + "/" + name
        # Build hash from key
        command_string = [
            self.CARDANO_CLI_PATH,
            "address",
            "key-hash",
            "--payment-verification-key-file",
            keys_file_path + "/" + name + ".payment.vkey",
        ]

        rawResult = self.execute_command(command_string, None)
        key_hash = str(rawResult.rstrip())
        print("Key hash of the verification payment key: '%s'" % (key_hash))
        return key_hash

    def deriveAllKeys(self, name: str, size: Union[int, list[str]] = 24, save_flag: bool = True) -> dict:
        """This function creates all the keys and addresses and save them
        in root_folder/priv/wallet/walletname path


        Args:
            name ([str]): [name of the wallet to save the keys]
            size ([int]): [phrase extension: 24, 15, etc]
            save_flag ([bool]): [True if saved locally, False to only print results in console]
        """
        if not os.path.exists(self.KEYS_FILE_PATH + "/" + name):
            os.makedirs(self.KEYS_FILE_PATH + "/" + name)
        if isinstance(size, int):
            nmemonic = self.generate_mnemonic(size)
        else:
            nmemonic = size
        root_key = self.deriveRootKey(nmemonic)
        stake = self.deriveExtendedSigningStakeKey(root_key)
        payment = self.deriveExtendedSigningPaymentKey(root_key)

        payment_public_account_key = self.deriveExtendedVerificationPaymentKey(payment)
        stake_public_account_key = self.deriveExtendedVerificationStakeKey(stake)

        payment_address = self.derivePaymentAddress(payment_public_account_key)
        # Convert from cardano wallet keys to cardano-cli keys
        """
        Convert payment signing keys
        """
        payment_skey, payment_vkey, payment_addr = self.convertPaymentKey(payment, name)
        """
        Convert stake signing keys
        """
        stake_skey, stake_vkey, stake_addr = self.convertStakeSigningKey(stake, name)
        base_addr = self.deriveBaseAddress(name)

        # Hashing the verification keys
        hash_verification_key = self.keyHashing(name)

        # Building the paths
        payment_skey_path = self.KEYS_FILE_PATH + "/" + name + "/" + name + ".payment.skey"
        payment_vkey_path = self.KEYS_FILE_PATH + "/" + name + "/" + name + ".payment.vkey"
        payment_addr_path = self.KEYS_FILE_PATH + "/" + name + "/" + name + ".payment.addr"
        stake_skey_path = self.KEYS_FILE_PATH + "/" + name + "/" + name + ".stake.skey"
        stake_vkey_path = self.KEYS_FILE_PATH + "/" + name + "/" + name + ".stake.vkey"
        stake_addr_path = self.KEYS_FILE_PATH + "/" + name + "/" + name + ".stake.addr"

        # Creating the dict
        keys = {
            "mnemonic": nmemonic,
            "root_key": root_key,
            "private_stake_key": stake,
            "private_payment_key": payment,
            "payment_account_key": payment_public_account_key,
            "stake_account_key": stake_public_account_key,
            "payment_addr": payment_address,
            "payment_addr_path": payment_addr_path,
            "payment_skey": payment_skey,
            "payment_skey_path": payment_skey_path,
            "payment_vkey": payment_vkey,
            "payment_vkey_path": payment_vkey_path,
            "stake_addr": stake_addr,
            "stake_skey": stake_skey,
            "stake_skey_path": stake_skey_path,
            "stake_vkey": stake_vkey,
            "stake_vkey_path": stake_vkey_path,
            "stake_addr_path": stake_addr_path,
            "base_addr": base_addr,
            "hash_verification_key": hash_verification_key,
        }
        if save_flag:
            with open(self.KEYS_FILE_PATH + "/" + name + "/" + name + ".json", "w") as file:
                json.dump(keys, file, indent=4, ensure_ascii=False)

            print("##################################")
            print(
                "Find all the keys and address details in: %s"
                % (self.KEYS_FILE_PATH + "/" + name + "/" + name + ".json")
            )
            print("##################################")
        else:
            remove_folder(self.KEYS_FILE_PATH + "/" + name)
            self.LOGGER.debug(f"Keys info were not saved locally")
        return keys

    def generateCardanoKeys(self, name: str)-> str:
        keys_file_path = self.KEYS_FILE_PATH + "/" + name
        create_folder(keys_file_path)
        # Build Cardano keys with Cardano CLI
        command_string = [
            self.CARDANO_CLI_PATH,
            "address",
            "key-gen",
            "--verification-key-file",
            keys_file_path + "/" + name + ".payment.vkey",
            "--signing-key-file",
            keys_file_path + "/" + name + ".payment.skey",
        ]

        rawResult = self.execute_command(command_string, None)

        command_string = [
            self.CARDANO_CLI_PATH,
            "stake-address",
            "key-gen",
            "--verification-key-file",
            keys_file_path + "/" + name + ".stake.vkey",
            "--signing-key-file",
            keys_file_path + "/" + name + ".stake.skey",
        ]

        rawResult = self.execute_command(command_string, None)
        if rawResult == "":
            rawResult = "Keys stored in '%s' under the name '%s'" % (
                keys_file_path,
                name,
            )
        return rawResult

    def create_address_script(self, script_name: str)-> str:
        keys_file_path = self.KEYS_FILE_PATH + "/" + script_name
        # Build script addresses
        command_string = [
            self.CARDANO_CLI_PATH,
            "address",
            "build",
            "--payment-script-file",
            keys_file_path + "/" + script_name + ".script",
            "--out-file",
            keys_file_path + "/" + script_name + ".script.addr",
        ]
        if self.CARDANO_NETWORK == "testnet":
            command_string, index = self.insert_command(
                5, 1, command_string, ["--testnet-magic", self.CARDANO_NETWORK_MAGIC]
            )
        else:
            command_string, index = self.insert_command(
                5, 1, command_string, ["--mainnet"]
            )
        rawResult = self.execute_command(command_string, None)
        print("Script address stored in '%s'" % (keys_file_path))
        return rawResult
