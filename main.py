from cardanopythonlib import base

# starter = base.Starter()
# print(starter.CARDANO_CLI_PATH)
# config_path = "./cardano_config.ini"

node = base.Node()

print(node.query_tip_exec())

print(node.MINT_FOLDER)
# node.create_simple_script("MyFirstMultiSig","mint", "all", 1, ["80b34df2162e9c4a38ce63322a8f903c9455a0bebd64c02cf1f3222a"])
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
# policyid = node.create_policy_id("MyFirstMultiSig", "mint")
# print(policyid)
# print(node.query_protocol())

# keys = base.Keys()
# keys.deriveAllKeys("wallet_name", size = 24, save_flag = False)
# keys.generate_mnemonic(size= 24)

# # Option 1

# wallet_name = "receiving"
# nmemonic_size = 24
# # keys.generate_mnemonic()
# words = ["stock", "pattern", "fire", "thought", "denial", "divorce", "rocket", "destroy", "dog", "weekend", "twin", "group", "emerge", "invest", "muffin", "outer", "dress", "mom", "action", "average", "arrange", "proud", "piano", "doctor"]
# keys.deriveAllKeys("test_wallet", words, True)


# Building multisig script

# node.KEYS_FILE_PATH
# wallet_id = "wallet01"
# print(node.query_tip_exec())
# node.get_transactions(wallet_name)
# print(node.analyze_tx("tx.draft"))

# hash= keys.keyHashing(wallet_id)
# node.create_multisig_script(wallet_id,"all","",[hash])
# node.create_policy_id(wallet_id)

# address_origin ="addr_test1vqrfdj8fkzs0pxg0eu4p38apgd430stz5hafx7pnsxn0ccg4jqkyd"
# address_origin ="addr_test1vp674jugprun0epvmep395k5hdpt689legmeh05s50kq8qcul3azr"
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
#          "policy_path": ".priv/wallets/wallet01/wallet01.script",
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

# # sign_address_name = "wallet01"
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
inline_datum = {"constructor": 0, "fields": [{"int": 42}]}
inline_datum = {
    "constructor": 0,
    "fields": [
        {
            "bytes": "c338509bed524537ffbd8412678339b302d5a57c4dcf666ee5f15c8c"
        },
        {
            "int": 1675357237
        },
        {
            "constructor": 0,
            "fields": [
                {
                    "constructor": 0,
                    "fields": [
                        {
                            "map": [
                                {
                                    "v": {
                                        "bytes": "29d222ce763455e3d7a09a665ce554f00ac89d2e99a1a83d267170c64d494e"
                                    },
                                    "k": {
                                        "int": 1
                                    }
                                },
                                {
                                    "v": {
                                        "bytes": "4d494e"
                                    },
                                    "k": {
                                        "int": 2
                                    }
                                },
                                {
                                    "v": {
                                        "int": 792
                                    },
                                    "k": {
                                        "int": 3
                                    }
                                }
                            ]
                        }
                    ]
                },
                {
                    "constructor": 0,
                    "fields": [
                        {
                            "map": [
                                {
                                    "v": {
                                        "bytes": "1d7f33bd23d85e1a25d87d86fac4f199c3197a2f7afeb662a0f34e1e776f726c646d6f62696c65746f6b656e"
                                    },
                                    "k": {
                                        "int": 1
                                    }
                                },
                                {
                                    "v": {
                                        "bytes": "574d54"
                                    },
                                    "k": {
                                        "int": 2
                                    }
                                },
                                {
                                    "v": {
                                        "int": 7660
                                    },
                                    "k": {
                                        "int": 3
                                    }
                                }
                            ]
                        }
                    ]
                },
                {
                    "constructor": 0,
                    "fields": [
                        {
                            "map": [
                                {
                                    "v": {
                                        "bytes": "da8c30857834c6ae7203935b89278c532b3995245295456f993e1d244c51"
                                    },
                                    "k": {
                                        "int": 1
                                    }
                                },
                                {
                                    "v": {
                                        "bytes": "4c51"
                                    },
                                    "k": {
                                        "int": 2
                                    }
                                },
                                {
                                    "v": {
                                        "int": 547624
                                    },
                                    "k": {
                                        "int": 3
                                    }
                                }
                            ]
                        }
                    ]
                },
                {
                    "constructor": 0,
                    "fields": [
                        {
                            "map": [
                                {
                                    "v": {
                                        "bytes": "8fef2d34078659493ce161a6c7fba4b56afefa8535296a5743f6958741414441"
                                    },
                                    "k": {
                                        "int": 1
                                    }
                                },
                                {
                                    "v": {
                                        "bytes": "41414441"
                                    },
                                    "k": {
                                        "int": 2
                                    }
                                },
                                {
                                    "v": {
                                        "int": 13549
                                    },
                                    "k": {
                                        "int": 3
                                    }
                                }
                            ]
                        }
                    ]
                },
                {
                    "constructor": 0,
                    "fields": [
                        {
                            "map": [
                                {
                                    "v": {
                                        "bytes": "6ac8ef33b510ec004fe11585f7c5a9f0c07f0c23428ab4f29c1d7d104d454c44"
                                    },
                                    "k": {
                                        "int": 1
                                    }
                                },
                                {
                                    "v": {
                                        "bytes": "4d454c44"
                                    },
                                    "k": {
                                        "int": 2
                                    }
                                },
                                {
                                    "v": {
                                        "int": 947
                                    },
                                    "k": {
                                        "int": 3
                                    }
                                }
                            ]
                        }
                    ]
                },
                {
                    "constructor": 0,
                    "fields": [
                        {
                            "map": [
                                {
                                    "v": {
                                        "bytes": "f43a62fdc3965df486de8a0d32fe800963589c41b38946602a0dc53541474958"
                                    },
                                    "k": {
                                        "int": 1
                                    }
                                },
                                {
                                    "v": {
                                        "bytes": "41474958"
                                    },
                                    "k": {
                                        "int": 2
                                    }
                                },
                                {
                                    "v": {
                                        "int": 8004
                                    },
                                    "k": {
                                        "int": 3
                                    }
                                }
                            ]
                        }
                    ]
                },
                {
                    "constructor": 0,
                    "fields": [
                        {
                            "map": [
                                {
                                    "v": {
                                        "bytes": "533bb94a8850ee3ccbe483106489399112b74c905342cb1792a797a0494e4459"
                                    },
                                    "k": {
                                        "int": 1
                                    }
                                },
                                {
                                    "v": {
                                        "bytes": "494e4459"
                                    },
                                    "k": {
                                        "int": 2
                                    }
                                },
                                {
                                    "v": {
                                        "int": 53170
                                    },
                                    "k": {
                                        "int": 3
                                    }
                                }
                            ]
                        }
                    ]
                },
                {
                    "constructor": 0,
                    "fields": [
                        {
                            "map": [
                                {
                                    "v": {
                                        "bytes": "25f0fc240e91bd95dcdaebd2ba7713fc5168ac77234a3d79449fc20c534f4349455459"
                                    },
                                    "k": {
                                        "int": 1
                                    }
                                },
                                {
                                    "v": {
                                        "bytes": "534f4349455459"
                                    },
                                    "k": {
                                        "int": 2
                                    }
                                },
                                {
                                    "v": {
                                        "int": 1008
                                    },
                                    "k": {
                                        "int": 3
                                    }
                                }
                            ]
                        }
                    ]
                },
                {
                    "constructor": 0,
                    "fields": [
                        {
                            "map": [
                                {
                                    "v": {
                                        "bytes": "884892bcdc360bcef87d6b3f806e7f9cd5ac30d999d49970e7a903ae5041564941"
                                    },
                                    "k": {
                                        "int": 1
                                    }
                                },
                                {
                                    "v": {
                                        "bytes": "5041564941"
                                    },
                                    "k": {
                                        "int": 2
                                    }
                                },
                                {
                                    "v": {
                                        "int": 411
                                    },
                                    "k": {
                                        "int": 3
                                    }
                                }
                            ]
                        }
                    ]
                },
                {
                    "constructor": 0,
                    "fields": [
                        {
                            "map": [
                                {
                                    "v": {
                                        "bytes": "b6a7467ea1deb012808ef4e87b5ff371e85f7142d7b356a40d9b42a0436f726e75636f70696173205b76696120436861696e506f72742e696f5d"
                                    },
                                    "k": {
                                        "int": 1
                                    }
                                },
                                {
                                    "v": {
                                        "bytes": "434f5049"
                                    },
                                    "k": {
                                        "int": 2
                                    }
                                },
                                {
                                    "v": {
                                        "int": 873
                                    },
                                    "k": {
                                        "int": 3
                                    }
                                }
                            ]
                        }
                    ]
                },
                {
                    "constructor": 0,
                    "fields": [
                        {
                            "map": [
                                {
                                    "v": {
                                        "bytes": "38ad9dc3aec6a2f38e220142b9aa6ade63ebe71f65e7cc2b7d8a8535434c4159"
                                    },
                                    "k": {
                                        "int": 1
                                    }
                                },
                                {
                                    "v": {
                                        "bytes": "434c4159"
                                    },
                                    "k": {
                                        "int": 2
                                    }
                                },
                                {
                                    "v": {
                                        "int": 496
                                    },
                                    "k": {
                                        "int": 3
                                    }
                                }
                            ]
                        }
                    ]
                },
                {
                    "constructor": 0,
                    "fields": [
                        {
                            "map": [
                                {
                                    "v": {
                                        "bytes": "6f46e1304b16d884c85c62fb0eef35028facdc41aaa0fd319a152ed64d434f53"
                                    },
                                    "k": {
                                        "int": 1
                                    }
                                },
                                {
                                    "v": {
                                        "bytes": "4d434f53"
                                    },
                                    "k": {
                                        "int": 2
                                    }
                                },
                                {
                                    "v": {
                                        "int": 803
                                    },
                                    "k": {
                                        "int": 3
                                    }
                                }
                            ]
                        }
                    ]
                },
                {
                    "constructor": 0,
                    "fields": [
                        {
                            "map": [
                                {
                                    "v": {
                                        "bytes": "a0028f350aaabe0545fdcb56b039bfb08e4bb4d8c4d7c3c7d481c235484f534b59"
                                    },
                                    "k": {
                                        "int": 1
                                    }
                                },
                                {
                                    "v": {
                                        "bytes": "484f534b59"
                                    },
                                    "k": {
                                        "int": 2
                                    }
                                },
                                {
                                    "v": {
                                        "int": 0
                                    },
                                    "k": {
                                        "int": 3
                                    }
                                }
                            ]
                        }
                    ]
                },
                {
                    "constructor": 0,
                    "fields": [
                        {
                            "map": [
                                {
                                    "v": {
                                        "bytes": "ce5b9e0f8a88255b65f2e4d065c6e716e9fa9a8a86dfb86423dd1ac044494e47"
                                    },
                                    "k": {
                                        "int": 1
                                    }
                                },
                                {
                                    "v": {
                                        "bytes": "44494e47"
                                    },
                                    "k": {
                                        "int": 2
                                    }
                                },
                                {
                                    "v": {
                                        "int": 367
                                    },
                                    "k": {
                                        "int": 3
                                    }
                                }
                            ]
                        }
                    ]
                },
                {
                    "constructor": 0,
                    "fields": [
                        {
                            "map": [
                                {
                                    "v": {
                                        "bytes": "8e51398904a5d3fc129fbf4f1589701de23c7824d5c90fdb9490e15a434841524c4933"
                                    },
                                    "k": {
                                        "int": 1
                                    }
                                },
                                {
                                    "v": {
                                        "bytes": "4333"
                                    },
                                    "k": {
                                        "int": 2
                                    }
                                },
                                {
                                    "v": {
                                        "int": 6460
                                    },
                                    "k": {
                                        "int": 3
                                    }
                                }
                            ]
                        }
                    ]
                },
                {
                    "constructor": 0,
                    "fields": [
                        {
                            "map": [
                                {
                                    "v": {
                                        "bytes": "10a49b996e2402269af553a8a96fb8eb90d79e9eca79e2b4223057b64745524f"
                                    },
                                    "k": {
                                        "int": 1
                                    }
                                },
                                {
                                    "v": {
                                        "bytes": "4745524f"
                                    },
                                    "k": {
                                        "int": 2
                                    }
                                },
                                {
                                    "v": {
                                        "int": 292
                                    },
                                    "k": {
                                        "int": 3
                                    }
                                }
                            ]
                        }
                    ]
                },
                {
                    "constructor": 0,
                    "fields": [
                        {
                            "map": [
                                {
                                    "v": {
                                        "bytes": "5dac8536653edc12f6f5e1045d8164b9f59998d3bdc300fc928434894e4d4b52"
                                    },
                                    "k": {
                                        "int": 1
                                    }
                                },
                                {
                                    "v": {
                                        "bytes": "4e4d4b52"
                                    },
                                    "k": {
                                        "int": 2
                                    }
                                },
                                {
                                    "v": {
                                        "int": 85
                                    },
                                    "k": {
                                        "int": 3
                                    }
                                }
                            ]
                        }
                    ]
                },
                {
                    "constructor": 0,
                    "fields": [
                        {
                            "map": [
                                {
                                    "v": {
                                        "bytes": "078eafce5cd7edafdf63900edef2c1ea759e77f30ca81d6bbdeec92479756d6d69"
                                    },
                                    "k": {
                                        "int": 1
                                    }
                                },
                                {
                                    "v": {
                                        "bytes": "59554d4d49"
                                    },
                                    "k": {
                                        "int": 2
                                    }
                                },
                                {
                                    "v": {
                                        "int": 30
                                    },
                                    "k": {
                                        "int": 3
                                    }
                                }
                            ]
                        }
                    ]
                },
                {
                    "constructor": 0,
                    "fields": [
                        {
                            "map": [
                                {
                                    "v": {
                                        "bytes": "804f5544c1962a40546827cab750a88404dc7108c0f588b72964754f56594649"
                                    },
                                    "k": {
                                        "int": 1
                                    }
                                },
                                {
                                    "v": {
                                        "bytes": "56594649"
                                    },
                                    "k": {
                                        "int": 2
                                    }
                                },
                                {
                                    "v": {
                                        "int": 4393
                                    },
                                    "k": {
                                        "int": 3
                                    }
                                }
                            ]
                        }
                    ]
                },
                {
                    "constructor": 0,
                    "fields": [
                        {
                            "map": [
                                {
                                    "v": {
                                        "bytes": "8a1cfae21368b8bebbbed9800fec304e95cce39a2a57dc35e2e3ebaa4d494c4b"
                                    },
                                    "k": {
                                        "int": 1
                                    }
                                },
                                {
                                    "v": {
                                        "bytes": "4d494c4b"
                                    },
                                    "k": {
                                        "int": 2
                                    }
                                },
                                {
                                    "v": {
                                        "int": 37559
                                    },
                                    "k": {
                                        "int": 3
                                    }
                                }
                            ]
                        }
                    ]
                },
                {
                    "constructor": 0,
                    "fields": [
                        {
                            "map": [
                                {
                                    "v": {
                                        "bytes": "9a9693a9a37912a5097918f97918d15240c92ab729a0b7c4aa144d7753554e444145"
                                    },
                                    "k": {
                                        "int": 1
                                    }
                                },
                                {
                                    "v": {
                                        "bytes": "53554e444145"
                                    },
                                    "k": {
                                        "int": 2
                                    }
                                },
                                {
                                    "v": {
                                        "int": 721
                                    },
                                    "k": {
                                        "int": 3
                                    }
                                }
                            ]
                        }
                    ]
                },
                {
                    "constructor": 0,
                    "fields": [
                        {
                            "map": [
                                {
                                    "v": {
                                        "bytes": "d5dec6074942b36b50975294fd801f7f28c907476b1ecc1b57c916ed524154"
                                    },
                                    "k": {
                                        "int": 1
                                    }
                                },
                                {
                                    "v": {
                                        "bytes": "524154"
                                    },
                                    "k": {
                                        "int": 2
                                    }
                                },
                                {
                                    "v": {
                                        "int": 166
                                    },
                                    "k": {
                                        "int": 3
                                    }
                                }
                            ]
                        }
                    ]
                },
                {
                    "constructor": 0,
                    "fields": [
                        {
                            "map": [
                                {
                                    "v": {
                                        "bytes": "6787a47e9f73efe4002d763337140da27afa8eb9a39413d2c39d4286524144546f6b656e73"
                                    },
                                    "k": {
                                        "int": 1
                                    }
                                },
                                {
                                    "v": {
                                        "bytes": "524144"
                                    },
                                    "k": {
                                        "int": 2
                                    }
                                },
                                {
                                    "v": {
                                        "int": 4
                                    },
                                    "k": {
                                        "int": 3
                                    }
                                }
                            ]
                        }
                    ]
                },
                {
                    "constructor": 0,
                    "fields": [
                        {
                            "map": [
                                {
                                    "v": {
                                        "bytes": "af2e27f580f7f08e93190a81f72462f153026d06450924726645891b44524950"
                                    },
                                    "k": {
                                        "int": 1
                                    }
                                },
                                {
                                    "v": {
                                        "bytes": "44524950"
                                    },
                                    "k": {
                                        "int": 2
                                    }
                                },
                                {
                                    "v": {
                                        "int": 8
                                    },
                                    "k": {
                                        "int": 3
                                    }
                                }
                            ]
                        }
                    ]
                },
                {
                    "constructor": 0,
                    "fields": [
                        {
                            "map": [
                                {
                                    "v": {
                                        "bytes": "c0ee29a85b13209423b10447d3c2e6a50641a15c57770e27cb9d507357696e67526964657273"
                                    },
                                    "k": {
                                        "int": 1
                                    }
                                },
                                {
                                    "v": {
                                        "bytes": "575254"
                                    },
                                    "k": {
                                        "int": 2
                                    }
                                },
                                {
                                    "v": {
                                        "int": 5812
                                    },
                                    "k": {
                                        "int": 3
                                    }
                                }
                            ]
                        }
                    ]
                },
                {
                    "constructor": 0,
                    "fields": [
                        {
                            "map": [
                                {
                                    "v": {
                                        "bytes": "628436be6fa349ebf4ac3d749e87a36981b930d4bb4319c11e64042c464c5a"
                                    },
                                    "k": {
                                        "int": 1
                                    }
                                },
                                {
                                    "v": {
                                        "bytes": "464c5a"
                                    },
                                    "k": {
                                        "int": 2
                                    }
                                },
                                {
                                    "v": {
                                        "int": 13
                                    },
                                    "k": {
                                        "int": 3
                                    }
                                }
                            ]
                        }
                    ]
                }
            ]
        }
    ]
}

address_origin = "addr_test1vpsudqpk00kn4g6qzwm24re8gvtc2lvg2yr4gm52pu89wfqd7n25a"

params = {
    "address_origin": "addr_test1vpsudqpk00kn4g6qzwm24re8gvtc2lvg2yr4gm52pu89wfqd7n25a",
    "address_destin": [
        {
        "address": "addr_test1vp674jugprun0epvmep395k5hdpt689legmeh05s50kq8qcul3azr",
        "amount": 1000000000,
      },
    ],
    # "inline_datum": inline_datum,
}

# params = {
#     "address_origin": address_origin,
#     # "address_destin": address_destin_no_tokens,
#     "change_address": address_origin,
#     # "metadata": metadata,
#     # "mint": None,
#     # "script_path": None,
#     # "witness": 1,
#     "inline_datum": inline_datum,
# }

result = node.build_tx_components(params)
print(result)

sign_address_name = "AylluPayment"
result = node.sign_transaction([sign_address_name])
result = node.submit_transaction()
