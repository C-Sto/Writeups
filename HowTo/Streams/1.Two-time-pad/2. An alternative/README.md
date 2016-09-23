# An alternative to Crib Dragging

So, we know the two time pad vulnerability, and we know how to crib-drag. However,
as you have noticed, it can be quite involved. Surely there is a way of 
automating this, right? Let's think about what we are actually doing when 
we crib drag...

1. We make a *guess* as to the plaintext, to reveal another part of the plaintext
2. If that's right, we use that part of the plaintext to find a partial key to reveal 
more plaintext
3. We use that partial key to make more educated guesses at the plaintexts

It boils down to making a guess, and checking to see if that guess is right.
What it looks like, if you visualise this, is we are checking sections horizontally.
We check a chunk at a time, and hope that it's right. What if instead of combining 
the two ciphertexts to eliminate the key, we make a guess at the key 
directly? If the key is generated correctly, this _shouldn't_ work as the key stream 
should be at least close to random (bytes, not limited to ascii), 
and if we even get one part of the key guess even a little wrong, the information we get 
may be unclear ``` 0x??*ed*???? -> ??(???? ``` when it is ``` 0xdeadbeef -> frog ```.
Effectively, what we want to do is make a guess at the smallest section of the 
key as possible, and check if it's right. This is impossible to do if you
have only _one_ ciphertext, but we don't, remember? We have multiple, and
they all use the same keystream...

```
key (we don't know this)
????????????????????????????????
CT1
c7e890aa42c1b1ed6c465caf26dcc32e
CT2
f8fc89a14484ace12f424db53bda843b
CT3
faf294ef4284b5f9635608aa27d78c32
```

So, if we guess a byte in the key, we get multiple outputs to test it against:
```
guessed key byte
01

CT1
c7
PT1
c6

CT2
f8
PT2
f9

CT3
fa
PT3
fb
```

We can _then_ guess only a byte, but check multiple outputs for correct-ness.
If we compare this to crib-dragging, this would look like a vertical test.
If we get one looking correct (within the ascii range) but two incorrect, 
we can be fairly certain that this guess is incorrect, and move on to the 
next one. It should be noted, that this will only work if you have a pretty 
good idea as to what the content will be. It also works better the more 
ciphertext you have, as you are giving it more things to score against.

One method for checking correctness, is using the chi-square test. 
We can look up expected letter frequencies (for english, for example), and plug them 
into the test. This will give us a scoring method, that should enable us 
to score each guessed byte based on how 'correct' it is. A lower chi-square result
 represents a 'better' score. So we use the test for each tested key byte, keep all the best bytes, 
and that should be the keystream, or at least a pretty good guess at it. 

This is a modified version of the test that has worked well for me for scoring
plaintexts, along with a rough english distribution:

``` python

eng_freq ={'a':8.167, "b":1.492, "c":2.782, "d":4.253, "e":12.702,
          "f":2.228, "g":2.015, "h":6.094, "i":6.966, "j": 0.153,
          "k":0.772, "l":4.025, "m":2.406, "n":6.749, "o":7.507,
          "p":1.929, "q":0.095, "r":5.987, "s":6.327, "t":9.056,
          "u":2.758, "v":0.978, "w":2.360, "x":0.150, "y":1.974,
          "z":0.074, " ":55.00, "\n":0.01, ".":6.53, ",":6.16,
          ";":0.32,  ":":0.34,  "!":0.33,  "?":0.56, "'":2.43,
          '"':2.67,  "-":1.53}


def chi_square_score(plaintext, distr):
    score = 0
    tested = []
    for char in distr.keys()+list(plaintext):
        # only test each character once
        if char in tested:
            continue
        # count the number of occurences of the character
        count = plaintext.count(char)
        # get the expected from the given distribution
        if(distr.has_key(char)):
            expected = distr.get(char)
        else:
            # this will give us a high number for any unexpected characters we run into
            expected = len(plaintext)*0.0001
        score+=((count-expected)*(count-expected))/expected
        tested.append(char)
    return score

```


## Putting it into practise

Okay, lets take some secret ciphertexts, an appropriately random key, do 
some stuff, and break them!

I'll use the xor function from the crib dragging example to perform the 
encryption, because I'm lazy:

``` python
def xor(s1,s2):
    shorter, longer = (s1,s2) if len(s1) < len(s2) else (s2,s1)
    out = ""
    for x in range(len(shorter)):
        v = chr(ord(longer[x])^ord(shorter[x]))
        out+= v
    return out

```
