def print_hex_chunks(m):
    for x in range(0,len(m),32):
        print m[x:x+32]

def print_raw_chunks(m):
    for x in range(0,len(m),16):
        print m[x:x+16]

def print_raw_chunks_in_hex(m):
    for x in range(0,len(m),16):
        ms = m[x:x+16].encode('hex')
        while len(ms) < 32:
            ms = ms + '00'
        print ms

def xor_hex_strings(a, b):
    return hex(int(a, 16) ^ int(b, 16)).strip('0x').strip('L')

def xor_three_hex_strings(a,b,c):
    return xor_hex_strings(a,xor_hex_strings(b,c))

# example step by step of how it would be done on a 'known string'

cook = "7f9c2e92513181cdf0e32fcfcdfac0a4bbe72007ffaa0f386f065f84367f70541b2cd7824e0a3086a46b0d0811afe3a1b7d603cb9255b" \
       "080455098a3fb5c89895d9cd778bb25d6bead22976974e33482"
print "raw:"
print_raw_chunks("?userdata=loldong&colour=red&sometext=fifty%20shades%20of%20grey")
print
print "raw(hex):"
print_raw_chunks_in_hex("?userdata=loldong&colour=red&sometext=fifty%20shades%20of%20grey")
print
print "cipher:"
print_hex_chunks(cook)
plain = "ades%20of%20grey"
print
print "plain:"
print plain.encode('hex')
second_last = "b7d603cb9255b080455098a3fb5c8989"
print
print "desired:"
print "aaaaa&admin=true".encode('hex')
print
print "Evil block:"
print xor_three_hex_strings("616465732532306f6625323067726579", "0xb7d603cb9255b080455098a3fb5c8989",
                            "61616161612661646d696e3d74727565")
print
print "Evil CT:"
print "7f9c2e92513181cdf0e32fcfcdfac0a4bbe72007ffaa0f386f065f84367f70541b2cd7824e0a3086a46b0d0811afe3a1b7d307d9d641e1" \
      "8b4e1cc4aee85c99955d9cd778bb25d6bead22976974e33482"