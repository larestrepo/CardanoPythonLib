"""
This submodule defines the destination class
"""

# General Imports
from typing import Tuple, Union, List
from dataclasses import dataclass, field


# Module Imports

from cardanopythonlib.starter import Starter
from cardanopythonlib.source import Source

@dataclass()
class Destination(Starter):
    adestins: Union[list[dict], None] = field(init=True, default=None)

    TokenList = List[tuple[str, int, str]]
    def __post_init__(self):
        if self.adestins:
            self.adestins = self.adestins
        else:
            self.adestins = []
    
    def tokenList(self) -> TokenList:
        token_list = []
        if self.adestins:
            for adestin in self.adestins:
                tokens = adestin.get("tokens", None)
                if tokens is not None:
                    for item in tokens:
                        token_list.append(tuple(item.values()))

        return token_list
    
    def tokens(self, tokens: Union[dict, None]) -> str:
        asset_output = ""
        policyid = ""
        token_list = []
        if tokens:
            for token in tokens:
                name = token["name"]
                amount = token["amount"]
                policyid = token["policyID"]
                name = self.string_encode(name)
                full_name = policyid + "." + name
                asset_output = (str(amount) + " " + full_name + "+")
                token_list.append((name, amount, policyid))
        
        return asset_output[:-1]

    def check(self, address_source: Source, qDestination: int, assets_output: str) -> bool:
        utxos = address_source.transactions
        tLovelace = address_source.tLovelace
        amounts = []
        asset = assets_output.split(" ")
        asset_check = True
        lovelace_check = False
        if assets_output != "":
            asset_check = False
            for utxo in utxos:
                for amount in utxo["amounts"]:
                    amounts.append(amount)
                    if asset[1] in amount["token"]:
                        if asset[0] <= amount["amount"]:
                            asset_check = True
        if tLovelace > qDestination:
            lovelace_check = True
        return asset_check and lovelace_check
    
    def string(self, reference_data: list[str]) -> Tuple[str, int, str]:
        tx_out_address = ""
        amount = 0
        asset_output_string = ""
        if self.adestins:
            asset_output_string = ""
            for adestin in self.adestins:
                tx_out_address = adestin["address"]
                amount = adestin.get("amount", 0)
                tokens = adestin.get("tokens", None)
                asset_output = self.tokens(tokens)
                if asset_output != "":
                    asset_output = "+" + asset_output
                quantity = self.min_required_utxo(tx_out_address, asset_output, *reference_data)
                if amount < quantity:
                    amount = quantity
                asset_output_string += asset_output
        return tx_out_address, amount, asset_output_string

    def add(self, address: str="", quantity: int=0, assets: str="") -> list[str]:
        output_string = ""
        output_string = address + "+" + str(quantity)
        output_string = output_string + assets
        return ["--tx-out", output_string]
