# Hashcat Dictionary style attacks

There is actually a few different dictinary attacks, but they are mostly
simple, so we will go through a few of them. A dictionary attack is only 
as strong as the dictionary file. Finding a good dictionary file for 
the task is an important step to take.

# Straight

A straight attack simply runs through the wordlist provided, and tries 
each line. If the word does not appear in the wordlist, the attempt will fail

The attack flag is 0, and this attack is available on both oclhashcat and hashcat

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
