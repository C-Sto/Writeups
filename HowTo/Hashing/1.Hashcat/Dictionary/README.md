# Hashcat Dictionary style attacks

There is actually two different dictionary attacks (that work on both 
hashcat and oclHashcat), but they are mostly
simple, so we will go through both them. A dictionary attack is only 
as strong as the dictionary file. Finding a good dictionary file for 
the task is an important step to take, and like the mask attack, the more 
information you get, the more likely you will be to get the hash.

# Straight

A straight attack simply runs through the wordlist provided, and tries 
each line. If the word does not appear in the wordlist, the attempt will fail

The attack option is 0, and this attack works the same in both hashcat and 
oclHashcat

```hashcat -a 0 -m 0 hashfile wordlist```

# Combinator

The combinator attack is a variant of the straight attack, except it combines
words together to have more a more complicated search space. If the hash is 
something like 'fishfish', it won't be found in a straight attack, but will be 
found using the combinator attack.

The combinator attack is slightly different between oclhashcat and hashcat:

## hashcat

Only takes _one_ wordlist, and tries every combination of each word in it. For example

```hashcat -a 1 -m 0 hashfile wordlist```
with a wordlist of:
```
cat
dog
frog
```
would result in attempts that look like:
```
catcat
catdog
catfrog
dogcat
dogdog
...
frogfrog
```

## oclHashcat

takes _two_ wordlist values, one for left and one for right. This results 
in a slightly more flexible usage, if you know some parts of the password
only appear in the left or right hand side.

```oclhashcat -a 1 -m 0 hashfile leftwords rightwords```
with leftwords =
```
one
two
```

and rightwords =

```
dog
cat
frog
```

would result in attempts that look like:

```
onedog
onecat
onefrog
twodog
twocat
twofrog
```

In addition to being able to specify both wordlists, oclhashcat also allows
the usage of rules to be applied to each side. Take note, these are _rules_ 
and not masks. The -j and -k flags are used to specify rules to apply

```oclhashcat -a 1 -m 0 -j '$-' -k '$?' leftwords rightwords ```

would result in these attempts:

```
one-dog?
one-cat?
one-frog?
...
```

# Putting it into practise

Okay, let's have a look at the relevant challenge from Cysca2015. 
Remember, each 'password' is salted with ```cysca2015```

We are given the hash:
1ee4edda3890bcc543a5c8d0f1fc7e14c2ac4752286eb2549f61013b6645be91

So, if we load the hash with salt into a hashfile:
cysca2015:1ee4edda3890bcc543a5c8d0f1fc7e14c2ac4752286eb2549f61013b6645be91

Once we work out the hashtype, we can use the $salt.plain version.

We are also given an image of an obscure, unknown movie:

![image of hackers](https://github.com/CySCA/CySCA2015/blob/master/crypto_and_hash_cracking/files/images/challenge-2.PNG)

And the hint:

Dictionaries make easy pray for password cracking!
 
So, maybe we need to find the script, and use it as a dictionary?
(hint for this challenge, the word is lowercase so we _sorta_ need to pre-process the dictionary)

First, we find the script. It's easily available on the Googles, find it.
Now, we convert all the words to lowercase. There are a number of ways to do this, 
 pick your favourite.

Then, we find out the hash type. It's 64 hex chars long, which means it's 
32 bytes, or 256 bits. SHA256 would be a suitible guess.
This means that our hash type will be ```1420 = sha256($salt.$pass)```, 
taking our salt into consideration.

Now, we load the script into a straight dictionary attack, and try it:

``` hashcat -a 0 -m 1420 hashfile hackers_processed.script ```

and ta-da! we are done. Confirm it worked, you should get a result _Very_ quickly.

As a side note, because the word was so short, running a brute force attack 
while we worked out what we needed to do, and processing the dictionary file etc 
probably would have given us the result plaintext before we were done.

Dealing with dictionaries can be a pain, so I'll give some more crack-me 
hashes in the 'Rules' section.




