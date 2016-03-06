# Writeups for the Boston Key party CTF 2016

[1] : Cookbook - 6 - 20 solves : pwn: a top chef wrote this cookbook for me but i think he has an extra secret recipe! https://s3.amazonaws.com/bostonkeyparty/2016/58056c425dc617b65f94a8b558a4699fedf4a9fb.tgz cookbook.bostonkey.party 5000  
[2] : Simple Calc - 5 - 153 solves : pwn: what a nice little calculator! https://s3.amazonaws.com/bostonkeyparty/2016/b28b103ea5f1171553554f0127696a18c6d2dcf7 simplecalc.bostonkey.party 5400  
[3] : hmac_crc - 5 - 31 solves : crypto: We're trying a new mac here at BKP---HMAC-CRC. The hmac (with our key) of "zupe zecret" is '0xa57d43a032feb286'.  What's the hmac of "BKPCTF"? https://s3.amazonaws.com/bostonkeyparty/2016/0c7433675c3c555afb77271d6a549bf5d941d2ab  
[4] : Frog Fractions 2 - 5 - 53 solves : reversing: Turns out Frog Fractions 2 is not battletoads https://s3.amazonaws.com/bostonkeyparty/2016/05223a3cae8b71d81592d5977fb1c3622bcbf793  NOTE: key in different format flag is md5 of the key (incl newline at the end, sorry for crazy flag format), with BKPCTF{} around it, eg BKPCTF{764efa883dda1e11db47671c4a3bbd9e}  
[5] : segsh - 6 - 21 solves : pwn: segsh.bostonkey.party 8888  https://s3.amazonaws.com/bostonkeyparty/2016/405b72ee16deada7a9f899cef8a7e0e5.tar flag lives in /home/segsh/flag  
[6] : Found it? - 1 - 732 solves : misc: BKPCTF{hello world} is the flag
[7] : Good Morning - 3 - 85 solves : web: http://52.86.232.163:32800/  https://s3.amazonaws.com/bostonkeyparty/2016/bffb53340f566aef7c4169d6b74bbe01be56ad18.tgz
[8] : gsilvis counting magic - 9 - 4 solves : crypto: Here's a verification/decryption server:  gcm.ctf.bostonkey.party:32768 .  Get the GCM MAC key (the thing the server prints out on startup).  We've given you one valid ciphertext to get you started.  It has  iv: [102 97 110 116 97 115 116 105 99 32 105 118] and tag: [119 179] https://s3.amazonaws.com/bostonkeyparty/2016/a8730f449f0c6b985790fb4df3ebae4c01556648.tar
[9] : des ofb - 2 - 167 solves : crypto: Decrypt the message, find the flag, and then marvel at how broken everything is. https://s3.amazonaws.com/bostonkeyparty/2016/e0289aac2e337e21bcf0a0048e138d933b929a8c.tar
[10] : unholy - 4 - 51 solves : reversing: python or ruby? why not both! https://s3.amazonaws.com/bostonkeyparty/2016/9c2b8593c64486de25698fcece7c12fa0679a224.tar.gz
[11] : spacerex - 8 - 6 solves : pwn: spacerex.bostonkey.party 6666 https://s3.amazonaws.com/bostonkeyparty/2016/3cac632a559f062e71fc09b2629f2f8b.tar
[12] : lily.flac - 2 - 17 solves : misc: more than just a few bleebs ;) https://s3.amazonaws.com/bostonkeyparty/2016/87582357ff1a7c3e8d11c749ac12ad819f8f7d4b
[13] : complex calc - 5 - 58 solves : pwn: we've fixed a tiny bug! https://s3.amazonaws.com/bostonkeyparty/2016/d60001db1a24eca410c5d102410c3311d34d832c simplecalc.bostonkey.party 5500
[14] : Bug Bounty - 3 - 32 solves : web: grill the web! http://52.87.183.104:5000/
[15] : More Like ZKP - 4 - 29 solves : crypto: We've made a zero-knowledge proof protocol for graph 3-coloring.  Here are  prover (52.86.232.163:32795) and verifier (52.86.232.163:32794) servers.  Convince the verifier that you know the prover's graph-coloring! https://s3.amazonaws.com/bostonkeyparty/2016/48cdc8756b6a9a5052c6da2d061b9bd61d13a1fa.tgz
[16] : qwn2own - 10 - 1 solves : pwn: hack it. https://s3-us-west-1.amazonaws.com/qwn2own/d0cb00dc266da1c42335d54d2bbd41bf-v2.tar the binary hasn't changed or been recompiled, one line in the source code has been commented out since it was not compiled in the first place ctf.bostonkey.party 9090 for details
[17] : feistel - 5 - 9 solves : crypto: I just made a brand new cipher!  Can you recover the key? https://s3.amazonaws.com/bostonkeyparty/2016/365ed3941ca31214edfa942df37e73726bc07d0f   52.86.232.163:32785 Revert mistaken point value from 3 to 5 before any solves.  Please tell gsilvis if you think this is unfair, and we may un-revert
[18] : OptiProxy - 2 - 62 solves : web: inlining proxy here http://optiproxy.bostonkey.party:5300
[19] : bob's hat - 4 - 46 solves : crypto : Alice and Bob are close together, likely because they have a lot of things in common. This is why Alice asked him a small *q*uestion, about something cooler than a wienerhttps://s3.amazonaws.com/bostonkeyparty/2016/b36f750ea5ea90f54b0f983d3c7ad9ce672bbd5a.zip
[20] : Jit in my pants - 3 - 20 solves : reversing: Because reversing an obfuscated jit'ed virtual machine for 3 points is fun! https://s3.amazonaws.com/bostonkeyparty/2016/c3803116bd70e802483d3bc4c4b564d2
[21] : ltseorg - 4 - 25 solves : crypto: make some (charlie)hash collisions! ltseorg.bostonkey.party 5555 https://s3.amazonaws.com/bostonkeyparty/2016/a531382ad51f8cd2b74369e2127e11dfefb1676b.tar
