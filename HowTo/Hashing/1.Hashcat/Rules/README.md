# Rules
Hashcat rules are where hash-cracking really starts to become an art. 
Using rules in combination with a dictionary attack allows you to have a 
relativly small dictionary, but attempt many different variations of each 
word. It takes the word, applies certain rules to it (hence the name) and 
then checks those resulting hashes. I'll show a few of the more commonly used 
rules, get a full list of rules at the hashcat wiki (https://hashcat.net/wiki/doku.php?id=rule_based_attack).
To use rules, you need to build a rules file. This is a file that contains 
a set of rules to run against each word, each line defines a new rule, 
so if you want to run multiple rules against the same word (to get different outputs)
just add a newline. Be aware that for every rule, it will test the plaintext 
 _for that rule_. That means that for complex rulesets, you _may_ be testing 
 the same plaintext many times (using lots of rules doesn't always work better). 
 Another thing to remember is that using rules takes up CPU power, so an 
 attack that implements complicated rules will always be slower than one 
 without rules. There are some intricacies in terms of which versions have which rules, 
 But I tend to go on the 'try and see' basis.
 
 An excellent way of making sure your rules are working properly is using 
 the --stdout argument. The only problem with this is that this will only 
 work with hashcat, oclhashcat will not work with the --stdout argument.


## Replace

As you would expect, using a 0 instead of an o in frog will foil a dictionary 
attempt. We can get it by using the 'replace' rule:

```
Rule:
s
Usage:
sXY where X = the existing character and Y = the character to be replaced
Example rule:
so0
Example output:
frog => fr0g
dog => d0g
cat => cat
```
Using multiple rules in the same line:

```
Example rule:
sa4so0
Example output:
analog => 4n4l0g
```

## Append

Another popular password strategy is to append a number, think 'princess90' 
or 'hotdogs1991'. Neither of those will appear in a dictionary, so we can 
write a rule that appends a character or two to the file.

```
Rule:
$
Usage
$X where X = the character to append
Example rule:
$0
Example output:
frog => frog0
cat => cat0
```

Unfortunately, if we want to append numbers 0 through 9 (cat0, cat1..etc)
we have to write a new rule for _each_. This can be cumbersome, especially 
if you want to write 1900-2029. Writing a python script is one option, or 
possibly using a shell script, but there is a simpler option - maskprocessor!

We can use maskprocessor -o to send the output into a file. So doing 1990 
through 2020 would be as simple as doing the two maskprocessor commands:

``` maskprocessor 19?d?d -o years```

``` maskprocessor -1 012 20?1?d -o years```

However, we want the numbers in a valid rule format. So we change the command
to have a $ (for append) before each character (since this is done in the 
terminal, we need to escape by wrapping the mask in ''s):

``` maskprocessor '$1$9$?d$?d' -o years.rule ```

``` maskprocessor -1 012 '$2$0$?1$?d' -o years.rule```

We need to remember, though, that _each_ of these rules will be applied to 
_every_ word in the wordlist, which will mean our wordlist size will be 
numberofrules*numberofwords (which can get big very quickly).


# In practise

Okay, lets have a look at the relevant Cysca2015 hash.

The hash (with salt):

3bb2dd1a9b36f4745e994e3bea658e79:cysca2015

The hints:

We are given the XKCD image:

![stuff](https://github.com/CySCA/CySCA2015/blob/master/crypto_and_hash_cracking/files/images/challenge-3.png?raw=true)

A dictionary file (found uploaded)

And the words:

Maybe substitution is too simple with today's password crackers.

Let's look at the hash type first. Right off the bat, it looks like a short hash, 
so it's probably md5. If we count the bits of output (hex/2)*8, we see that 
it's 128 bits of output, so, yes, it's most likely md5.
Taking our salt into consideration, our hashing mode will be -m 20 md5($salt.$plain)

Looking at the XKCD, we can guess that the substitutions are _probably_ 
going to be simple 'leet' substitutions (a for 4, o for 0, etc). Let's first 
try a full substitution, since partial or one time substitution rules as seen 
in the comic are slightly more complicated to write. Our rule will look like:

``` sa4so0si1se3 ```

Let's try it with their dictionary:

```hashcat -a 0 -m 20 hashfile dictionary -r rulefile ```

huh, it didn't work? Let's look a bit closer at the xkcd comic, it has a 'special'
character and number appended. We can do that using our maskprocessor trick:

```maskprocessor -1 ?s?d 'sa4so0si1se3$?1$?1' -o rulefile ```

Still nothing... How about the first letter capital? That's a rule we can 
look up. It turns out that adding a lower case 'c' will capitalise the first 
letter, and since we've tried the lowercase versions, it's worth a go!

```maskprocessor -1 ?s?d 'csa4so0si1se3$?1$?1' -o rulefile ```


Wahey! we have a winner. Verify the result.

Here are some hashes to try out your l33t new skillz.

Remember that all plains begin with ```ecu_cysca_training{``` and have a ```}``` at 
the end. You can do this using the maskprocessor trick, or you can use the 
hash salt syntax, no rules. All passes are using the provided dictionary 
file, and _some_ sort of rule/s.

Hash:
51335e337e4c6be887c97aa97dd855bc1f05dcb03badcc1ad2f8f0471f4f146c

Hint:
sup3r 3asy

Hash:
44b3aeb6e5ae9baba6254e3d5c0e377f88fac7f6dbdeb931e4ca8dba2ace8a4e

Hint:
The year of the hipster submarine thing

Hash:
92a65a2dee5bcb79dbe2985f2319c5fdc33583d4211f8c23747d25d07240ea61

Hint:
if a password is too short, just double it right?

Hash:
2277090479ad9447de920de8288c11abe8fc1a8d7ce6d6ca1eca6ff8c30032e5

Hint:
drowssap

Hash:
0d2f93b486f91ffe093a01b28b47e6ec855f6af0993bcc74efe22161d188c046

Hint:
if a password isn't good, just add 4 numbers to the end


