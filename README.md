# CardanoPythonLib

### Cardano Python Library

This is a Python library to interact with Cardano Blockchain. 

<hr>

- Prerequesites

    Minimum: Cardano-cli. You will be able to run offchain code, generate keys, create and sign transactions.
    
    Desired: Cardano-node running. You will be able to submit onchain and get confirmations from the blockchain.


### Install poetry

```shell
curl -sSL https://install.python-poetry.org | python3 -

poetry new <project_name>
```
### Add dependencies
```shell
poetry add cardanopythonlib
```

The library relies on a cardano_config.ini file which connects to Cardano testnet by default. If you want to overwrite some of the parameters, please create a new ini file in your folder:

    [node]
    KEYS_FILE_PATH = ./.priv/wallets
    TRANSACTION_PATH_FILE = ./.priv/transactions
    CARDANO_NETWORK = testnet
    CARDANO_NETWORK_MAGIC = 1097911063
    CARDANO_CLI_PATH = cardano-cli
    URL = http://localhost:8090/v2/wallets/

When using CARDANO_NETOWRK = mainnet the CARDANO_NETWORK_MAGIC is ignored. 

Instantiate the class as follows:

```python
from cardanopythonlib import base

config_path = './cardano_config.ini' # Optional argument
node = base.Node(config_path) # Or with the default ini: node = base.Node()
node.query_tip_exec()
```

#

### Working with the library

cardanopythonlib folder is the package that contains the main functionalities. 

base.py file contains 3 classes.

- Starter
- Node
- Keys

For usage please go to docs folder.

### Credits:

Latest implementations related to Plutus are based on the following repo:

[pycardano](https://github.com/Python-Cardano/pycardano)
