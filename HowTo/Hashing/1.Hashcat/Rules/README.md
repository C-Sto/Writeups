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
Examples can be found uploaded.


## Replace
```
frog
fr0g
```

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
AddeA
