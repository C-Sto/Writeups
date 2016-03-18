from Crypto.Cipher import AES
import os

key = os.urandom(16)
def encrypt(key):
    msg1 = "{\"id:\"19\", some_other_thing:12, user_entered_thing:\""
    msg2 = "\", is_admin: \"no\"}"
    message = msg1+raw_input("Enter some stuff to encrypt: ")+msg2
    while (len(message) % 16) != 0:
        message = message+'\x00'
    aes = AES.new(key, AES.MODE_ECB)
    return aes.encrypt(message).encode('hex')

def decrypt(message, key):
    aes = AES.new(key, AES.MODE_ECB)
    return aes.decrypt(message.decode('hex'))

#~~~~~~~~~~~~~~~~~~~~DO NOT EDIT ABOVE THIS LINE~~~~~~~~~~~~~~~~~~~

ui = ""
while ui != "!q" :
    enc = encrypt(key)
    spaced = [enc[i:i+32] for i in range(0,len(enc),32)]
    print "Encrypted spaced version: ",spaced,'\n'
    print "Encrypted version: ", enc ,'\n'
    print "Length of ciphertext: ",  len(enc)/2
    ui = raw_input("Enter some hex to decrypt: ")
    if ui == "!q":
        exit
    try:
        print "Decrypted version: ", decrypt(ui, key)
    except:
        print "Error in decryption, make sure your ciphertext is in hex, and is valid"
    ui = raw_input("Type !q to quit: ")
