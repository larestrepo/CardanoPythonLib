from cardanopythonlib import base

# starter = base.Starter()
# print(starter.CARDANO_CLI_PATH)
# config_path = './cardano_config.ini'

node = base.Node()

print(node.MINT_FOLDER)
# node.create_simple_script('MyFirstMultiSig','mint', 'all', 1, ['80b34df2162e9c4a38ce63322a8f903c9455a0bebd64c02cf1f3222a'])
parameters = {
    "name": "Myfinaltest",
    "type": "atLeast",
    "required": 1,
    "hashes": ["80b34df2162e9c4a38ce63322a8f903c9455a0bebd64c02cf1f3222a"],
    "type_time": "before",
    "slot": 4983000,
    "purpose": "mint"
    }
node.create_simple_script(parameters=parameters)
node.create_policy_id('mint','Myfinaltest')
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

# result = node.build_tx_components(params)

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

params = {
    'address_origin': 'addr_test1vzqtxn0jzchfcj3cee3ny250jq7fg4dqh67kfspv78ejy2scj24vv', 
    'address_destin': [{'address': 'addr_test1qrhdv4zc4mqpkh6qsvp3chgu9kluz9ctyex0kmklja9upwnnw0ll60v9pxn8507976e6w5rwvkm988jw0mhlyujrzt0s0n2udv', 'amount': {'quantity': 25000000, 'unit': 'lovelace'}, 'assets': []}], 
    'change_address': 'addr_test1vzqtxn0jzchfcj3cee3ny250jq7fg4dqh67kfspv78ejy2scj24vv', 
    'metadata': {'1337': {
        'name': 'hello world',
        'completed': 0
    }}, 
    'mint': None, 
    'script_path': None, 
    'witness': 1}

result = node.build_tx_components(params)