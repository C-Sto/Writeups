'''
Below is a step by step solution using a crib dragging method - use it to check your work or if you are
really stuck. Run the script, and step through the output as you read through it to get an idea of what
you should be looking for
'''

c1 = "GQBRFxcACQBOHRVSBgcRAFIKTwFPVRxPOABWPB1VRwQAARYAGA0RAAsaGUUXTxYARG4WGUUWT0cm\
Ti9BRgcZAgACHQIYBxBNBAAQBxdFBA0TAAAwSBgAOg0fCxlJCQhOAQcANA4eRVcWGhlEDVUNACkA\
AkUGSA4cTggTTx5BGE4eTwAQChwXACkQDw==".decode('base64')

c2 = "B0UcEAFURxgPAA9BRx0TCUxZFhpVVRhPOUU/Qh8AAQoLAghOC0UzTw0bFAAJDhwLADcKA0UHTgMK\
HB0VQRwR".decode('base64')

c3 = "GQBRExcADAEBGQ8AAggVDQAWGx1FB1BGIRdWFh0ACwAACUF5AxAGABEKFFIQSAROQisAGEUTQw8G\
AAlNABAAGgA4HRpSHAEAFQELABcNCkUGGwAKDgwAJxFWLBxTDgsLQkFXCEEJClQRTx5ODAVZVyYE\
AkIBAAUKCwBBRxwIF0dHAAE=".decode('base64')

c4 = "DwsSRRtGRxYBG0FBFAJWCEVZBxpXVTkHI0UQABdMDgEJTiVPAkIAAA0KGUxEAhJOWSEQURcXABMA\
AU4DTBsbCgAVHU8GCwE=".decode('base64')

# xor where we repeat the short string to match the long string
def repeatingxor(s1,s2):
    shorter, longer = (s1,s2) if len(s1) < len(s2) else (s2,s1)
    out = ""
    for x in range(len(longer)):
        v = chr(ord(longer[x])^ord(shorter[x%len(shorter)]))
        out+= v
    return out

# xor where we only xor up until the end of one of the strings
def shortxor(s1,s2):
    shorter, longer = (s1,s2) if len(s1) < len(s2) else (s2,s1)
    out = ""
    for x in range(len(shorter)):
        v = chr(ord(longer[x])^ord(shorter[x]))
        out+= v
    return out

# rotates a string left ('the' => 'het')
def rotl_string(instr):
    return instr[1:]+instr[0]

# prints out all the possible locations of the given 'test' string. Start with ' the', see what you get
def drag(c1, c2, test):
    shorter, longer = (c1,c2) if len(c1) < len(c2) else (c2,c1)
    p1p2 = repeatingxor(shorter,longer[:len(shorter)])
    for x in range(len(test)):
        print x
        v= repeatingxor(p1p2,test).encode('ascii','replace')
        out2 = ""
        out1 = ''
        for i in range(0,len(v)-len(test),len(test)):
            out1+=test
            out2+= v[i:i+len(test)]
        print out1
        print out2
        print
        test = rotl_string(test)

raw_input("Let's begin by trying a drag and look for english.\nPress enter to continue")
print "C2"
drag(c1,c2,"the ")
print "C3"

drag(c1,c3,'the ')
print "C4"
drag(c1,c4,'the ')

raw_input("if it's right, in the same location in the other drags, there will be partial english too\nidentified 'on't ' in C4^C1 at position index 35-40 in drag position 0\nPress Enter to continue")
m1m4 = shortxor(c1,c4[:39])
# xor c1 or c4 with the 'known' bytes to get a partial key (first numbers are garbage to pad to desired position)
partkey = shortxor("12345678901234567890123456789012345on't ", c4)

# look at text from xoring the partial key
print "C1"
print shortxor(c1,partkey)
print "C2"
print shortxor(c2,partkey)
print "C3"
print shortxor(c3,partkey)
print "C4"
print shortxor(c4,partkey)
print "key"
print partkey
raw_input("make a guess to complete some of the english (let's try a space before 'Your' in C3)\nPress Enter to continue")
partc3 = "'9pb9p|/92s%>v3rw%7#`Zu7dq.3|43:s Your"
temp_key = shortxor(partc3,c3)
# check it against all the other ciphertext to see if you are right
print "C1"
print shortxor(c1,temp_key)
print "C2"
print shortxor(c2,temp_key)
print "C3"
print shortxor(c3,temp_key)
print "C4"
print shortxor(c4,temp_key)
raw_input("looks right, now lets put a space infront of the Don't in C4..\nPress Enter to continue")

partc4 = "123456789012345678901234567890123 Don't "
temp_key = shortxor(partc4,c4)
# check it against all the other ciphertext to see if you are right
print "C1"
print shortxor(c1,temp_key)
print "C2"
print shortxor(c2,temp_key)
print "C3"
print shortxor(c3,temp_key)
print "C4"
print shortxor(c4,temp_key)
raw_input("looks good, but no english words stand out to me, let's try another drag using 'and '..\nPress Enter to continue")

print "C2"
drag(c1,c2,"and ")
print "C3"
drag(c1,c3,'and ')
print "C4"
drag(c1,c4,'and ')

raw_input("okay, we can see 'me yo' at 45-50 in drag 2 C4, and corresponding places in the other text appears to be english too\n"
          "let's combine that with our previously known key, and add the u 'you' ;)\n"
          "Press Enter to continue")
m1m4 = shortxor(c1,c4[:50])
partkey = shortxor("123456789012345678901234567890123 Don't 12345me you", c4)
# and see what it looks like all together
temp_key = partkey

print "C1"
print shortxor(c1,temp_key)
print "C2"
print shortxor(c2,temp_key)
print "C3"
print shortxor(c3,temp_key)
print "C4"
print shortxor(c4,temp_key)

raw_input("hey, another 'u' to add :D\nPress Enter to continue")

temp_key = shortxor(c2, "9|=a/$767+2`+p7>8(032|/6z1|>91ling Go1#>xxake you")

print "C1"
print shortxor(c1,temp_key)
print "C2"
print shortxor(c2,temp_key)
print "C3"
print shortxor(c3,temp_key)
print "C4"
print shortxor(c4,temp_key)
raw_input("you're!\nPress Enter to continue")


temp_key = shortxor(c4, "123456789012345678901234567890123 Don't 12345me you're")

print "C1"
print shortxor(c1,temp_key)
print "C2"
print shortxor(c2,temp_key)
print "C3"
print shortxor(c3,temp_key)
print "C4"
print shortxor(c4,temp_key)
raw_input("# time to make a guess at c4's bridged bit... Don't ?????me you're.... Don't tell me?\n"
          "Press Enter to continue")

temp_key = shortxor(c4, "123456789012345678901234567890123 Don't tell me you're")

print "C1"
print shortxor(c1,temp_key)
print "C2"
print shortxor(c2,temp_key)
print "C3"
print shortxor(c3,temp_key)
print "C4"
print shortxor(c4,temp_key)
raw_input("jackpot. ow the rules and so d...o I?\nPress Enter to continue")

temp_key = shortxor(c1, "'9pf9py.v6e!!1r> kq+)2|.sq3)x7:ow the rules and so do I")

print "C1"
print shortxor(c1,temp_key)
print "C2"
print shortxor(c2,temp_key)
print "C3"
print shortxor(c3,temp_key)
print "C4"
print shortxor(c4,temp_key)

print "Enough hand holding, if you want the rest, you know what to do. Feel free to download and edit this file," \
      " or implement your own method"

# If you want to get the rest out, keep trying and verifying your attempts. This is an extremely long way of doing it,
# but I wanted to make it clear what was going on at each step
