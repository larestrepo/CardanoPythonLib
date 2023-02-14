"""
This submodule defines the mint class
"""

# General Imports
import json
from base64 import b16encode
from typing import Tuple, Union
from dataclasses import dataclass, field

from cardanopythonlib.starter import Starter


@dataclass()
class Mint(Starter):

    mint: Union[dict, None] = field(init=True, default=None)
    
    def __post_init__(self):
        if self.mint:
            self.tokens = self.mint["tokens"]
            self.action = self.mint["action"]
        else:
            self.tokens = {}
            self.action = "send"
            
    
    def quantity(self, token: dict) -> int:
        return int(token["amount"])

    def policyid(self, token: dict) -> str: # type: ignore
        policyid = ""
        for token in self.tokens:
            policyid = token["policyID"]
        return str(policyid)

    def coin_name(self, token: dict) -> str:
        mint_name = "lovelace"
        for token in self.tokens:
            mint_name = token["name"].encode("utf-8")
            mint_name = b16encode(mint_name).decode("utf-8").lower()
            policyid = self.policyid(token)
            mint_name = str(policyid + "." + mint_name)
        
        return mint_name
        
    def script(self, policyid: str) -> Union[dict, None]:
        script = None
        if policyid != "":
            policy_path = self.MINT_FOLDER + '/' + policyid + '.script'
            with open (policy_path, 'r') as file:
                script_content = json.load(file)
            script = script_content.get("scripts")
        return script

    def string(self) -> Tuple[list[str], str, str]:
        mint_output_string = ''
        mint_array = []
        policy_path = ""
        if self.tokens:
            for token in self.tokens:
                mint_name = self.coin_name(token)
                mint_quantity = self.quantity(token)
                mint_policyid = self.policyid(token)
                policy_path = self.MINT_FOLDER + '/' + mint_policyid + '.script'
                mint_output_string += (str((-1)*mint_quantity) + " "+ mint_name) if self.action == "burn" else (str(mint_quantity) + " "+ mint_name+ "+")
            if mint_output_string[-1] == '+':
                mint_output_string = mint_output_string[:-1]
            mint_string = "--mint="
            mint_string = mint_string + mint_output_string
            mint_output_string = "" if self.action == "burn" else "+" + mint_output_string
            mint_array.append(mint_string)
            mint_array.append("--mint-script-file")
            mint_array.append(policy_path)
        return mint_array, mint_output_string, self.action
    
    def ttl(self) -> Tuple[str, str]:
        type_validity = ""
        slot_validity = ""
        for token in self.tokens:
            policyid = self.policyid(token)
            script = self.script(policyid)
            if script is not None:
                for items in script:
                    if items["type"] != "sig":
                        type_validity = items["type"]
                        slot_validity = items["slot"]
        return type_validity, slot_validity

    def min_utxo(self, tx_out_tokens: str, source_address: str="addr_test1vp674jugprun0epvmep395k5hdpt689legmeh05s50kq8qcul3azr") -> int:
        min_lovelece_utxo = 0
        if tx_out_tokens != "":
            min_lovelece_utxo = self.min_required_utxo(source_address, tx_out_tokens)
        return min_lovelece_utxo
