# CardanoPythonLib

### Cardano Python Library

### Installation

#

1. Prerequesites

- Minimum: Cardano-cli, Cardano Wallet and Cardano Address installed. You will be able to run offchain code, generate keys, create and sign transactions.
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

3. Download the library from github
> We are working to allow the installation of this library with pip but in the meantime:

    git clone https://github.com/larestrepo/CardanoPythonLib.git

4. Install requirements (For the time being optional)

If you look at the requirements, in this release, it only contains some support dependencies for shaping and styling python code. Basically no dependencies as of now.

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
