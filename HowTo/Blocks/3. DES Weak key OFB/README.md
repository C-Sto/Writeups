# DES Weak Key OFB

Some ciphers are not so secure. DES, which is widely known to be...brittle, has 
an interesting property when a certain type of key is used. The effect is that 
the cipher's encryption and decryption methods become identical - when usually 
they are the inverse. Usually, encrypting a block twice would be just that, however 
with a weak key, encrypting it twice simply decrypts the block. There are only a handful 
of keys that have this property (you can look at them on wikipedia), so avoiding them 
is ideal, but stuff gets _really_ bad when you need to rely on encrypting another ciphertext 
block to generate a keystream, say.

### OFB Mode

Okay, let's forget DES for a minute and explore OFB mode. The way OFB mode works 
is the cipher takes a first input (an IV), and encrypts it, then encrypts the 
ciphertext from that to generate the next block etc. The keystream that is generated 
is then XOR'd against the plaintext. I'm sure you can see where this is going...

Here is a handy diagram that was stolen from wikipedia

![ofb diagram](https://github.com/C-Sto/Writeups/blob/master/HowTo/Blocks/3.%20DES%20Weak%20key%20OFB/OFB.png)

### Combining the two

Since using DES with a weak key has that super sweet effect, it means 
that every other block in the cipher is then simple XOR'd against the IV. 
Since we know the IV, we can just XOR it against the ciphertext to test, if 
half of the ciphertext is legible, we can deduce that a weak key is used, 
and since there is only a handful, we can simply just try each until one works \o/

I've included a file that has 5 different ciphertexts, figure out which one 
is vulnerable to the weak key, and find the secrets held within