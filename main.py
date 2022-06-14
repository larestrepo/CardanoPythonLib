from cardanopythonlib import base

keys = base.Keys()

# Option 1

# wallet_name = 'test02'
# nmemonic_size = 24
# keys.deriveAllKeys(wallet_name, size= nmemonic_size)


# Building multisig script
node = base.Node()
node.KEYS_FILE_PATH
wallet_id = 'wallet01'
node.get_transactions(wallet_id)

# hash= keys.keyHashing(wallet_id)
# node.create_multisig_script(wallet_id,'all','',[hash])
# node.create_policy_id(wallet_id)

address_origin ='addr_test1vqrfdj8fkzs0pxg0eu4p38apgd430stz5hafx7pnsxn0ccg4jqkyd'
address_destin = [
        {
          "address": "addr_test1qr2ac9vl2epy3yjynkqyfuskx6wp6ld70579v3s6wknve3rjkcctzvtrmt0chuqgaphal08kaqhn0gn295v7wefe95eqvl97xq",
          "amount": {
                "quantity": 50000000,
                "unit": "lovelace"
            },
          "assets": None,
        },
      ]
address_destin = None
metadata = None
witness = 1

mint = { "policyID": "ae6498eeb6f7f7bdd3b411c7d3bdf0dfd29f6b989382f9bdb1279638",
         "policy_path": '.priv/wallets/wallet01/wallet01.script',
         "tokens": [
          {"name": "Prueba4",
          "amount": 4575122544123},
         ]
        }



params = {
    "message": {
        "tx_info": {
            "address_origin": address_origin,
            "address_destin": address_destin,
            "change_address": address_origin,
            "metadata": metadata,
            "mint": mint,
            "script_path": None,
            "witness": witness,
        }
    }
}

result = node.build_tx_components(params)

sign_address_name = 'wallet01'
result = node.sign_transaction(sign_address_name)
result = node.submit_transaction()