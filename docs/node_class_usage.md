# Node class 

### Node class helps you to interact with the Cardano blockchain by using mainly the Cardano CLI.
A challenge when using the Cardano CLI is that some commands are difficult to build, there are multiple parameters and sometimes it is even needed to make calculations. Instead of doing it manually this library helps you to query the blockchain, addresses and build complex transactions by just passing the inputs required in json format. Even more with this in place, it is possible to automate tasks, like having a job creating NFTs as per requests and after fulfilling certain conditions. Possibilities are endless.

***

### Basic usage

1. Interaction with the blockchain

Available methods are:

- id_to_address(wallet_name)
- get_txid()
- query_protocol(saving_path='')
- query_tip_exec()
- get_transactions(wallet_id)
- get_balance(wallet_id)
- utxo_selection(addr_origin_tx, quantity, deplete)
- tx_min_fee(tx_in_count, tx_out_count) -- deprecated
- sign_witness(signing_key_name)
- create_multisig_script(script_name, type, required, hashes)
- create_policy_id(script_name)
- sign_transaction(sign_address_name)
- submit_transaction()
- build_tx_components(params)
- analyze_tx(tx_name_file)
- assemble_tx(witness_wallet_name_array)

Some of these functions we've already seen it in the keys_class_usage like create_multisig_script where we created the multisig script after creating some wallets. 

The most important function, like the core of this library, is the <mark>build_tx_components</mark>. Basically every interaction with the blockchain is via transactions, so it is mandatory to build a transaction. The way Cardano works is that it is possible to build the transaction offchain and have a validation at this level, so you can be certain that when you submit your transaction is less likely to fail. This step of building the transaction and offline validation is done with the <mark>build_tx_components</mark>. 

But let's first look at some useful functions

### query_protocol
It creates a json file with the protocol parameters from the blockchain.

```python
from cardanopythonlib import base

node = base.Node()
node.query_protocol()
```

### query_tip_exec
It prints in the console/stores in a variable the result of the query tip

    {
        "era": "Alonzo",
        "syncProgress": "100.00",
        "hash": "8fbcae43a6290b23511f02e03d088acc473debd54d2da13eed9031b4e5bfe8c4",
        "epoch": 210,
        "slot": 60535224,
        "block": 3621136
    }

```python
from cardanopythonlib import base

node = base.Node()
node.query_tip_exec()
```
### get_transactions
You can pass the name of the wallet if store in the path .priv/wallets/<wallet_id>. In which case is going to look by default the utxos for the .payment.addr. Or you can provide the address itself. 
It will return a dictionary with the utxos associated to the address.

```python
from cardanopythonlib import base

node = base.Node()
wallet_id = 'test1'
node.get_transactions(wallet_id)
wallet_id = 'addr_test1vrut60f37qvfy8ma6u7jrlt69atkwjpa8axfvryg69hgqlc7xz9hw'
node.get_transactions(wallet_id)
```
### get_balance
Similar to get_transactions but it gives a dictionary with the address balance

```python
from cardanopythonlib import base

node = base.Node()
wallet_id = 'test1'
node.get_balance(wallet_id)
wallet_id = 'addr_test1vrut60f37qvfy8ma6u7jrlt69atkwjpa8axfvryg69hgqlc7xz9hw'
node.get_balance(wallet_id)
```

### build_tx_components
Build any kind of transaction packing the components in a json format.

The params must be built following some minimum rules:

```json
 schema = {
                'address_origin': {
                    'type': 'string',
                    'required': True,
                },
                'address_destin': {
                    'type': 'list',
                    'nullable': True,
                    'schema':{ 'type': 'dict', 'schema':{
                        'address': {'type': 'string', 'required': True},
                        'amount': {'type': 'dict', 'required': True, 'schema': {'quantity': {'type': 'integer', 'required': True}, 'unit': {'type': 'string'}}},
                        'assets': {'type': 'dict', 'nullable': True}
                    }
                    }
                },
                'change_address': {
                    'type': 'string',
                    'required': True,
                },
                'metadata': {
                    'type': 'dict',
                    'nullable': True,
                },
                'mint': {
                    'type': 'dict',
                    'nullable': True,
                },
                'script_path': {
                    'type': 'string',
                    'nullable': True,
                },
                'witness': {
                    'type': 'integer',
                    'required': True,
                },
        }
```
The only mandatory fields are: address_origin, change_address and witness.

Below a couple of examples.

1. The most simple and silly transaction. Sending the minimum amount of ADA allowed to the same address.

```python
from cardanopythonlib import base
node = base.Node()
address_origin ='addr_test1qp3hc694xtngj6vt4kgxppqz5807kxyy737l4s7n35vmhgrjkcctzvtrmt0chuqgaphal08kaqhn0gn295v7wefe95eqh3m3q7'
metadata = None
witness = 1
params = {
    "message": {
        "tx_info": {
            "address_origin": address_origin,
            "address_destin": None,
            "change_address": address_origin,
            "metadata": None,
            "mint": None,
            "script_path": None,
            "witness": witness,
        }
    }
}

result = node.build_tx_components(params)
```

The result is:

    ['cardano-cli', 'transaction', 'build', '--tx-in', 'a26bd5ebe05a7dd2b6a383d1db51189cea93eff56f10f8cd43111574b73ce909#0', '--change-address', 'addr_test1qp3hc694xtngj6vt4kgxppqz5807kxyy737l4s7n35vmhgrjkcctzvtrmt0chuqgaphal08kaqhn0gn295v7wefe95eqh3m3q7', '--testnet-magic', '1097911063', '--witness-override', '1', '--out-file', './.priv/transactions/tx.draft']
    Estimated transaction fee: Lovelace 165325

    ################################

2. The same simple transaction as before but just to insert some metadata in the Blockchain.

```python
from cardanopythonlib import base
node = base.Node()
address_origin ='addr_test1qp3hc694xtngj6vt4kgxppqz5807kxyy737l4s7n35vmhgrjkcctzvtrmt0chuqgaphal08kaqhn0gn295v7wefe95eqh3m3q7'
metadata = {"1337": {
        "name": "hello world",
        "completed": 0
    }}
witness = 1
params = {
    "message": {
        "tx_info": {
            "address_origin": address_origin,
            "address_destin": None,
            "change_address": address_origin,
            "metadata": metadata,
            "mint": None,
            "script_path": None,
            "witness": witness,
        }
    }
}

result = node.build_tx_components(params)
```
The result is:

    ['cardano-cli', 'transaction', 'build', '--tx-in', 'a26bd5ebe05a7dd2b6a383d1db51189cea93eff56f10f8cd43111574b73ce909#0', '--change-address', 'addr_test1qp3hc694xtngj6vt4kgxppqz5807kxyy737l4s7n35vmhgrjkcctzvtrmt0chuqgaphal08kaqhn0gn295v7wefe95eqh3m3q7', '--metadata-json-file', './.priv/transactions/tx_metadata.json', '--testnet-magic', '1097911063', '--witness-override', '1', '--out-file', './.priv/transactions/tx.draft']
    Estimated transaction fee: Lovelace 168493

    ################################

> **Note:** Compare the latest with the previous transaction. See that the metadata fields where activated and the fees were increased. 

> **Note:** It also picked the utxo from the ones available in the address based on the utxo_selection algorithm.

> **Note:** The transaction file is stored by default in './.priv/transactions/tx.draft'. Keep in mind that if you rerun the script twice, it will overwrite your previously created file. 

3. Transaction sending to a different address
To send to different addresses use the field address_destin as a list of address following the specified format.

```python
from cardanopythonlib import base
node = base.Node()
address_origin ='addr_test1qp3hc694xtngj6vt4kgxppqz5807kxyy737l4s7n35vmhgrjkcctzvtrmt0chuqgaphal08kaqhn0gn295v7wefe95eqh3m3q7'
metadata = None
address_destin = [
        {
          "address": "addr_test1qr2ac9vl2epy3yjynkqyfuskx6wp6ld70579v3s6wknve3rjkcctzvtrmt0chuqgaphal08kaqhn0gn295v7wefe95eqvl97xq",
          "amount": {
                "quantity": 5000000,
                "unit": "lovelace"
            },
          "assets": None,
        },
      ]
witness = 1
params = {
    "message": {
        "tx_info": {
            "address_origin": address_origin,
            "address_destin": address_destin,
            "change_address": address_origin,
            "metadata": metadata,
            "mint": None,
            "script_path": None,
            "witness": witness,
        }
    }
}

result = node.build_tx_components(params)
```
The result is:

    ['cardano-cli', 'transaction', 'build', '--tx-in', '1b00055fa6bd06296562a3bf78f3cbe30525add63c8fe228a89d6c8a3f37c9e4#0', '--tx-out', 'addr_test1qr2ac9vl2epy3yjynkqyfuskx6wp6ld70579v3s6wknve3rjkcctzvtrmt0chuqgaphal08kaqhn0gn295v7wefe95eqvl97xq+5000000', '--change-address', 'addr_test1vqrfdj8fkzs0pxg0eu4p38apgd430stz5hafx7pnsxn0ccg4jqkyd', '--metadata-json-file', './.priv/transactions/tx_metadata.json', '--testnet-magic', '1097911063', '--witness-override', '1', '--out-file', './.priv/transactions/tx.draft']
    Estimated transaction fee: Lovelace 170121

    ################################

    Sign transaction file stored in './.priv/transactions/tx.signed'
    Transaction successfully submitted.

> You can add multiple address destinations in the address_destin list as long as you keep the format to send to multiple addresses in one transaction. 

4. minting
We need to first create a minting script and policyid. 


```python
from cardanopythonlib import base
keys = base.Keys()
wallet_id = 'wallet01'
hash= keys.keyHashing(wallet_id)
node.create_multisig_script(wallet_id,'all','',[hash])
node.create_policy_id(wallet_id)
```
The result is:

    Key hash of the verification payment key: '0696c8e9b0a0f0990fcf2a189fa1436b17c162a5fa93783381a6fc61'
    Executing Creation of script
    Script stored in './.priv/wallets/wallet01/wallet01.script'
    '{'type': 'all', 'scripts': [{'type': 'sig', 'keyHash': '0696c8e9b0a0f0990fcf2a189fa1436b17c162a5fa93783381a6fc61'}]}'
    Executing Creation of Minting Policy ID
    ae6498eeb6f7f7bdd3b411c7d3bdf0dfd29f6b989382f9bdb1279638

Then, the actual minting transaction

5. Transaction sending to a different address with tokens
To send to different addresses use the field address_destin as a list of address following the specified format.

```python
from cardanopythonlib import base
node = base.Node()
address_origin ='addr_test1qp3hc694xtngj6vt4kgxppqz5807kxyy737l4s7n35vmhgrjkcctzvtrmt0chuqgaphal08kaqhn0gn295v7wefe95eqh3m3q7'
metadata = None
address_destin = [
        {
          "address": "addr_test1qr2ac9vl2epy3yjynkqyfuskx6wp6ld70579v3s6wknve3rjkcctzvtrmt0chuqgaphal08kaqhn0gn295v7wefe95eqvl97xq",
          "amount": {
                "quantity": 3000000,
                "unit": "lovelace"
            },
          "assets": [{
            "asset_name": "Prueba4",
            "amount": 4575122544123,
            "policyID": "ae6498eeb6f7f7bdd3b411c7d3bdf0dfd29f6b989382f9bdb1279638"
          },
        },
      ]
witness = 1
params = {
    "message": {
        "tx_info": {
            "address_origin": address_origin,
            "address_destin": address_destin,
            "change_address": address_origin,
            "metadata": metadata,
            "mint": None,
            "script_path": None,
            "witness": witness,
        }
    }
}

result = node.build_tx_components(params)
```
The result is:

    ['cardano-cli', 'transaction', 'build', '--tx-in', '71c979e89fdb6930af4369d8c6315aa626e9197c37268899573d9026add69626#0', '--tx-in', 'b31bb6acaec9eb167e034cc2b8f2fca205211174cd1f721f10f217aa90efaf6d#1', '--tx-out', 'addr_test1qr2ac9vl2epy3yjynkqyfuskx6wp6ld70579v3s6wknve3rjkcctzvtrmt0chuqgaphal08kaqhn0gn295v7wefe95eqvl97xq+3000000+4575122544123 ae6498eeb6f7f7bdd3b411c7d3bdf0dfd29f6b989382f9bdb1279638.50727565626134', '--change-address', 'addr_test1vqrfdj8fkzs0pxg0eu4p38apgd430stz5hafx7pnsxn0ccg4jqkyd', '--testnet-magic', '1097911063', '--witness-override', '1', '--out-file', './.priv/transactions/tx.draft']
    Estimated transaction fee: Lovelace 170737

    ################################

    Sign transaction file stored in './.priv/transactions/tx.signed'
    Transaction successfully submitted.

5. Transaction sending all combinations
To send to different addresses use the field address_destin as a list of address following the specified format.

```python
from cardanopythonlib import base
node = base.Node()
address_origin ='addr_test1qp3hc694xtngj6vt4kgxppqz5807kxyy737l4s7n35vmhgrjkcctzvtrmt0chuqgaphal08kaqhn0gn295v7wefe95eqh3m3q7'
metadata = metadata = {"1337": {
        "name": "hello world",
        "completed": 0
    }}
address_destin = [
        {
          "address": "addr_test1qr2ac9vl2epy3yjynkqyfuskx6wp6ld70579v3s6wknve3rjkcctzvtrmt0chuqgaphal08kaqhn0gn295v7wefe95eqvl97xq",
          "amount": {
                "quantity": 3000000,
                "unit": "lovelace"
            },
          "assets": [{
            "asset_name": "Prueba4",
            "amount": 4575122544123,
            "policyID": "ae6498eeb6f7f7bdd3b411c7d3bdf0dfd29f6b989382f9bdb1279638"
          },
        },
      ]
witness = 1
params = {
    "message": {
        "tx_info": {
            "address_origin": address_origin,
            "address_destin": address_destin,
            "change_address": address_origin,
            "metadata": metadata,
            "mint": None,
            "script_path": None,
            "witness": witness,
        }
    }
}

result = node.build_tx_components(params)
```
The result is:

    ['cardano-cli', 'transaction', 'build', '--tx-in', '71c979e89fdb6930af4369d8c6315aa626e9197c37268899573d9026add69626#0', '--tx-in', 'b31bb6acaec9eb167e034cc2b8f2fca205211174cd1f721f10f217aa90efaf6d#1', '--tx-out', 'addr_test1qr2ac9vl2epy3yjynkqyfuskx6wp6ld70579v3s6wknve3rjkcctzvtrmt0chuqgaphal08kaqhn0gn295v7wefe95eqvl97xq+3000000+4575122544123 ae6498eeb6f7f7bdd3b411c7d3bdf0dfd29f6b989382f9bdb1279638.50727565626134', '--change-address', 'addr_test1vqrfdj8fkzs0pxg0eu4p38apgd430stz5hafx7pnsxn0ccg4jqkyd', '--testnet-magic', '1097911063', '--witness-override', '1', '--out-file', './.priv/transactions/tx.draft']
    Estimated transaction fee: Lovelace 170737

    ################################

    Sign transaction file stored in './.priv/transactions/tx.signed'
    Transaction successfully submitted.

### sign_transaction
The sign transaction just takes the tx.draft previously created with the build_tx_components and stores a new tx.signed file in the same default path. This is just the transaction file signed with the skey. The skey file should be in the./.priv/wallet/<wallet_name> folder with the name <wallet_name.payment.skey>. If the Keys class was used, the keys should be there by default otherwise you need to place the file in the path. 

```python
from cardanopythonlib import base

node = base.Node()
wallet_id = 'test1'
result = node.sign_transaction(wallet_id)
```
The result is:

    Sign transaction file stored in './.priv/transactions/tx.signed'

### submit_transaction
Submit transaction will submit the signed transaction to the blockchain. It expects to have a tx.signed file in the folder: ./.priv/transactions/tx.signed

```python
from cardanopythonlib import base

node = base.Node()
result = node.submit_transaction()
```
