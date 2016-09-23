import socket
import string

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect(("146.148.102.236",24069))
def sendMsg(s, msg):
    s.send(msg+'\n')

def recvMsg(s):
    return s.recv(1024)

CODE = {'A': '.-',     'B': '-...',   'C': '-.-.',
        'D': '-..',    'E': '.',      'F': '..-.',
        'G': '--.',    'H': '....',   'I': '..',
        'J': '.---',   'K': '-.-',    'L': '.-..',
        'M': '--',     'N': '-.',     'O': '---',
        'P': '.--.',   'Q': '--.-',   'R': '.-.',
     	'S': '...',    'T': '-',      'U': '..-',
        'V': '...-',   'W': '.--',    'X': '-..-',
        'Y': '-.--',   'Z': '--..',

        '0': '-----',  '1': '.----',  '2': '..---',
        '3': '...--',  '4': '....-',  '5': '.....',
        '6': '-....',  '7': '--...',  '8': '---..',
        '9': '----.'
        }

MORSE = {}

for x in CODE.keys():
    MORSE[CODE[x]] = x

ROUND = '1'

round3a = "abcdefghijklmnopqrstuvwxyz; ',. ' ;}~ !\"#$%&'()"
round3 = ["abcsftdhuneimky;qprglvwxjzo ',",
          "axje.uidchtnmbrl'poygk,qf;s -wv"]

ALPHABET = list(
           "abcdefghijklmnopqrstuvwxyz{|}~ !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`")

testStrings = ["abcdefghijklmnopqrstuvwxy",
               "aaaaaaaaaabbbbbbbbbbccccc",
               "abc123abc123xyz",
               "aaaaaaaaaaaaaaaaaaaaaaaaa",
               "aaaaaaaaabbbbccccddddeeee"]

round8a =    [("aabbcaabb\x00aabc\x00aabc\x00abbc\x00abbc\x00",1),
              ("616161616161616161006161616100616161610061616161006161616100".decode('hex'),3),
              ("616162646561616364006161636400616263650061626365006162646500".decode('hex'),4),
              ("||>||>||>|}?}}?}}?}}@~~@~",1)]

answers = ["moon child", "bastian","my luckdragon","atreyu vs gmork","i owe you","reading is dangerours",
           "the oracle", "gmorks cool", "fragmentation", "the nothing", "dont forget auryn", "try swimming", "giant turtle",
           "welcome atreyu","save the princess"]

print "Alphabet length:",len(ALPHABET)

ct = "(yZs$[u4O%'S**"
plain =    "aabcdefz{|}~ !\"#$%&'"

m = recvMsg(s)
print m
sendMsg(s, '')
while m is not None:
    m = recvMsg(s)
    if m.count('No... I am leaving.') > 0:
        print "Epic fail lol"
        exit(0)
    if m.count('level ') > 0:
        ROUND = m[m.index('level ')+6:m.index('level ')+7]
        print 'ROUND', ROUND
    if int(ROUND) > 7:
        print ROUND, m
    if ROUND == '1' :
        if m.split('\n')[1][0:4] == 'What':
            morse = m.split('\n')[1].split('What is ')[1]
            morse = morse.split('  decrypted?')[0]
            morsewords = morse.split('   ')
            out = ""
            for word in morsewords:
                for ch in word.split(' '):
                    if ch == '':
                        continue
                    out+= MORSE[ch]
                out+=" "
        sendMsg(s, out[:-1])
    if ROUND == '2':
        if m.split('\n')[1][0:4] == 'What':
            msg = m.split('\n')[1].split('What is ')[1]
            msg = msg.split(' decrypted?')[0]
            out = ""
            for x in msg:
                out += ALPHABET[ALPHABET.index(x)-13]
        sendMsg(s, out)

    if ROUND == '3':
        if m.count('Give me some text:')  > 0:
            sendMsg(s, 'cdefb.,\'')
            m = recvMsg(s)
        if m.split('\n')[0][0:4] == 'cdef':
            alph = m.split('\n')[0].split(' ')
            if alph[3][0]=='c': round3v = round3[0]
            if alph[3][0]=='j': round3v = round3[1]
        if m.split('\n')[1][0:4] == 'What':
            msg = m.split('\n')[1].split('What is ')[1]
            msg = msg.split(' decrypted?')[0]
            out = ""
            for x in msg:
                out += round3a[round3v.index(x)]
            sendMsg(s, out)
        else:
            sendMsg(s, 'abcdefghijklmnopqrs')
    if ROUND == '4':
        if m.count('Give me some text:')  > 0:
            sendMsg(s, 'abcdefghijklmnopqrstuvwxy')
            m = recvMsg(s)
        if m.split('\n')[0][0:4] == 'abcd':
            alph = m.split('\n')[0].split(' ')[3]
            if len(alph) > 0:
                shift = ALPHABET.index(alph[0])
            else:
                shift = ALPHABET.index(' ')
        if m.split('\n')[1][0:4] == 'What':
            msg = m.split('\n')[1].split('What is ')[1]
            msg = msg.split(' decrypted?')[0]
            out = ""
            for x in msg:
                out += ALPHABET[ALPHABET.index(x)-shift]
        sendMsg(s, out)
    if ROUND == '5':
        if m.count('Give me some text:') > 0:
            sendMsg(s, "abcdefgh{|}~ !\"#$%&'()*")
            m = recvMsg(s)
        if m.split('\n')[0][0:4] == 'abcd':
            alph = m.split('\n')[0].split(' ')[3]
            shift = ALPHABET.index(alph[0])
        if m.split('\n')[1][0:4] == 'What':
            msg = m.split('\n')[1].split('What is ')[1]
            msg = msg.split(' decrypted?')[0]
            out = ""
            for x in msg:
                if x =='\x7f':
                    x = ' '
                out += ALPHABET[ALPHABET.index(' ')+(ALPHABET.index(' ')-ALPHABET.index(x))]
        sendMsg(s, out)

    if ROUND == '6':
        if m.count('Give me some text:') > 0:
            sendMsg(s, "aabcdefz{|}~ !\"#$%&'")
            m = recvMsg(s)
            #print 'round', m
        if m.split('\n')[0][0:4] == 'aabc':
            alph = m.split('\n')[0].split('encrypted is ')[1]
            if len(alph) > 0:
                shift = ALPHABET.index(alph[0])
                mult = ALPHABET.index(alph[2])-ALPHABET.index(alph[1])
        if m.split('\n')[1][0:4] == 'What':
            msg = m.split('\n')[1].split('What is ')[1]
            msg = msg.split(' decrypted?')[0]
            out = ""
            for x in msg:
                for xx in ALPHABET:
                    if ALPHABET[(ALPHABET.index(xx) * mult + shift) % (len(ALPHABET))] == x:
                        out += xx
        sendMsg(s, out)

    if ROUND == '7':
        if m.count('Give me some text:') > 0:
            sendMsg(s, testStrings[1])
            m = recvMsg(s)
            #print 'round', m
        if m.split('\n')[0][0:4] == 'aaaa':
            alph = m.split('\n')[0].split('encrypted is ')[1]
            shifts = [ALPHABET.index(alph[0]),ALPHABET.index(alph[1]),ALPHABET.index(alph[2])]

        if m.split('\n')[1][0:4] == 'What':
            msg = m.split('\n')[1].split('What is ')[1]
            msg = msg.split(' decrypted?')[0]
            out = ""
            for xx in range(len(msg)):
                shift = xx % 3
                out += ALPHABET[ALPHABET.index(msg[xx]) - shifts[shift]]
        if answers.count(out)<1:
            print "adding:", out
            answers.append(out)
        sendMsg(s, out)

    if ROUND == '8':
        if m.count('Give me some text:') > 0:
            sendMsg(s, testStrings[0])
            m = recvMsg(s)
            print 'round', m
        if m.split('\n')[0][0:4] == 'aaaa':
            alph = m.split('\n')[0].split('encrypted is ')[1]
            print alph, alph.encode('hex')

        if m.split('\n')[1][0:4] == 'What':
            msg = m.split('\n')[1].split('What is ')[1]
            msg = msg.split(' decrypted?')[0]
            msg = msg.strip('\x00')
            out = ""
            print "Decrypt this:", msg
            potents = []
            for x in answers:
                if x[0] == msg[0]:
                    potents.append(x)
            clonepotatos = potents
            if len(potents) > 1:
                print "potents", potents
                for x in potents:
                    print "potatoTesting:",x
                    for y in x:
                        if msg.count(y) != x.count(y):
                            if clonepotatos.count(x)>0:
                                print 'removed', x
                                clonepotatos.remove(x)
            print "could have gone bad?",clonepotatos
            out = clonepotatos[0]
            print out
        sendMsg(s, out)

    if ROUND == '9':
        testString = testStrings[1]
        if m.count('Give me some text:') > 0:
            sendMsg(s, testString)
            m = recvMsg(s)
            print 'round', m
        if m.split('\n')[0][0:4] == testString[0:4]:
            alph = m.split('\n')[0].split('encrypted is ')[1]
            print alph, alph.encode('hex')

        if m.split('\n')[1][0:4] == 'What':
            msg = m.split('\n')[1].split('What is ')[1]
            msg = msg.split(' decrypted?')[0]
            out = ""
            print "Decrypt this:", msg
            for x in answers:
                if len(x) == len(msg):
                    print x
            out = raw_input("")
        sendMsg(s, out)
