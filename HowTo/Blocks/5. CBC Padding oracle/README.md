# Padding oracle

An 'oracle' in this sense is _something_ that can tell us _something_ that 
might not be intended for us to know, or might not be directly available 
from looking at the system in it's expected uses. A timing oracle could tell us 
that a certain string comparison is successful, regardless of the result 
that is returned to us. A padding oracle could tell us if a message was 
padded correctly or incorrectly, just by having different error responses.

Okay, so what is 'padding'? if we look at a block cipher, we need to have 
a standard way of dealing with plaintext not _quite_ fitting within the block 
size. Padding solves this problem. There are a number of padding standards, 
the one that I've picked on is PKCS7. The brief summary is that bytes are
appended to the plaintext before encryption, corresponding to the number 
of bytes that required adding (lolwat?). If a block falls exactly within 
 the bounds, an additional block is added that is _just_ padding bytes.
 
An example might illustrate this a little better.

Each string is a hex representation of the bytes of the plaintext before 
being sent to _some_ block cipher of block size 6 bytes.

*full block*
```
aabbccddeeff
```

*not full block compared to full block*
```
aabbccddeeff
bbaadd
```

So we can see that there is a gap. We fill this gap with bytes that hold 
the value of the number of bytes that are to be added

*full block compared to padded block*
```
aabbccddeeff
bbaadd030303
```

So we can see that the block that needed padding is now a full block, and 
can be sent to the block cipher for encrypting. Here are some more valid 
paddings for PKCS7.

```
aa0505050505
aabb04040404
aabbcc030303
aabbccdd0202
aabbccddee01
aabbccddeeff060606060606
```

Right, now that we know what an oracle is, and what padding is, we can 
combine the two to *completely destroy any sort of confidentiality you hoped existed*.

If a developer, in all their wisdom, has decided to have *extremely* verbose 
errors (or just the specific kind of error we want to see),
 we can look for an error that says "hey, the padding was incorrect 
after I decrypted the thing you sent" This tells us that...well, the padding 
was incorrect on the thing we sent. If it so happens that AES CBC is the 
cipher mode in use (and messages are not being authenticated, we will get onto that in another section)
we can use the padding error as an oracle to decrypt _everything_.

In the CBC bit flipping section, we looked at how to change a bit (or byte) at 
a certain location in the plaintext. It only required that we know what was there,
so that we knew what we needed to change the previous block's corresponding byte to. 
If you haven't worked through that, it's a good idea to read back over it 
or get comfortable with it, as it's the main concept for implementing this.

Using the same logic, we can make a guess at what we think is in the last byte
of the plaintext. We do this by trying to make the padding be valid. An example
of this (be aware, all values are made up theoretical ones):

*assuming the 6 bye block cipher in cbc mode*
(for this example, the first 6 bytes in a 12 byte string are the IV)

```
# correctly padded plaintext (we do not know this)
aabbccddee01

# ciphertext (first 6 bytes are IV)
deadbeefffffabcdabcdabcd

# ciphertext with attacker flipped bits in IV (because cbc chain reaction)
deadbeeffffeabcdabcdabcd

# plaintext of attacker flipped bits in IV (this returns a 'bad padding' error)
aabbccddee99

# ciphertext with different attacker flipped bits in IV
deadbeefffaaabcdabcdabcd

# plaintext of attacker flipped bits in IV (this doesn't error, indicating a correct guess)
aabbccddee01

# ciphertext with attacker flipped bits in IV (attacking second last byte. We know the last byte, so can control the value of if)
deadbeeffeababcdabcdabcd

# plaintext of attacker flipped bits in IV (this returns a 'bad padding' error)
aabbccdd3002

# ciphertext with attacker flipped bits in IV (attacking second last byte)
deadbeefadababcdabcdabcd

# plaintext of attacker flipped bits in IV (this doesn't error, indicating a correct guess)
aabbccdd0202

..etc
```

Once we know what the value in the last byte is, we can look at the second-to-last byte by 
doing exactly the same thing, but changing the last byte to 0x02 instead of 
0x01. We can do that with _all_ bytes, and magically we have the plaintext. 

Even scarier, using the exact same method, we can inject a totally new 
completely chosen plaintext without any knowledge of the key, and only being 
told if the plaintext has valid padding or not.

A practical example that you can try will be put up soon. For now,
try the one that featured in the 2016 Google CTF (if it's still up). The solution
to this challenge was not to decrypt the cookie, but see if you can find the 
content using the padding oracle method.
https://eucalypt-forest.ctfcompetition.com/

