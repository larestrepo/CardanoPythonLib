# CardanoPythonLib

### Cardano Python Library

This is a Python library to interact with Cardano Blockchain. 

### Installation

#

1. Prerequesites

- Minimum: Cardano-cli. You will be able to run offchain code, generate keys, create and sign transactions.
- Desired: Cardano-node running. You will be able to submit onchain and get confirmations from the blockchain.
- Unlock more: Cardano wallet installed. You will be able to create wallets using the Cardano Wallet API.

> As a side note, we are working to allow the interaction of this library with the Cardano blockchain without the need of any cardano node or even cardano CLI/wallet/address installed locally.

2. Virtual environment setup
As you might know, it is recommended to run python code from a virtual environment to isolate your installation and keep everything clean and organized. 

I work with virtualenvwrapper but you can use your prefered choice. For virtualenvwrapper:

    sudo apt install python3-pip
    sudo -H pip3 install --upgrade pip
    sudo -H pip3 install virtualenv virtualenvwrapper

    echo "export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3" >> ~/.bashrc

    echo "export WORKON_HOME=~/Env" >> ~/.bashrc
    echo "source /usr/local/bin/virtualenvwrapper.sh" >> ~/.bashrc

Create the virtual environment

    mkvirtualenv <pick a cool name>

List all virtual environments

    lsvirtualenv

3. CardanoPythonLib installation

> CardanoPythonlib library is in PyPi. Link to official site: https://pypi.org/project/cardanopythonlib/

- Option 1. Pip installation

With the virtual environment active

    pip install cardanopythonlib

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


- Option 2. Download the library from github

    git clone https://github.com/larestrepo/CardanoPythonLib.git

4. Install requirements

Make sure to have active your virtual environment

    pip install -r requirements.txt

You should be good to go

#

### Working with the library

cardanopythonlib folder is the package that contains the main functionalities. 

base.py file contains 3 classes.

- Starter
- Node
- Keys

For usage please go to docs folder.

#
