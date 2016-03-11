###### RSA

RSA is a pretty popular cryptosystem. It consists of a public key, and a private key
both derived from the same sets of numbers. Some numbers can be known, some cannot.

Generally, these are the different parts and descriptions of each:

N = The public modulus. This is used as the modulus for the plaintext
 message that has E as the exponent. It is created by multiplying P and Q.

P = One of the primes that goes into producing the modulus N

Q = Another of the primes that goes into producing the modulus N

D = The private exponent. This is the multiplicative inverse of e (mod phi(n)), and is used
to turn ciphertext into plaintext. A clearer way to think of it is d\*e = 1 mod Phi(n)

E = The public exponent. This is generally one of a few small primes. This is the exponent
used to multiply the plaintext message

Phi(n) = The totient of P and Q. This is used to pick D.