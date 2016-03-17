###### Hashcat

Hashing is fun and all, but if you are trying to find a collision, or 
find the un-hashed value it takes a lot of work. Thankfully, we have super 
fast processors and GPU's to do the hard work for us, we just need a program 
to send the work there... enter hashcat!

If you have access to GPU(s), you will want to use OCLHashcat, it uses the GPU 
instead of CPU.

OCL hashcat's command line usage is as follows:
oclHashcat [options] hash|hashfile [dictionary|mask|directory]

So for example, doing a brute force attack on an md5 hash would look like:

oclHashcat -m 0 5f4dcc3b5aa765d61d8327deb882cf99 -a 3 ?a?a?a?a?A?a?a?a


### Attack Types

In reality, all the modes of operation are important for certain tasks, 
however there are a few that will be used fairly often. Brute-force (mask)
 Dictionary, and Rule based are the three that will be most likely to be handy,
 so I'll go over those first.
 
 ##Brue force (Mask)
 
 The mask version of brute force is identical to normal brute-force, except 
 you have more control over what values are tried. If for example, you know 
 that the password consists only of numbers, you can tell hashcat to only try
 numbers. This makes the keyspace much smaller. It also means if the hash is 
 salted manually, you can apply that to it.
 
 Hashcat has the ability to use custom charsets (so, if you know it uses specific letters)
 and also has a few built-in.
 
 
