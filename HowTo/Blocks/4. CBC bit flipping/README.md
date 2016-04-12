# CBC Bitflipping

Another encryption scheme is CBC. This scheme uses the output of the previous 
block as a way of preventing some of the attacks on ECB, we can't see the 
penguin anymore.

[image showing cbc](CBC_encryption.png)

Drats, foiled... or have we been?

Let's say we have an encrypted cookie that we want to add an admin credential to.
The plaintext looks something a bit like this:

```
?userdata=<your_user_data_goes_here>&colour=red&sometext=fifty%20shades%20of%20grey
```

so, knowing this, we want to add ```&admin=true``` to the end.

Let's make some assumptions:

1. We have full control over ciphertext
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

Here is an example:

plaintext(raw):
athisissomeencryptedtexthereandavaluethatwewanttochangeattheendd
ciphertext(hex):
8747d3b26b087c519ef966585cb0deccea569ece51102d87d5660642e28eb9898f428cd4d36427c14d75f493f671fd583c811c023de691e84b208aadac22ff9a

desired plaintext at end:
ogiveacookietooo
which would make our plaintext:
athisissomeencryptedtexthereandavaluethatwewanttogiveacookietooo

Our target block is:
(raw plaintext):
ochangeattheendd
(hex):
6f6368616e67656174746865656e6464
previous ciphertext:
8f428cd4d36427c14d75f493f671fd58
(xor'd together):
e021e4b5bd0342a039019cf6931f993c

make end zeros (ciphertext):
8747d3b26b087c519ef966585cb0deccea569ece51102d87d5660642e28eb989**e021e4b5bd0342a039019cf6931f993c**3c811c023de691e84b208aadac22ff9a
decrypted (raw):
'athisissomeencryptedtexthereanda)\xeaz6WT\xdf\xd5{v\xd3\xd7\xc6!2\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

So we can see that it completely garbles the edited block, but we don't care about 
that, we only care about injecting nasties at will. We change the "Xor'd together" 
to xor against our desired plaintext, and we win!





