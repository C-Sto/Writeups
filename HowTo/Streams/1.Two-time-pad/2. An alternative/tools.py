import os
import string

eng_freq ={'a':8.167, "b":1.492, "c":2.782, "d":4.253, "e":12.702,
          "f":2.228, "g":2.015, "h":6.094, "i":6.966, "j": 0.153,
          "k":0.772, "l":4.025, "m":2.406, "n":6.749, "o":7.507,
          "p":1.929, "q":0.095, "r":5.987, "s":6.327, "t":9.056,
          "u":2.758, "v":0.978, "w":2.360, "x":0.150, "y":1.974,
          "z":0.074, " ":55.00, "\n":0.01, ".":6.53, ",":6.16,
          ";":0.32,  ":":0.34,  "!":0.33,  "?":0.56, "'":2.43,
          '"':2.67,  "-":1.53}


def chi_square_score(plaintext, distr):
    score = 0
    tested = []
    for char in list(string.ascii_lowercase)+distr.keys()+list(plaintext):
        char = char.lower()
        # only test each character once
        if char in tested:
            continue
        # count the number of occurrences of the character
        count = plaintext.count(char)
        # get the expected from the given distribution
        if char in distr:
            expected = distr.get(char)
        else:
            # this will give us a high number for any unexpected characters we run into
            expected = len(plaintext)*0.00001
        score += ((count-expected) * (count-expected)) / expected
        tested.append(char)
    return score

# test our estimation function, remember that lower score = more english
c1 = "this is an english string"
c2 = os.urandom(25)
c3 = os.urandom(25).encode('base64')[:-1]
c4 = os.urandom(25).encode('hex')
c5 = "eeeeee"
c6 = "m awstiw.tna sehl ytu hht G'g fonlina'Gotee m.oe,ynr understaie"

c = {c1,c2,c3,c4,c5,c6}
for cx in c:
    print cx, chi_square_score(cx,eng_freq)


def xor(s1, s2):
    shorter, longer = (s1,s2) if len(s1) < len(s2) else (s2,s1)
    out = ""
    for x in range(len(shorter)):
        v = chr(ord(longer[x])^ord(shorter[x]))
        out += v
    return out

key = os.urandom(128)
plains = ["a super secret message that must never be revealed, nor should it ever fall into capture",
          "another super secret message, unfortunately encrypted under the same key as before :( :(",
          "this message is supposedly secret, but I'm having my doubts at the moment, to be frank..",
          "another english message sent under the same key, this is probably bad but I'm not sure..",
          "a non interesting message, pay it no mind, please dont discover what has been written in",
          "so, do we know if it matters if the same key is used to encrypt multiple messages yet?  ",
          "does anyone know what time the bottle store shuts? I'd like to get myself something nice",
          "to be fair though, this is a fairly large number of ciphertexts, isn't it? I mean, realy",
          "that being said, if you also think about capturing WEP traffic, that is a big number so,",
          "assuming somone misuses a nonce or IV somewhere, you can probably exploit this irl, srs ",
          "The magic number for ciphertexts for this method is roughly eleven, there are 15 herelol",
          "Just remember that the more ciphertexts that you have, the more accurate this method is ",
          "So if you can generate ciphertexts, you are at a serious advantage, because you can then",
          "work out the key fairly easily. Let's make that the challenge, you have a ct generator, ",
          "and a scret msg to decrypt that was encrypted using the same key, decrypt it for l33th4x"
          ]

# create the ciphertexts
c = []
for p in plains:
    c.append(xor(p,key))
print
print
# be a hacker
found_key = ''
for index in range(len(c[1])):
    # for each unknown key byte, we want to try all values, and keep the best score
    best = ''
    best_score = 9999999
    for possible_key_byte_value in range(0,256):
        possible_key_byte = chr(possible_key_byte_value)
        # create our 'plaintext'
        plain = ''
        score = 0
        for cx in c:
            plain += xor(possible_key_byte, cx[index])
        score += chi_square_score(plain, eng_freq)
        if score < best_score:
            best = possible_key_byte
            best_score = score
    found_key += best

for cx in c:
    print xor(found_key,cx)