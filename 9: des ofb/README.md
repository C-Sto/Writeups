### Solution

After inspecting the provided code, nothing obvious stands out. After making a few
attempts at various things - xoring the ciphertext against the IV provided a partial
plaintext...weird.

A bit of googling revealed that when encrypting with a weak key, the encryption and 
decryption process is identical. When in OFB mode, the IV is first encrypted against 
the key to provide the first block of keystream, then that block is encrypted with 
the same key to provide the next block of keystream, and so on. Because a weak key
is used, the second (and every even) keystream block is simply the IV. As it turns out
there are also only 4 weak keys in DES - so trying each decryption key and
looking at the result is a fairly simple task.
