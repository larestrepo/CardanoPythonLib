from cardanopythonlib import base

keys = base.Keys()

wallet_name = 'test02'
nmemonic_size = 24
keys.deriveAllKeys(nmemonic_size,wallet_name)

# Building multisig script
node = base.Node()

hashwallet01 = '0696c8e9b0a0f0990fcf2a189fa1436b17c162a5fa93783381a6fc61'
hashtest1 = 'f8bd3d31f018921f7dd73d21fd7a2f5767483d3f4c960c88d16e807f'
hashtest02 = '5a35f34a035eaa12b78aa4f0022d16e5f8e4564cb142334c4fe4496c'
keyHashes = [
    hashwallet01,
    hashtest1,
    hashtest02,
]
name = 'MyFirstMultiSig'

type = "atLeast"
required = 2
multisig_script = node.create_multisig_script(name, type, required, keyHashes)

keys.create_address_script(name)