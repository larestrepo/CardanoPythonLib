"""
This submodule defines the source class
"""


# General Imports
import random
from itertools import chain
from typing import Tuple, List
from dataclasses import dataclass, field

# Module Imports
from cardanopythonlib.starter import Starter

@dataclass()
class Source(Starter):
    address: str = field(init=True)
    deplete: bool = field(init=False, default=False)
    minCost: int = field(init=False, default=1000000)
    
    TokenList = List[tuple[str, int, str]]

    def __post_init__(self):
        if self.address != "":
            self.address = self.id_to_address(self.address)
            self.tLovelace = self.get_balance(self.address).get("lovelace", 0)
            self.transactions = self.get_transactions(self.address)
            self.utxo_lovelace = list(filter(lambda utxo: len(utxo["amounts"]) == 1, self.transactions))
            self.utxo_tokens = list(filter(lambda utxo: len(utxo["amounts"]) != 1, self.transactions))
            self.change_min_utxo = self.min_required_utxo(self.address)
        else:
            self.utxo_lovelace = []
            self.utxo_tokens = []

    def selection_utxo(self, utxo_list: list, quantity: int, coin_name: str="lovelace") -> Tuple[list[str], int, bool]:
        TxHash = []
        TxHash_lower = []
        TxHash_greater = []
        amount_equal = 0
        amount_lower = []
        amount_greater = []
        utxo_found = False
        for utxo in utxo_list:
            for amount in utxo["amounts"]:
                if amount.get("token") == coin_name:
                    if coin_name != "lovelace":
                        self.minCost = 0
                    if self.deplete:
                        TxHash.append(utxo["hash"] + "#" + utxo.get("id"))
                        amount_equal += int(amount.get("amount"))
                        utxo_found = True
                        break
                    if int(amount.get("amount")) == quantity + self.minCost:
                        TxHash.append(utxo["hash"] + "#" + utxo.get("id"))
                        amount_equal =sum([int(amount["amount"]) for amount in utxo["amounts"] if amount["token"] == "lovelace"])
                        utxo_found = True
                        break
                    elif int(amount.get("amount")) < quantity + self.minCost:
                        TxHash_lower.append(utxo["hash"] + "#" + utxo.get("id"))
                        amount_lower.append(int(amount.get("amount")))
                    elif int(amount.get("amount")) > quantity + self.minCost:
                        TxHash_greater.append(
                            utxo["hash"] + "#" + utxo.get("id")
                        )
                        amount_greater.append(int(amount.get("amount")))
            else:
                continue
            break

        if not utxo_found: # If more than 1 utxo 
            if sum(amount_lower) == quantity + self.minCost:
                TxHash = TxHash_lower
                amount_equal = sum(amount_lower)
            elif sum(amount_lower) < quantity + self.minCost:
                if amount_greater == []:
                    TxHash = []
                    amount_equal = 0
                else:
                    amount_equal = min(amount_greater)
                    index = [
                        i for i, j in enumerate(amount_greater) if j == amount_equal
                    ][0]
                    TxHash.append(TxHash_greater[index])
            elif sum(amount_lower) > quantity +  self.minCost and TxHash_greater == []:
                # Creating descending tuple list (utxo, q) to fill te amount required
                combined = sorted(list(zip(TxHash_lower, amount_lower)), key=lambda utxo: utxo[1], reverse=True)
                for i, (utxo, q) in enumerate(combined):
                    amount_equal += q
                    TxHash.append(utxo)
                    if amount_equal >= quantity + self.minCost:
                        break
            else:
                utxo_array = []
                amount_array = []
                for _ in range(999):
                    index_random = random.randint(0, len(self.address) - 1)
                    utxo = self.transactions.pop(index_random)
                    utxo_array.append(utxo["hash"] + "#" + utxo.get("id"))
                    for amount in utxo["amounts"]:
                        if amount.get("token") == coin_name:
                            amount_array.append(int(amount.get("amount")))
                    if sum(amount_array) >= quantity + self.minCost:
                        amount_equal = sum(amount_array)
                        break
                TxHash = utxo_array

        return TxHash, amount_equal, utxo_found

    def utxo(self, qLovelace: int, action: str, qToken: TokenList=[]) -> Tuple[list[str], int]:
        TxHash = []
        amount_equal = 0
        if self.address:
            if action == "mint":
                qToken = []
            if qToken != []:
                coin_name = ""
                for n, q, p in qToken:
                    coin_name = p + "." + self.string_encode(n)
                    TxHash, amount_equal, utxo_found = self.selection_utxo(self.utxo_tokens, q, coin_name=coin_name)
                    total = qLovelace + self.change_min_utxo
                    balance = amount_equal - total
                    estimated_fee = 500000
                    if utxo_found and ((balance) <= estimated_fee):
                        TxHash.extend(self.selection_utxo(self.utxo_lovelace, abs(balance) + estimated_fee, coin_name="lovelace")[0])
            else:
                TxHash, amount_equal, utxo_found = self.selection_utxo(self.utxo_lovelace, qLovelace, coin_name="lovelace")
            
        return TxHash, amount_equal

    def add(self, TxHash: list[str]) -> list[str]:
        TxHash = list(set(TxHash))
        tx_in = len(TxHash) * ["--tx-in"]
        return list(chain(*zip(tx_in, TxHash)))

    def check(self) -> bool:
        if self.tLovelace != 0:
            return True
        else:
            return False
