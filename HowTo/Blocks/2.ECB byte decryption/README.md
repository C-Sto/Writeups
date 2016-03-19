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
Enter some stuff to encrypt: a
Length of ciphertext:  976
Enter some stuff to encrypt: aa
Length of ciphertext:  976
```

```
Enter some stuff to encrypt: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
Encrypted spaced version:  ['1348a59a24520f9a12a36eb06fbd3868', '1348a59a24520f9a12a36eb06fbd3868', '8d93e891c6d8d4ddf8a92cfd7fb01f59', 'c392e64bc273eb2b3caa421abc1edb8b', ...
```

Right, with that out of the way, we can see the two repeated ciphertext blocks. If we remove one char from the end of our
padding, we end up with something like this

```
[aaaaaaaaaaaaaaaa][aaaaaaaaaaaaaaa?] -> ['1348a59a24520f9a12a36eb06fbd3868', '3ec16d8bcc2b1a540417d43edc2d58da',...
```

So how do we figure out what the last character is? Simple, submit a potential block until a block with known values
matches a block with the unknown value.

```
[aaaaaaaaaaaaaaab][aaaaaaaaaaaaaaa?] -> ['6aef3dabf400aecd73277cab3e05e42b', '3ec16d8bcc2b1a540417d43edc2d58da',...
[aaaaaaaaaaaaaaac][aaaaaaaaaaaaaaa?] -> ['7314155691632ccd2d2ff77eba983ba8', '3ec16d8bcc2b1a540417d43edc2d58da',...
[aaaaaaaaaaaaaaad][aaaaaaaaaaaaaaa?] -> ['b5dd247f53887415f66022c85d40baaa', '3ec16d8bcc2b1a540417d43edc2d58da',...
...
[aaaaaaaaaaaaaaaA][aaaaaaaaaaaaaaa?] -> ['3ec16d8bcc2b1a540417d43edc2d58da', '3ec16d8bcc2b1a540417d43edc2d58da',...
```

Once it does, we know the value of that last byte, and can do the same thing until we eventually reveal the whole plaintext.

```
[aaaaaaaaaaaaaaAa][aaaaaaaaaaaaaaA?] -> ['22c85070321d45bf22ff0ff2ace4e1b3', '9da4bdde6634e9bcbff66e75531df10e',
[aaaaaaaaaaaaaaAb][aaaaaaaaaaaaaaA?] -> ['f201e6b89cea7fd1f9c4081ff44cae41', '9da4bdde6634e9bcbff66e75531df10e',
...
etc
```

Strongly suggest you do this in code, or it is going to take a fairly long time with a fair amount of frustration. I have 
included a python script, feel free to modify it below the do not modify line to get it working - and try to avoid the 
temptation of decoding the base64 directly, or using the key.