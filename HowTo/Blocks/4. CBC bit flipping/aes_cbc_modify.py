from Crypto.Cipher import AES
import os

def encrypt(key, iv):
    msg1 = "?userdata="
    msg2 = "&colour=red&sometext=fifty%20shades%20of%20grey"
    user = raw_input("Enter some user data: ").replace("&","").replace("admin","")
    message = msg1+user+msg2
    while (len(message) % 16) != 0:
        message = message+'\x00'
    aes = AES.new(key, AES.MODE_CBC,iv)
    return iv.encode('hex')+aes.encrypt(message).encode('hex')

def decrypt(key, msg):
    if len(msg) < 1:
        msg = raw_input("Enter some stuff to decrypt (in hex)")
    iv = msg[:32].decode('hex')
    msg = msg[32:]
    aes = AES.new(key, AES.MODE_CBC,iv)
    out = aes.decrypt(msg.decode('hex'))
    return out

def is_admin(msg):
    v = decrypt(key, msg).strip('\x00')
    print v
    if v.count("&admin=true") > 0:
        return "You win"
    return "Nope"

def get_cookie(key):
    iv = os.urandom(16)
    return encrypt(key, iv)

#~~~~~~~~~~~~~~~~~~~~DO NOT EDIT ABOVE THIS LINE~~~~~~~~~~~~~~~~~~~
# IV is the first 16 bytes of the ciphertext. Shouldn't matter for this challenge

key = os.urandom(16)
ui = ""
print "Cookie structure is:"
print "?userdata=<USER DATA HERE>&colour=red&sometext=fifty%20shades%20of%20grey"
cookie = get_cookie(key)
print "Here is your cookie: ", cookie, '\n'
ui = raw_input("Enter a cookie, check if you are admin. Type !q to quit: ")
while ui != "!q":
    try:
        print is_admin(ui)
    except:
        print "Error decrypting"
    ui = raw_input("Enter a cookie, check if you are admin. Type !q to quit: ")
