# Keys class 

### Keys class helps you generate keys and addresses.
One of the major limitations with Cardano-cli is that the keys generated are not easy to integrate with wallet keys initially generated from Yoroi, Eternl, etc.

This class helps you create Keys from mnemonics and generate the equivalent key files like in Cardano-cli. So you can create your own keys and use them from the wallet and from the cli interchangeably.

***

### Basic usage

1. Generating the keys

> You can use the following methods separately but it is recommended that you use <mark>deriveAllKeys()</mark> method to get all the keys with a json file summary. 

Available methods are:

- generate_mnemonic(size)
- deriveRootKey(mnemonic)
- deriveExtendedSigningStakeKey(root_key)
- deriveExtendedSigningPaymentKey(root_key)
- deriveExtendedVerificationPaymentKey(payment_signing_key)
- deriveExtendedVerificationStakeKey(stake_signing_key)
- derivePaymentAddress(payment_verification_key)
- convertPaymentKey(payment_signing_key, name)
- convertStakeSigningKey(stake_signing_key, name)
- deriveBaseAddress(ayment_vkey,stake_vkey, name)
- keyHashing(name)
- deriveAllKeys(size, name)
- generateCardanoKeys(name)
- create_multisig_script(script_name, type, required, hashes)
- create_address_script(script_name)

***

Using the deriveAllKeys method, you can create all the keys with just a few lines of code ( run this from python3 in the terminal or within a file like the main.py provided): 

### Option 1

Create a wallet from scratch provide the number of words (recommended size = 24)

```python
from cardanopythonlib import base

keys = base.Keys()
wallet_name = 'wallet01'
nmemonic_size = 24
key.deriveAllKeys(wallet_name, size= 24)
```
The code will return something similar to this:

    ##################################
    Find all the keys and address details in: ./priv/wallets/wallet01/wallet01.json
    ##################################

All the keys will be store at './priv/wallets/<name_provided>

### Option 2

Recreate a wallet from nmemonics. You need to provide the words as a comma separated list

```python
from cardanopythonlib import base

keys = base.Keys()
wallet_name = 'wallet01'
mnemonic = ['dial','ivory','leave','fog','boring','nose','brass','food','kitchen','example','fame','expire','apart','game','pipe','ship','excite','sponsor','bread','place','beach','raven','prevent','stem']
keys.deriveAllKeys(wallet_name, words= mnemonic)
```

You can take a backup and delete the folder. Store your keys in a private location. This library does not keep any log or backup.

>**Warning:** Your nmenomics are the most important piece of information and the ultimate way of recovering your keys.

>**Note:** This libary does not keep backup or logs of any of these files.

>**Warning:** Keep in mind that if you rerun the above code with the same <mark>wallet_name</mark>, your previously generated keys will be overwritten.  


2. Multisig functionality

This library also provides the functionality to create a multisig script. This is useful when you want to provide authorization for transactions from multiple keys to unlock funds that locked in the script address.

For more details see: [Multisignatures](https://github.com/input-output-hk/cardano-node/blob/c6b574229f76627a058a7e559599d2fc3f40575d/doc/reference/simple-scripts.md).

For multisig you need multiple wallets that will be allowed to sign the transaction and a script file with the conditions to spend adas from the script address locking the funds. 

The steps are:

    1. Create multiple keys and addresses
    2. Hash the verification keys
    3. Create the script file
    4. Build the script address
    5. Lock funds in the script address
    6. Unlock funds from the script address

```python
from cardanopythonlib import base

keys = base.Keys()
wallet_names = ['wallet01', 'wallet02', 'wallet03']

keyHashes = []
for name in wallet_names:
    key_info = key.deriveAllKeys(24, name)
    hash = key_info['hash_verification_key']
    keyHashes.append(hash)

# building multisig script
name = 'MyFirstMultiSig'
node = base.Node()
type = "atLeast"
required = 2
multisig_script = node.create_multisig_script(name, type, required, keyHashes)

keys.create_address_script(name)
```

> In this example we generate 3 wallets and their hashes which are passed to create the script with the following conditions: At least 2o3 of the wallets should witness the transaction to unlock the funds from the script address.

### More realistic scenario

There should be normally participants that are supposed to witness the transaction and one assembler to collect the files from the participants, assembling and signing the transaction.

Every participant should run this code individually to generate the wallet and hash. If the wallet is already created, the keyHashing(wallet_name) option can be run to get the corresponding hash. Keep in mind that the verification file should be at .priv/wallets/<wallet_name> which is the default path where the keyHashing function will look for the key. The assembler should take the different hashes and create the multisig script and generate the script address.

To unlock the funds, the participants should witness the transaction by using the sign_witness function from the Node class also available in this library and send the generated transaction file to the assembler so he can assemble all the witness files to finally sign and submit the transaction. 
