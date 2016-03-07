from Crypto.Cipher import DES
from Crypto.Cipher import XOR

f = open('ciphertext', 'r')
ciph = f.read()
f.close()

IV = '13245678'

def tryKey(key):
    key = key.decode('hex')
    a = DES.new(key, DES.MODE_OFB, IV)
    return a.encrypt(ciph)

weak_keys = ["0101010101010101", "1F1F1F1F0E0E0E0E",
             "FEFEFEFEFEFEFEFE", "E0E0E0E0F1F1F1F1"]

def descrypt(c, k):
    key = k.decode('hex')
    a = DES.new(key, DES.MODE_ECB)
    return a.encrypt(c)

def blockify(c, blocksize):
    ret = []
    for x in range(0,len(c),blocksize):
        ret.append(c[x:x+blocksize])
    return ret

blocks = blockify(ciph,8)

def xor(a,b):
    a = XOR.new(a)
    return a.encrypt(b)
x = "13245678"
for i in blocks:
    print xor(x,i)

for key in weak_keys:
    print tryKey(key)


    
