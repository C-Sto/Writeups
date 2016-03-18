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
 
 !(ecbPenguin)[<insert penguin here>]
 
So using it on files with patterns longer than the block size is bad. We 
should be able to use it on small sets of data though, right?

Well, sure, but it also has the slightly weird property that you can literally 
copy and paste blocks, and as long as it's valid ciphertext it will end up being valid 
plaintext.

Let's first make a few assumptions. Firstly, the encryption function is secure. 
That means that as far as looking at ciphertext, plaintext, and keys, we can't simply 
decrypt it via bruteforce, or any other method (reasonably). I'll be using AES in this example 
but it should hold true for any secure cipher. Secondly, we have a good idea of the plaintext. 
This isn't always true, and doesn't always need to be true, but helps in this example. Thirdly, 
we can feed partial plaintext, and receive the corresponding ciphertext. We don't have access 
to the key, only an encryption and decryption function.

Let's say, for example, we have a cookie that is a json string. 

``` json

{id:"19", some_other_thing:12, user_entered_thing:"aa", is_admin:"no"}

```

This cookie is encrypted using the mighty AES (in ECB mode). Our goal is to
set the ciphertext to give us admin credentials.

We know that it's using AES ECB, but it's always a good idea to suss out the 
inputs and outputs. To do this, give it two different length outputs 
(by one, usually), and see how the length in the corresponding ciphertext changes.
If it doesn't change, or changes by more than the difference in input, it's
probably a block cipher. 
 
Next, to detect if it's in ECB mode, we send a long string 
of the same character, over and over. We want to aim for 2-3x the block size,
so in this case, 48 of the same character will probably do. Remember that thing 
about patterns longer than the blocksize showing up in ciphertext? now we look 
at the ciphertext block by block, if there is a duplicate block in there we know
two things, first, it's most likely ECB, second, that block is what your string of the 
same character encrypts to. Cool!

Now that we know that, if we have a good guess as to what the plaintext string 
is that we want to be the result of the decryption, all we need to do is replace 
one of the blocks of repeating character with our desired string.

To do this, we need to make sure we are dealing with the right block. Send 
requests to the encryption function with one character less, until the second 
duplicate block disappears. Once it does, you know that the length you have 
remaining will encrypt to one entire block of repeating characters, and 
the next block contains all the same character, except for one (this is 
actually the basis for another attack, we will get onto that later). So, 
add the character back, then remove one block worth of characters. In the case 
of AES, this is 16. You should still have at least one blocksize worth of 
characters left, and probably some additional padding. Replace the blocksize 
worth of characters, with a string you want, something like, say " is_admin:"yes"}"

Now, we remember what the repeating character block looks like right? take the 
new block after that, and copy it. If you have access to the decryption function 
decrypt it, and marvel at your l33t skills. But wait, we still need to make 
the cookie valid right?

Now, depending on where you need to paste your data, this could be easy (like in the example)
or only slightly less easy. If the data you want is exactly the right length, and is on the end,
then all we need to do is pad the rest of the data so that the last block fits perfectly on 
the end. Then we paste our data where that last block would be, and hey presto - we have 
admin!

If you are in the unfortunate position where you need to paste it on the border between 
two blocks, and it comes in the plaintext before we can add padding, you are going to need 
to generate valid plaintext for both of those blocks, and replace them.
 



