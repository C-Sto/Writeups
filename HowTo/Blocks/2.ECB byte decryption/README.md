# Byte at a time decryption

You will recall from the cut and paste example, there was a point at which we knew an entire block, besides one byte.
If we change the scenario somewhat, and assume that we can supply data at the START, and unknown data is appended, it turns
out we can decrypt everything without knowing the key or plaintext.

So, our assumptions for this one are as follows:

1. The encryption function is secure. We don't need to know what sort of encryption is used, just that it is ECB
2. We can submit plaintext, and receive ciphertext.
3. The returned ciphertext is the result of the user supplied input being prepended to the unknown (secret) plaintext.
ciphertext = enc(user_values+secret_message,unknown_key)

Right, now let's get into HOW.

First, just like before we need to establish that we are indeed working with a block cipher, and that it's ECB.

```
code to submit single char
code to submit two chars
```

```
code to submit 32 chars
identify repeating block
```

Right, with that out of the way, we can see the two repeated ciphertext blocks. If we remove one char from the end of our
padding, we end up with something like this

```
[aaaaaaaaaaaaaaaa][aaaaaaaaaaaaaaa?]
```

So how do we figure out what the last character is? Simple, submit the block until it matches. For example..

```
[aaaaaaaaaaaaaaaa][aaaaaaaaaaaaaaab]
[aaaaaaaaaaaaaaaa][aaaaaaaaaaaaaaac]
[aaaaaaaaaaaaaaaa][aaaaaaaaaaaaaaad]
```

until that last ciphertext block matches the unknown one. Once it does, we know the value of that last byte, and can do
the same thing until we eventually reveal the whole plaintext.
