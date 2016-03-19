from Crypto.PublicKey import RSA
from Crypto import Random

# creating a key
random_generator = Random.new().read
key = RSA.generate(1024, random_generator)
public = key.publickey()

# getting info from the key
print "public modulus: ", public.n
print "public exponent: ", public.e
print "private exponent: ", key.d
print "prime 1: ", key.p
print "prime 2: ", key.q

# exporting a key
print key.exportKey()
print public.exportKey()

# importing a key *newlines are required!*
publicString = "-----BEGIN PUBLIC KEY-----\n" \
               "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC+WC2sir1XvH2lDyyjaJGqYJPM\n" \
               "KVsLWL36XY24Xv7bdJlRrDtkUQtiDqlrW7l+EEzSE0BQKwa7Bw9eGdCGefbw3nNc\n" \
               "v6yiypA/D2Ex3BFHFzYxZPqKc219UO3xRz/pjOevJgwHcD2i3EWeUnTYHEO9uHcm\n" \
               "LUJkV0pShYaJlp8pPwIDAQAB\n" \
               "-----END PUBLIC KEY-----"
public = RSA.importKey(publicString)

# creating a key from primitives (this is a bad idea for security, don't expect hand picked primitives to be safe)
# the tuple takes these args: (n,e,d,p,q,Phi(n))
p = 10972999900218833046945112565984503578779728691545585391273961622045499117452093030445545025986394639787757880151546172061114256410017721845481728681517593
q = 11262017558322659460576213941347569162450407776524874320055190766100865070424960601177389215122318328488576758474253320352863725020159380742436021184329877
n = 123578117543737288045673954054072954467599664259704288706671323840097013441987215617240631210000600342849827213782518902841329277183431623223185557474465999264721330884501964316920152340654436399494651467082421052971352976336653071268723076156150984067120236200259993349093284010796840077698042028963091026061
# we cast to long here, because that's what the library expects
e = 65537L
d = 4917706494866515818897991549399915547728762750649385613424459657521293483935832557635588540758374135132098652265816398349179650501157966848742968611523372569593782124152290512579279280137648366597283096546867066843460339603097322527930154111459800645797462674970482728372660772473298884916199159589912435201
key = RSA.construct((n,e,d))
print "Hand picked values:"
print key.exportKey()
