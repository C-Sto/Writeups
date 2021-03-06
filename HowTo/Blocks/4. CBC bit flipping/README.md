# CBC Bitflipping

Another encryption scheme is CBC. This scheme uses the output of the previous 
block as a way of preventing some of the attacks on ECB, we can't see the 
penguin anymore.
*Note: this is the basis of the CBC padding oracle attack, which is turning up in some CTF's*

![image showing cbc](CBC_encryption.png)

Drats, foiled... maybe...

Let's say we have an encrypted cookie that we want to add an admin credential to.
The plaintext looks something a bit like this:

```
?userdata=<your_user_data_goes_here>&colour=red&sometext=fifty%20shades%20of%20grey
```

so, knowing this, we want to add ```&admin=true``` to the **end**.
*As a side note, we are assuming anything in the user input area is escaped appropritately*

Let's make some assumptions:

1. We have full control over ciphertext. It's not authenticated in any way.
2. The encryption function is secure (AES, in this case)
3. We know what the plaintext looks like, roughly
4. We don't know the key

Because while decrypting the ciphertext, it takes the previous ciphertext 
block and xor's it against the currently decrypted block to reveal the plaintext, 
and we have full access to that ciphertext block, we then have full control
over that part of the plaintext. However, it will totally screw with the plaintext 
in the block before it. sometimes this is OK, sometimes this can be hard to deal with.

The way we do it is simple, we first need to make the target block decrypt to 0's. Once we
can do that, we can simply xor whatever we injected to make it 0 with our desired data, and 
it should decrypt into what we wanted.

How to make 0's? Well, since XORing the ciphertext value with the pre-plaintext value would result
in plaintext, and we know the ciphertext and the plaintext, to turn it into 
0's, we just XOR the pre-plaintext with the ciphertext, and then again with the plaintext.

Our injected data would be: xor(plaintext(xor(pre-plaintext,ciphertext))

Where the plaintext and pre-plaintext are of the target block, and the ciphertext 
is of the block before it.

Here is an example using a simpler plaintext of 32 'a' characters, and
a key of "YELLOW SUBMARINE" and an IV of "YELLOW SUBMARINE"

```
plaintext(raw):
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
plaintext(hex):
6161616161616161616161616161616161616161616161616161616161616161
ciphertext(hex) (broken into blocks for clarity):
59454c4c4f57205355424d4152494e45 656117aa24402dbd7294b4f089cce890 a69fc6d8d51b3447286f536539a66ce7

desired plaintext at end:
aaaaa&admin=true
ogiveacookietooo
which would make our plaintext:
aaaaaaaaaaaaaaaaaaaaa&admin=true

Our target block is:
(raw plaintext):
aaaaaaaaaaaaaaaa
(hex):
61616161616161616161616161616161
second last ciphertext block:
656117aa24402dbd7294b4f089cce890
(xor'd together):
040076cb45214cdc13f5d591e8ad89f1

make end zeros (ciphertext) (broken into blocks for clarity):
59454c4c4f57205355424d4152494e45 040076cb45214cdc13f5d591e8ad89f1 a69fc6d8d51b3447286f536539a66ce7
decrypted (hex)(compare this to the plaintext hex):
9ab4273a37ec12ef997ececbcfabf29200000000000000000000000000000000
decrypted (raw):
��':7��~��ϫ�                
```

So we can see that it completely garbles the edited block that used to be a bunch of ```a```'s, but we don't care about 
that, we only care about injecting nasties at will. We change the "Xor'd together" 
to xor against our desired plaintext, and we win!

```
(raw plaintext):
aaaaaaaaaaaaaaaa
(hex):
61616161616161616161616161616161
second last ciphertext block:
656117aa24402dbd7294b4f089cce890
(xor'd together):
040076cb45214cdc13f5d591e8ad89f1
Desired plaintext(raw):
aaaaa&admin=true
Desired plaintext(hex):
61616161612661646d696e3d74727565
(xor'd):
656117aa24072db87e9cbbac9cdffc94

Evil ciphertext(hex) (broken into blocks for clarity):
59454c4c4f57205355424d4152494e45 656117aa24072db87e9cbbac9cdffc94 a69fc6d8d51b3447286f536539a66ce7
Decrypted evil ciphertext(hex):
835f6a515b08f01cb1a6fc2420b4df4061616161612661646d696e3d74727565
Decrypted evil ciphertext(raw):
�_jQ[����$ ��@aaaaa&admin=true
```

Winner!

Right, now see if you can implement this yourself, there is a python file 
[aes cbc modify](aes_cbc_modify.py), your goal is to make the is_admin method
tell you that you are an admin, without modifying anything above the line - 
break it using crafted input only. Be aware that any '&' character, or 
'admin' values will be eaten. I've set the is_admin function to print the 
decrypted cookie out, to make it clear what it sees, this will help with 
debugging dramatically, however irl you don't get this luxury. **If you want to do this 
realistically, remove that print line**. As some help, there is a [utility](util.py)
file here too, to help deal with the cookie. It will show step by step how you
might tackle this problem, but with some old data.



