from cardanopythonlib import base

# starter = base.Starter()
# print(starter.CARDANO_CLI_PATH)
# config_path = './cardano_config.ini'

node = base.Node()

print(node.query_tip_exec())

print(node.MINT_FOLDER)
# node.create_simple_script('MyFirstMultiSig','mint', 'all', 1, ['80b34df2162e9c4a38ce63322a8f903c9455a0bebd64c02cf1f3222a'])
# parameters = {
#     "name": "Myfinaltest",
#     "type": "atLeast",
#     "required": 1,
#     "hashes": ["80b34df2162e9c4a38ce63322a8f903c9455a0bebd64c02cf1f3222a"],
#     "type_time": "before",
#     "slot": 4983000,
#     "purpose": "mint",
# }
# node.create_simple_script(parameters=parameters)
# node.create_policy_id("mint", "Myfinaltest")
# policyid = node.create_policy_id("MyFirstMultiSig", 'mint')
# print(policyid)
# print(node.query_protocol())

# keys = base.Keys()
# keys.deriveAllKeys("wallet_name", size = 24, save_flag = False)
# keys.generate_mnemonic(size= 24)

# # Option 1

# wallet_name = 'receiving'
# nmemonic_size = 24
# # keys.generate_mnemonic()
# words = ['stock', 'pattern', 'fire', 'thought', 'denial', 'divorce', 'rocket', 'destroy', 'dog', 'weekend', 'twin', 'group', 'emerge', 'invest', 'muffin', 'outer', 'dress', 'mom', 'action', 'average', 'arrange', 'proud', 'piano', 'doctor']
# keys.deriveAllKeys(wallet_name, words = words)


# Building multisig script

# node.KEYS_FILE_PATH
# wallet_id = 'wallet01'
# print(node.query_tip_exec())
# node.get_transactions(wallet_name)
# print(node.analyze_tx('tx.draft'))

# hash= keys.keyHashing(wallet_id)
# node.create_multisig_script(wallet_id,'all','',[hash])
# node.create_policy_id(wallet_id)

# address_origin ='addr_test1vqrfdj8fkzs0pxg0eu4p38apgd430stz5hafx7pnsxn0ccg4jqkyd'
# address_origin ='addr_test1vp674jugprun0epvmep395k5hdpt689legmeh05s50kq8qcul3azr'
# address_destin = [
#         {
#           "address": "addr_test1qr2ac9vl2epy3yjynkqyfuskx6wp6ld70579v3s6wknve3rjkcctzvtrmt0chuqgaphal08kaqhn0gn295v7wefe95eqvl97xq",
#           "amount": {
#                 "quantity": 2379258,
#                 "unit": "lovelace"
#             },
#             "assets": [
#                 {
#                     "asset_name": "testtokens2",
#                     "amount": 123,
#                     "policyID": "1f4df2e4cb4c94705bed1312646d95c9b0f4ec342445619c65593601"
#                 },
#                 {
#                     "asset_name": "testtoken",
#                     "amount": 40,
#                     "policyID": "205a5880aebba0d1e330bb652114e3baea52542d4c0cb2defe26d5c9"
#                 },
#                 {
#                     "asset_name": "miprueba3",
#                     "amount": 1,
#                     "policyID": "7dd0bce9e78cb528ecde1bfd95d8b076b1bbc43436b5437a1e43ab3c"
#                 },
#                 {
#                     "asset_name": "miprueba3",
#                     "amount": 1,
#                     "policyID": "df3aaea99062110b5ebafe3a5054104561ea379c5039f4313b8e7222"
#                 },
#                 {
#                     "asset_name": "friday1002",
#                     "amount": 1,
#                     "policyID": "76277a33f1f3f12846c6aea8347e83fc6d7a0c0b8932139e9a7fb6e3"
#                 },
#                 {
#                     "asset_name": "miprueba",
#                     "amount": 47,
#                     "policyID": "ea3f8733d3fdf9b1b1efb5ed8559d337e46ef2b6a6f496e01f33c271"
#                 }
#             ]

#         },
#       ]
# # address_destin = None
# metadata =  {"1337": {
#         "name": "hello world",
#         "completed": 0
#     }}
# witness = 1

# mint = { "policyID": "ae6498eeb6f7f7bdd3b411c7d3bdf0dfd29f6b989382f9bdb1279638",
#          "policy_path": '.priv/wallets/wallet01/wallet01.script',
#          "tokens": [
#           {"name": "Pruebamil",
#           "amount": 452215},
#          ]
#         }

# mint = None

# metadata = None
# params = {
#     "message": {
#         "tx_info": {
#             "address_origin": address_origin,
#             "address_destin": None,
#             "change_address": address_origin,
#             "metadata": None,
#             "mint": None,
#             "script_path": None,
#             "witness": witness,
#         }
#     }
# }

# params =   {
#   "address_origin": "addr_test1vpsudqpk00kn4g6qzwm24re8gvtc2lvg2yr4gm52pu89wfqd7n25a",
#   "address_destin": [
#     {
#       "address": "addr_test1qz37wr0plpncl8ewpj305t0ysmrpgk6ef5r2lcmkq0gdrhw5fy5y35v9tscc8s6djv55yld5x29m6twdkeuzuqjmnx2s57fre9",
#       "amount": 2000000,
#       "tokens": [
#         {
#           "name": "ayllu",
#           "amount": 123,
#           "policyID": "e58ae630bfa049e1a5232bb69e4d0c8e85aaa03d5a304ac443a2e9a2"
#         }
#       ]
#     },
#     {
#       "address": "addr_test1qp9pqrswvsfkqd5kmurs7lvlv65jq9l2mefjtnsx3y5uwvepetzja2kx6fwmlcasy995ppa5yhdr2sksfgas63d846hshmc704",
#       "amount": 2000000,
#       "tokens": [
#         {
#           "name": "ayllu",
#           "amount": 12,
#           "policyID": "e58ae630bfa049e1a5232bb69e4d0c8e85aaa03d5a304ac443a2e9a2"
#         }
#       ]
#     }
#   ],
#   "change_address": "addr_test1qz6xn4nsf9qh44pf327heujp0aq0n2vl4fu37sgl4uxstpfpetzja2kx6fwmlcasy995ppa5yhdr2sksfgas63d846hskdgyvu",
#   "metadata": {},
#   "mint": {
#     "policyID": "e58ae630bfa049e1a5232bb69e4d0c8e85aaa03d5a304ac443a2e9a2",
#     "policy_path": "./.priv/scripts/mint/aylluMinting.script",
#     "validity_interval": None,
#     "tokens": [
#       {
#         "name": "ayllu",
#         "amount": 135
#       }
#     ]
#   },
#   "script_path": "./.priv/scripts/mint/aylluMinting.script",
#   "witness": 2
# }

# result = node.build_tx_components(params)

# print(result)

# # sign_address_name = 'wallet01'
# result = node.sign_transaction(wallet_name)
# result = node.submit_transaction()
# import ast
# response = node.get_txid_body()
# print(response)
# response = node.get_txid_signed()
# print(response)
# response = node.analyze_tx_body()
# print(response)
# response = node.analyze_tx_signed()
# # response = json.dumps(response)
# response = ast.literal_eval(response)
# print(response)

# params = {
#   "address_origin": "addr_test1vzqtxn0jzchfcj3cee3ny250jq7fg4dqh67kfspv78ejy2scj24vv",
#   "address_destin": [
#     {
#       "address": "addr_test1qq76wsvtpw3a67mcdq93fv4d6hpk872meclggqjljwrdavq95yaattr99dteap4y7rqjr80ujvuguegc72rqjfs25mfs8vtrae",
#       "amount": {
#         "quantity": 2000000,
#         "unit": "lovelace"
#       },
#       "assets": [

#       ]
#     }
#   ],
#   "metadata": {{"1337": {
#         "name": "hello world",
#         "completed": 0
#     }}},
#   "witness": 1
# }

# result = node.analyze_tx_body()
# result = node.analyze_tx_signed()
# result = node.get_txid_body()
result = node.get_tx_info("9900f38bb17ed9a91111f5de61a9e8a4a540f85b0af4d0804a83ad3ee1fccefa",0)
print(result)

import json
with open('./.priv/transactions/tx_info.json', 'r') as file:
  tx_info = json.load(file)

print(tx_info)

address_origin = 'addr_test1vpsudqpk00kn4g6qzwm24re8gvtc2lvg2yr4gm52pu89wfqd7n25a'
# metadata = {"1337": {"name": "hello world", "completed": 0}}
address_destin_no_tokens = [
  {
      "address": "addr_test1vp9pqrswvsfkqd5kmurs7lvlv65jq9l2mefjtnsx3y5uwvcahgzxk",
      "amount": 3000000,
      "tokens": [],
  }]
inline_datum = {
    "constructor": 0,
    "fields": [{
"int": 42
    }]
}

params = {
            "address_origin": address_origin,
            "address_destin": address_destin_no_tokens,
            "change_address": address_origin,
            # "metadata": metadata,
            # "mint": None,
            # "script_path": None,
            # "witness": 1,
            "inline_datum": inline_datum,
        }

result = node.build_tx_components(params)
print(result)

sign_address_name = 'AylluPayment'
result = node.sign_transaction([sign_address_name])
result = node.submit_transaction()
