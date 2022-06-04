from cardanopythonlib import base

keys = base.Keys()

wallet_name = 'wallet01'
nmemonic_size = 24
keys.deriveAllKeys(nmemonic_size,wallet_name)