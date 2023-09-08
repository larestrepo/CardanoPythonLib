import os
import sys
import unittest
import time

from cardanopythonlib import base
from cardanopythonlib.path_utils import remove_file

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "cardanopythonlib"))


class TestLibrary(unittest.TestCase):
    def setUp(self):
        self.config_path = "cardanopythonlib/config/cardano_config.ini"
        self.starter = base.Starter()
        self.node = base.Node()
        self.wallet_name = "test_wallet"
        self.address_origin = (
            "addr_test1vqkge7txl2vdw26efyv7cytjl8l6n8678kz09agc0r34pdss0xtmp"
        )
        self.source = base.Source("addr_test1vqkge7txl2vdw26efyv7cytjl8l6n8678kz09agc0r34pdss0xtmp")
        self.metadata = {"1337": {"name": "hello world", "completed": 0}}
        self.address_destin_no_tokens = [
            {
                "address": "addr_test1qp674jugprun0epvmep395k5hdpt689legmeh05s50kq8qc0wx9lg9h8x72hctqg34gy2eygnlrf7nyf343w34r67hjskugtxl",
                "amount": 3000000,
                # "tokens": [],
            }
        ]
        self.address_destin_with_tokens = [
            {
                "address": "addr_test1qp674jugprun0epvmep395k5hdpt689legmeh05s50kq8qc0wx9lg9h8x72hctqg34gy2eygnlrf7nyf343w34r67hjskugtxl",
                "tokens": [{

                    "name": "MyTestEMG",
                    "amount": 1,
                    "policyID": "3547253f769b35cd318e062f7ade5b4ceb43462beb3f12ac18ce536b"
                }
                ],
            },
        ]
        self.inline_datum = {
    "constructor": 0,
    "fields": [
        {
            "bytes": "c338509bed524537ffbd8412678339b302d5a57c4dcf666ee5f15c8c"
        },
        {
            "int": 1676391853
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
                                        "int": 938
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
                                        "int": 8157
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
                                        "int": 459964
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
                                        "int": 13459
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
                                        "int": 18511
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
                                        "int": 92320
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
                                        "int": 740
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
                                        "int": 436
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
                                        "int": 1180
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
                                        "int": 515
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
                                        "int": 682
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
                                        "int": 6046
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
                                        "int": 277
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
                                        "int": 84
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
                                        "int": 26
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
                                        "int": 5168
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
                                        "int": 30419
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
                                        "int": 940
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
                                        "int": 169
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
                                        "int": 7
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
                                        "int": 7473
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
                                        "int": 7
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
        # self.inline_datum = {"constructor": 0, "fields": [{"int": 42}]}
        self.script_name = "script_name"
        self.policyID = "cc8df048ecf8d32149269767c961aa193d89208844e876bdef186c9f"
        self.script_file_path = "./priv/example/example.script"
        self.type_time = "before"
        self.slot = 39874005
        self.purpose = "mint"

    #####################################
    # This is the start of the section to test Starter class and Keys class
    #####################################


    def test_query_tip_exec(self):
        tip = self.node.query_tip_exec()
        self.assertIs(type(tip), dict, "Verify that your node is running")
        self.assertEqual(
            tip["era"], "Babbage", "Verify that your node is in Alonzo era"
        )
        self.assertEqual(
            tip["syncProgress"],
            "100.00",
            f"Verify that your node is in sync. Current progress: {tip['syncProgress']}",
        )

    # def test_utxo_selection(self):
    #     mock_transactions = [
    #         {
    #             "hash": "0d085c60b8db224e43608886250d524ceee17f4b4b1091aec879e40135975644",
    #             "id": "0",
    #             "amounts": [{"token": "lovelace", "amount": "2000000"}],
    #         },
    #         {
    #             "hash": "496602485616c1b636461762f1e41084f863a51847ecc9fbc30a504d28b8917b",
    #             "id": "0",
    #             "amounts": [{"token": "lovelace", "amount": "1000000000"}],
    #         },
    #         {
    #             "hash": "c2e7b4319abc56ba57ba1c044a36aac3613b71c1131ab30f86e16ba0ffba9c12",
    #             "id": "0",
    #             "amounts": [
    #                 {"token": "lovelace", "amount": "2000000"},
    #                 {
    #                     "token": "3547253f769b35cd318e062f7ade5b4ceb43462beb3f12ac18ce536b.4d7954657374454d47",
    #                     "amount": "1",
    #                 },
    #             ],
    #         },
    #     ]
    #     utxo_tokens = list(filter(lambda utxo: len(utxo["amounts"]) != 1, mock_transactions))
    #     txHash_in = self.source.selection_utxo(utxo_tokens, 3000000) # Send lovelace
    #     self.assertTrue(
    #         txHash_in == (['496602485616c1b636461762f1e41084f863a51847ecc9fbc30a504d28b8917b#0'], 1000000000),
    #         "Wrong selection in assert 1. Send lovelace"
    #     )
    #     txHash_in = self.source.selection_utxo(mock_transactions, 2000000) # Send lovelace
    #     self.assertTrue(
    #         txHash_in == (['496602485616c1b636461762f1e41084f863a51847ecc9fbc30a504d28b8917b#0'], 1000000000),
    #         "Wrong selection in assert 2. Send lovelace"
    #     )
    #     txHash_in = self.source.selection_utxo(mock_transactions, 1000000) # Send lovelace
    #     self.assertTrue(
    #         txHash_in == (['0d085c60b8db224e43608886250d524ceee17f4b4b1091aec879e40135975644#0'], 2000000),
    #         "Wrong selection in assert 3. Send lovelace"
    #     )
    #     txHash_in = self.source.selection_utxo(mock_transactions, 1000000000) # Send lovelace
    #     self.assertTrue(
    #         txHash_in == (['496602485616c1b636461762f1e41084f863a51847ecc9fbc30a504d28b8917b#0', '0d085c60b8db224e43608886250d524ceee17f4b4b1091aec879e40135975644#0'], 1002000000),
    #         "Wrong selection in assert 4. Send lovelace"
    #     )
    #     txHash_in = self.source.selection_utxo(mock_transactions, 2000000)# Mint token. It should take the utxo with enough balance and without tokens
    #     self.assertTrue(
    #         txHash_in == (['496602485616c1b636461762f1e41084f863a51847ecc9fbc30a504d28b8917b#0'], 1000000000),
    #         "Wrong selection in assert 5. Mint token. It should take the utxo with enough balance and without tokens"
    #     )

    #     txHash_in = self.source.selection_utxo(mock_transactions, 1, coin_name="3547253f769b35cd318e062f7ade5b4ceb43462beb3f12ac18ce536b.4d7954657374454d47") # If coin name specified with default action it means that the token is to be sent"
    #     self.assertTrue(
    #         txHash_in == (['c2e7b4319abc56ba57ba1c044a36aac3613b71c1131ab30f86e16ba0ffba9c12#0'], 2000000),
    #         "Wrong selection in assert 6. If coin name specified with default action it means that the token is to be sent"
    #     )
    #     txHash_in = self.source.selection_utxo(mock_transactions, 1, coin_name="3547253f769b35cd318e062f7ade5b4ceb43462beb3f12ac18ce536b.4d7954657374454d47") # Burn if coin name specified with action = "Burn"
    #     self.assertTrue(
    #         txHash_in == (['c2e7b4319abc56ba57ba1c044a36aac3613b71c1131ab30f86e16ba0ffba9c12#0'], 2000000),
    #         "Wrong selection in assert 6. Burn if coin name specified with action = Burn"
    #     )

    def test_create_multisig_script(self):
        type = "all"
        required = ""
        hashes = [
            "f8bd3d31f018921f7dd73d21fd7a2f5767483d3f4c960c88d16e807f",
            "955df18bcefaf6f7b956c2299633a75dfd3153451a56bd9676fd58a7",
            "0696c8e9b0a0f0990fcf2a189fa1436b17c162a5fa93783381a6fc61",
        ]
        # type_time = "before"
        slot = self.node.query_tip_exec()["slot"] + 20000
        purpose = "mint"
        parameters = {
            "type": type,
            "required": required,
            "hashes": hashes,
            "type_time": self.type_time,
            "slot": slot,
            "purpose": purpose,
        }
        multisig_script, policyID = self.node.create_simple_script(parameters)
        try:
            assert multisig_script != None
            assert policyID != None

            self.assertEqual(
                multisig_script["type"], type, "Review the type of the multisig script"
            )
            if required == "":
                self.assertIn(
                    multisig_script["type"],
                    ["all", "any"],
                    "Review the type of the multisig script and the required field",
                )
            else:
                self.assertIs(
                    multisig_script["required"],
                    int,
                    "Review the number of required signatures",
                )
            self.assertEqual(
                len(multisig_script["scripts"]),
                len(hashes),
                "Review that the number of wallets corresponds",
            )

            script_file_path = self.starter.MINT_FOLDER
            self.assertIn(purpose, script_file_path)
            # keys_file_path = self.starter.KEYS_FILE_PATH + "/" + script_name
            file_exists = os.path.exists(script_file_path)

            remove_file(script_file_path, "/" + policyID + ".script")
            remove_file(script_file_path, "/" + policyID + ".policyid")

            self.assertEqual(
                len(policyID.split(" ")), 1, f"Verify the existence of the script file"
            )
            self.assertTrue(
                file_exists,
                f"Verify the creation of the policy script file in {script_file_path}",
            )
            self.assertEqual(
                len(policyID), 56, "Problem with the generation of the PolicyID"
            )
        except AssertionError:
            print(f"Verify your required field")

    def test_create_simple_script(self):
        type = "all"
        hashes = ["f8bd3d31f018921f7dd73d21fd7a2f5767483d3f4c960c88d16e807f"]
        # type_time = "before"
        slot = self.node.query_tip_exec()["slot"] + 20000
        parameters = {
            "type": type,
            "hashes": hashes,
            "purpose": self.purpose,
            "type_time": self.type_time,
            "slot": slot,
        }
        multisig_script, policyID = self.node.create_simple_script(parameters)
        try:
            assert multisig_script != None
            assert policyID != None

            script_file_path = self.starter.MINT_FOLDER
            file_exists = os.path.exists(script_file_path)

            remove_file(script_file_path, "/" + policyID + ".script")
            remove_file(script_file_path, "/" + policyID + ".policyid")

            self.assertEqual(
                multisig_script["type"], type, "Review the type of the multisig script"
            )
            script = multisig_script["scripts"]
            for item in script:
                if slot in item.keys():
                    script.pop(item)

            self.assertEqual(
                len(script),
                len(hashes),
                "Review that the number of wallets corresponds",
            )

            self.assertEqual(
                len(policyID.split(" ")), 1, f"Verify the existence of the script file"
            )
            self.assertTrue(
                file_exists,
                f"Verify the creation of the policy script file in {script_file_path}",
            )
            self.assertEqual(
                len(policyID), 56, "Problem with the generation of the PolicyID"
            )
        except AssertionError:
            print(f"Verify your required field")

    def test_build_tx(self):
        tx_file_path = self.starter.TRANSACTION_PATH_FILE
        remove_file(tx_file_path, "/tx.draft")
        address_origin = self.address_origin
        params = {
            "address_origin": address_origin,
            # "address_destin": None,
            "change_address": address_origin,
            # "metadata": None,
            # "mint": None,
            # "script_path": None,
            # "witness": 1,
        }
        response = self.node.build_tx_components(params)

        file_exists = os.path.exists(tx_file_path + "/tx.draft")

        remove_file(tx_file_path, "/tx.draft")
        remove_file(tx_file_path, "/tx_metadata")

        self.assertTrue(
            file_exists,
            f"Verify the creation of the transaction draft file in {tx_file_path}",
        )
        self.assertIn(
            "Estimated transaction fee: Lovelace",
            response,
            "Failed to build the transaction",
        )

    def test_build_tx_metadata(self):
        tx_file_path = self.starter.TRANSACTION_PATH_FILE
        remove_file(tx_file_path, "/tx.draft")
        params = {
            "address_origin": self.address_origin,
            # "address_destin": None,
            "change_address": self.address_origin,
            "metadata": self.metadata,
            # "mint": None,
            # "script_path": None,
            # "witness": 1,
        }
        response = self.node.build_tx_components(params)
        file_exists = os.path.exists(tx_file_path + "/tx.draft")

        remove_file(tx_file_path, "/tx.draft")
        remove_file(tx_file_path, "/tx_metadata")

        self.assertTrue(
            file_exists,
            f"Verify the creation of the transaction draft file in {tx_file_path}",
        )
        self.assertIn(
            "Estimated transaction fee: Lovelace",
            response,
            "Failed to build the transaction",
        )

    def test_build_tx_destin_no_tokens(self):
        tx_file_path = self.starter.TRANSACTION_PATH_FILE
        remove_file(tx_file_path, "/tx.draft")
        params = {
            "address_origin": self.address_origin,
            "address_destin": self.address_destin_no_tokens,
            "change_address": self.address_origin,
            "metadata": self.metadata,
            # "mint": None,
            # "script_path": None,
            # "witness": 1,
        }
        response = self.node.build_tx_components(params)
        file_exists = os.path.exists(tx_file_path + "/tx.draft")

        remove_file(tx_file_path, "/tx.draft")
        remove_file(tx_file_path, "/tx_metadata")

        self.assertTrue(
            file_exists,
            f"Verify the creation of the transaction draft file in {tx_file_path}",
        )
        self.assertIn(
            "Estimated transaction fee: Lovelace",
            response,
            "Failed to build the transaction",
        )

    def test_build_tx_destin_tokens(self):
        tx_file_path = self.starter.TRANSACTION_PATH_FILE
        remove_file(tx_file_path, "/tx.draft")
        params = {
            "address_origin": self.address_origin,
            "address_destin":  [
            {
                "address": self.address_origin,
                # "amount": 3000000,
                "tokens": [
                    {
                        "name": "MyTestEMG",
                        "amount": 1,
                        "policyID": "3547253f769b35cd318e062f7ade5b4ceb43462beb3f12ac18ce536b"
                    }
                ],
            }
        ],
            # "change_address": self.address_origin,
            # "metadata": self.metadata,
            # "mint": None,
            # "script_path": None,
            # "witness": 1,
        }
        response = self.node.build_tx_components(params)
        file_exists = os.path.exists(tx_file_path + "/tx.draft")

        remove_file(tx_file_path, "/tx.draft")
        remove_file(tx_file_path, "/tx_metadata")

        self.assertTrue(
            file_exists,
            f"Verify the creation of the transaction draft file in {tx_file_path}",
        )
        self.assertIn(
            "Estimated transaction fee: Lovelace",
            response,
            "Failed to build the transaction",
        )

    def test_build_tx_inline(self):
        tx_file_path = self.starter.TRANSACTION_PATH_FILE
        remove_file(tx_file_path, "/tx.draft")
        params = {
            "address_origin": ("addr_test1vrpns5yma4fy2dllhkzpyeur8xes94d903xu7enwuhc4erqecraxf"),
            "address_destin": [
            {
                "address": "addr_test1vrpns5yma4fy2dllhkzpyeur8xes94d903xu7enwuhc4erqecraxf",
                # "amount": 3000000,
                "tokens": [{

                    "name": "MAYZORACLE",
                    "amount": 1,
                    "policyID": "f0beeed590ae14ae003613d5ca13f9754aefb5b63ae50672ccc6a23c"
                }
                ],
            }
        ],
            # "change_address": self.address_origin,
            # "metadata": self.metadata,
            # "mint": None,
            # "script_path": None,
            # "witness": 1,
            "inline_datum": self.inline_datum,
        }
        response = self.node.build_tx_components(params)
        file_exists = os.path.exists(tx_file_path + "/tx.draft")

        remove_file(tx_file_path, "/tx.draft")
        remove_file(tx_file_path, "/tx_metadata")

        self.assertTrue(
            file_exists,
            f"Verify the creation of the transaction draft file in {tx_file_path}",
        )

        self.assertIn(
            "Estimated transaction fee: Lovelace",
            response,
            "Failed to build the transaction",
        )

        ######################################
        # 
        params = {
            "address_origin": self.address_origin,
            "address_destin": self.address_destin_with_tokens,
            "metadata": self.metadata,
            # "mint": None,
            # "script_path": None,
            # "witness": 1,
            "inline_datum": self.inline_datum,
        }

    def test_just_mint(self):

        type = "all"
        hashes = ["75eacb8808f937e42cde4312d2d4bb42bd1cbfca379bbe90a3ec0383"]
        slot = self.node.query_tip_exec()["slot"] + 20000
        parameters = {
            "type": type,
            "hashes": hashes,
            "type_time": self.type_time,
            "slot": slot,
            "purpose": self.purpose,
        }
        multisig_script, policyID = self.node.create_simple_script(parameters)
        script_file_path = self.starter.MINT_FOLDER

        mint = {
            "action": "mint",
            "tokens": [
                {"name": "", "amount": 1, "policyID": policyID},
            ],
        }
        tx_file_path = self.starter.TRANSACTION_PATH_FILE
        params = {
            "address_origin": self.address_origin,
            "metadata": self.metadata,
            # "address_destin": self.address_destin_no_tokens,
            "mint": mint,
        }
        response = self.node.build_tx_components(params)
        file_exists = os.path.exists(tx_file_path + "/tx.draft")

        self.assertTrue(
            file_exists,
            f"Verify the creation of the transaction draft file in {tx_file_path}",
        )
        self.assertIn(
            "Estimated transaction fee: Lovelace",
            response,
            "Failed to build the transaction",
        )

        remove_file(script_file_path, "/" + self.script_name + ".script")
        remove_file(script_file_path, "/" + self.script_name + ".policyid")
        remove_file(tx_file_path, "/tx_metadata")
        remove_file(tx_file_path, "/tx.draft")

    def test_just_burn(self):
        slot = 9764754
        type = "all"
        hashes = ["75eacb8808f937e42cde4312d2d4bb42bd1cbfca379bbe90a3ec0383"]
        # hashes = ["c338509bed524537ffbd8412678339b302d5a57c4dcf666ee5f15c8c"]
        # slot = self.node.query_tip_exec()["slot"] + 20000
        parameters = {
            "type": type,
            "hashes": hashes,
            "type_time": self.type_time,
            "slot": slot,
            "purpose": self.purpose,
        }
        multisig_script, policyID = self.node.create_simple_script(parameters)
        script_file_path = ""
        if self.purpose == "mint":
            script_file_path = self.starter.MINT_FOLDER
        elif self.purpose == "multisig":
            script_file_path = self.starter.MULTISIG_FOLDER

        mint = {
            "action": "burn",
            "tokens": [
                {"name": "Random", "amount": 758, "policyID": policyID},
            ],
        }
        params = {
            "address_origin": "addr_test1vqkge7txl2vdw26efyv7cytjl8l6n8678kz09agc0r34pdss0xtmp",
            "mint": mint,
        }
        response = self.node.build_tx_components(params)
        
        tx_file_path = self.starter.TRANSACTION_PATH_FILE
        file_exists = os.path.exists(tx_file_path + "/tx.draft")

        self.assertTrue(
            file_exists,
            f"Verify the creation of the transaction draft file in {tx_file_path}",
        )
        self.assertIn(
            "Estimated transaction fee: Lovelace",
            response,
            "Failed to build the transaction",
        )

        remove_file(script_file_path, "/" + self.script_name + ".script")
        remove_file(script_file_path, "/" + self.script_name + ".policyid")
        remove_file(tx_file_path, "/tx_metadata")
        # remove_file(tx_file_path, "/tx.draft")

        response = self.node.sign_transaction([self.wallet_name])
        response = self.node.submit_transaction()

class TestLibraryOnline(unittest.TestCase):
    def setUp(self):
        self.config_path = "cardanopythonlib/config/cardano_config.ini"
        self.starter = base.Starter()
        self.node = base.Node()
        self.wallet_name = "test_wallet"
        self.address_origin = (
            "addr_test1vqkge7txl2vdw26efyv7cytjl8l6n8678kz09agc0r34pdss0xtmp"
        )
        self.metadata = {"1337": {"name": "hello world", "completed": 0}}
        self.address_destin_no_tokens = [
            {
                "address": "addr_test1qp674jugprun0epvmep395k5hdpt689legmeh05s50kq8qc0wx9lg9h8x72hctqg34gy2eygnlrf7nyf343w34r67hjskugtxl",
                "amount": 3000000,
                # "tokens": [],
            }
        ]
        self.inline_datum = {"constructor": 0, "fields": [{"int": 42}]}
        self.script_name = "script_name"
        self.policyID = "cc8df048ecf8d32149269767c961aa193d89208844e876bdef186c9f"
        self.script_file_path = "./priv/example/example.script"
        self.type_time = "before"
        self.slot = self.node.query_tip_exec()["slot"] + 90000
        self.purpose = "mint"

    #####################################
    # This is the start of the section to test Starter class and Keys class
    #####################################

    def test_mint_and_burn(self):

        type = "all"
        hashes = ["75eacb8808f937e42cde4312d2d4bb42bd1cbfca379bbe90a3ec0383"]
        parameters = {
            "type": type,
            "hashes": hashes,
            "type_time": self.type_time,
            "slot": self.slot,
            "purpose": self.purpose,
        }
        multisig_script, policyID = self.node.create_simple_script(parameters)
        script_file_path = script_file_path = self.starter.MINT_FOLDER

        mint = {
            "action": "mint",
            "tokens": [
                {"name": "Random", "amount": 758, "policyID": policyID},
            ],
        }
        tx_file_path = self.starter.TRANSACTION_PATH_FILE
        params = {
            "address_origin": self.address_origin,
            # "address_destin": self.address_destin_no_tokens,
            "mint": mint,
        }
        response = self.node.build_tx_components(params)
        file_exists = os.path.exists(tx_file_path + "/tx.draft")

        self.assertTrue(
            file_exists,
            f"Verify the creation of the transaction draft file in {tx_file_path}",
        )
        self.assertIn(
            "Estimated transaction fee: Lovelace",
            response,
            "Failed to build the transaction",
        )
        # If still alive sign and submit

        response = self.node.sign_transaction([self.wallet_name])

        file_exists = os.path.exists(tx_file_path + "/tx.signed")

        self.assertTrue(
            file_exists,
            f"Verify the creation of the transaction sign file in {tx_file_path}",
        )

        self.assertIn(
            "Transaction signed!!",
            response,
            "Failed to sign the transaction"
        )

        response = self.node.submit_transaction()

        # Loop to confirm the transaction

        txHash = self.node.get_txid_body()
        txHash = txHash[:-1]

        transaction_result = self.node.get_transactions(self.address_origin)
        confirmation = False
        while not confirmation:
            for transaction in transaction_result:
                if transaction['hash'] == txHash:
                    confirmation = True
            time.sleep(10)
            transaction_result = self.node.get_transactions(self.address_origin)

##################################
# Section to burn the previously created token
##################################

        mint = {
            "action": "burn",
            "tokens": [
                {"name": "Random", "amount": 758, "policyID": policyID},
            ],
        }

        params = {
                    "address_origin": "addr_test1vqkge7txl2vdw26efyv7cytjl8l6n8678kz09agc0r34pdss0xtmp",
                    "mint": mint,
                }
        response = self.node.build_tx_components(params)
        
        tx_file_path = self.starter.TRANSACTION_PATH_FILE
        file_exists = os.path.exists(tx_file_path + "/tx.draft")

        remove_file(script_file_path, "/" + self.script_name + ".script")
        remove_file(script_file_path, "/" + self.script_name + ".policyid")
        remove_file(tx_file_path, "/tx_metadata")

        self.assertTrue(
            file_exists,
            f"Verify the creation of the transaction draft file in {tx_file_path}",
        )
        self.assertIn(
            "Estimated transaction fee: Lovelace",
            response,
            "Failed to build the transaction",
        )
        # If still alive sign and submit

        response = self.node.sign_transaction([self.wallet_name])

        file_exists = os.path.exists(tx_file_path + "/tx.signed")

        remove_file(tx_file_path, "/tx.draft")

        self.assertTrue(
            file_exists,
            f"Verify the creation of the transaction sign file in {tx_file_path}",
        )

        response = self.node.submit_transaction()
        remove_file(tx_file_path, "/tx.signed")

if __name__ == "__main__":
    unittest.main()
