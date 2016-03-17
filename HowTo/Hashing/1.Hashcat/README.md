# Hashcat

Hashing is fun and all, but if you are trying to find a collision, or 
find the un-hashed value it takes a lot of work. Thankfully, we have super 
fast processors and GPU's to do the hard work for us, we just need a program 
to send the work there... enter hashcat!

If you have access to GPU(s), you will want to use OCLHashcat, it uses the GPU 
instead of CPU.

OCL hashcat's command line usage is as follows:

oclHashcat [options] hash|hashfile [dictionary|mask|directory]

Hashcat has not got the option to use a hash directly, it loads from a hash file only

hashcat [options] hashfile [dictionary|mask|directory]

So for example, doing a brute force attack on an md5 hash with 8 characters would look like:

oclHashcat -m 0 5f4dcc3b5aa765d61d8327deb882cf99 -a 3 ?a?a?a?a?a?a?a?a

## Hash type
The hash type is picked with the -m flag. There is a refrence list on the hashcat wiki.
The easiest way of identifying a hash is looking at the bit length of the output. Generally, 
there is only a few hash types it could be, so picking the most likely based on the bit length usually works.

## Attack Types

In reality, all the modes of operation are important for certain tasks, 
however there are a few that will be used fairly often. Brute-force (mask)
 Dictionary, and Rule based are the three that will be most likely to be handy,
 so I'll provide a brief overview here, then slightly more involved in it's own directory.
 
### Brute force (Mask)
 
A bruteforce attack, but we have more control over the values tried.
The built in masks:
 
 ```
 
?l = abcdefghijklmnopqrstuvwxyz
?u = ABCDEFGHIJKLMNOPQRSTUVWXYZ
?d = 0123456789
?s = «space»!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
?a = ?l?u?d?s
?b = 0x00 - 0xff

 ```
 
 Some example commands:
 
 ```
 
 #000-999
 oclHashcat -m 0 5f4dcc3b5aa765d61d8327deb882cf99 -a 3 ?d?d?d
 
 #0-999
 oclHashcat -m 0 5f4dcc3b5aa765d61d8327deb882cf99 -a 3 ?d?d?d --increment
 
 #aa00-zz99
 oclHashcat -m 0 5f4dcc3b5aa765d61d8327deb882cf99 -a 3 ?l?l?d?d
 
 #abc000-abc999
  oclHashcat -m 0 5f4dcc3b5aa765d61d8327deb882cf99 -a 3 abc?d?d?d
 
 ```