import hashlib
pre_hash = b'faff'
hashed = hashlib.sha1(pre_hash)
hex_dig = hashed.hexdigest()

print(hex_dig)