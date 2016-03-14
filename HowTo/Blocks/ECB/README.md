###### ECB Mode

ECB mode (Electronic Code Book) is the most basic form of using a block cipher.
Each corresponding plaintext block turns into a ciphertext block of identical size.

Visual representation for a blocksize of 4 and a simple encryption function
```
AAAABBBBCCCCAAAABBBC
|   |   |   |   |   |
DDDDEEEEFFFFDDDDGGGG
```

The longer the message, the easier it is to infer plaintext. Repeating
ciphertext blocks represent parts of the plaintext that also repeat. 
This means repeating patterns appear in the ciphertext - as can be
 seen by the famous ECB penguin.
 
 <insert penguin here>
