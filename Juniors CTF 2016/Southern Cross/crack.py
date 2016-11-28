import re

alph = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
alph_shift = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

def rotate(l, n):
    return l[n:] + l[:n]

def encrypt(text,key):
    r = ""
    keyindex = 0
    for x in text:
        off = alph.index(key[keyindex])
        shifted=rotate(alph_shift, off)
        r+=shifted[alph.index(x)]
        keyindex = (keyindex+1) % len(key)
    return r

def decrypt(text,key):
    if not len(key)>0:
        return ''
    r = ""
    keyindex = 0
    for x in text:
        off = alph.index(key[keyindex])
        shifted=rotate(alph_shift, off)
        if x not in alph:
            r+=x
        else:
            r+=alph[shifted.index(x)]
            keyindex = (keyindex+1) % len(key)
    return r

freqs = {
'a': 0.0651738,
'b': 0.0124248,
'c': 0.0217339,
'd': 0.0349835,
'e': 0.1041442,
'f': 0.0197881,
'g': 0.0158610,
'h': 0.0492888,
'i': 0.0558094,
'j': 0.0009033,
'k': 0.0050529,
'l': 0.0331490,
'm': 0.0202124,
'n': 0.0564513,
'o': 0.0596302,
'p': 0.0137645,
'q': 0.0008606,
'r': 0.0497563,
's': 0.0515760,
't': 0.0729357,
'u': 0.0225134,
'v': 0.0082903,
'w': 0.0171272,
'x': 0.0013692,
'y': 0.0145984,
'z': 0.0007836,
' ': 0.1918182
}

def score(s):
    score = 0
    for i in s:
        c = chr(ord(i)).lower()
        if c in freqs:
            score += freqs[c]
    return score

testkey = "GRAVITY"
testText = "MABEL EATS SPRINKLES".replace(' ','')



testenc = encrypt(testText, testkey)
testdec = decrypt(testenc, testkey)
print testenc, score(testenc)
print testdec, score(testdec)



crypted = file("crypt.txt", 'r').read()
#dict
#pth = "/usr/share/wordlists/rockyou.txt"
pth = "fghex.txt"
bst = 0
bstt = ""
with open(pth, "r") as ins:
    for line in ins:
        line = line.replace(' ','')
        line = line.upper()
        line = valids = re.sub(r"[^A-Z]+", '', line)
        tstTxt = decrypt(crypted, line)
        scr = score(tstTxt)
        if scr > bst:
            bst = scr
            bstt = tstTxt
            print bstt

for i in range(4):
    print f.readline()


#bruteforce

bst = 0
bstt = ""
for current in xrange(10):
    a = [i for i in alph]
    for y in xrange(current):
        a = [x+i for i in alph for x in a]
        for j in a:
            test_key = j
            tstTxt = decrypt(crypted, test_key)
            scr = score(tstTxt)
            if scr > bst:
                bst = scr
                bstt = tstTxt
                print bstt
