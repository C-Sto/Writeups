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
 so I'll go over those first.
 
### Brute force (Mask)
 
 The mask version of brute force is identical to normal brute-force, except 
 you have more control over what values are tried. If for example, you know 
 that the password consists only of numbers, you can tell hashcat to only try
 numbers. This makes the keyspace much smaller, and cracking task much easier. It also means if the hash is 
 salted manually, or you know a part of the password, you can add it to the mask.
 
 The mask added to the end specifies the length. This can be overridden with the 
 --increment flag. With the --increment flag, the mask specifies the maximum length to test.
 
 Hashcat has the ability to use custom charsets. There is also some built in
  charsets, they are as follows:
 
 
 ```
 
?l = abcdefghijklmnopqrstuvwxyz
?u = ABCDEFGHIJKLMNOPQRSTUVWXYZ
?d = 0123456789
?s = «space»!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
?a = ?l?u?d?s
?b = 0x00 - 0xff

 ```
 
 To do a masked brute force, we specify the attack type 3. To use just the 
 inbuilt masks, simply add the mask at the end. Here are some examples.
 
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
 
 We can also specify our own mask. To do this, we specify the mask number 
 and then the characters that should exist in it. doing it this way, we can 
 generate multiple masks
 
 ```
 
 #abc111-abcddd
 oclHashcat -m 0 5f4dcc3b5aa765d61d8327deb882cf99 -a 3 -1 123abcd abc?1?1?1
 
 #abc11155-abcddd77
 oclHashcat -m 0 5f4dcc3b5aa765d61d8327deb882cf99 -a 3 -1 123abcd -2 567 abc?1?1?1?2?2
 
 ```
 
 There is also a handy tool bundled with hashcat (usually) called maskprocessor.
 We can use this as a wordlist generator, in case we need to manually implement a 
 hash function to test, or need to customize on for a task. Or, to make sure the mask
 does what we expect it to do.
 
 ```
 #00aa-99zz
 maskprocessor ?d?d?l?l
  
 ```
 
 Cool! so, lets test it. One of the previous CYSCA2015 challenges was to 
 crack a hash based on a picture of a pin pad. The hash value is:
 
 ```
 
 0137d1896047cbf24bcb18f79a9ad475933ad229
 
 ```
 That hash value is 20 bytes long, which means a 160 bit hash function. 
 SHA1 is the most likely candidate (-m 100). Here is the picture provided:
 
 ![Image of pin pad](https://github.com/C-Sto/Writeups/blob/master/HowTo/Hashing/1.Hashcat/challenge-1.png)
 
 We are told that the value is salted with the value "cysca2015" and 16 digits long.
 
 So, using that information, we can devise a custom mask ```-1 0942```
 
 Put that together with the length of 16, and the salt, results in the hashcat 
 command of
 
 ```
 oclhashcat -m 100 0137d1896047cbf24bcb18f79a9ad475933ad229 -a 3 -1 0942 cysca2015?1?1?1?1?1?1?1?1?1?1?1?1?1?1?1?1
 
 ```
 
 
