###### XOR

Xor is a fundamental part of crypto, it has the cool property that XORing two
values results in a third value that is _usually_ very difficult to return back to
it's base parts. The cool part is, that doing the same XOR operation with two of the 
three values results in the third

```
A xor B = C
B xor C = A
C xor A = B
```

Which is cool, because if we can generate a random key, xor it against a not random
plaintext, it will generate a random ciphertext.

### OH SHIT XOR SUCKS

That's cool and all, but that also means that if the attacker has either the plaintext 
or the key, he wins. This might seem silly, but for example, if we know part of the key,
then we can get part of the plaintext, if the plaintext is english and we know enough 
of the key, we can guess the rest. Also, because of the way XOR works, if
the key is used to encrypt more than one plaintext, we can do a ciphertext
only attack, and discover the plaintext (and the key).

For example

```
K XOR P1 = C1
K XOR P2 = C2
```

Will mean that if we XOR C1 and C2, we eliminate the key. We can then guess 
at the plaintext of C1, and if we are right, the plaintext of C2 will be the result

```
C1 XOR C2 = P1P2

P1P2 XOR P1 = P2
```

This is called crib-dragging, and the more values that are XOR'd against the
same key that we can obtain, the better it works.

There is a file titled 'cribdragme' that contains a bunch of ciphtertexts all
xor'd against the same key. See if you can find the plaintext using only the provided
ciphertexts!

