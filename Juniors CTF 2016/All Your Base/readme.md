## Task Text
### “All your base are belong to us”

Once in Mystery Shack


- Gruncle Stan, where are you going?
- Guys, I'm going to Las Vegas. Gonna con them into giving me all their money. Haha.
- Gruncle, Mabel has already been a head while you were away last time. May I take a lead now?
- As you wish, Dipper. I'll leve you my cash. As I arrive in LA, I'll send you an email with an account number.
- But Gruncle, how will I know that the message is from you?
- Ha, McGucket has invented electronic signature. I'll use it. You will have a verification key and I will have a signature key.
- Ok, Gruncle Stan. I'm going to do it right. Have fun in LA.

A few hours later (Gideon is muttering to himself)


- Eventually I've got a chance to take Stan's Mystery Shack.
- I'll steal the money while Dipper will be sending it to Stan.
- Genious. But how will we do this? Dipper is going to use the bank services.
- It means that we only have to figure out the way how the money ends up in my hands.
- I'll fake Stan's message and write in the number of my account. Haha.
- Yeah, that's genious. But Stan uses McGucket's e-signature. Dipper will instantly realize what is going on.
- McGucket is so dumb that he used CRC32 insead of regular hash. It'll be dead easy to hack it.
- But I don't know anything about hashes, keys and cryptography. What am I supposed to do?
- You can seek for help. It seems I know someone who will attempt to do this.
On the next day Gideon captured the message from Stan with an account number. Change the message:
~~~
############ BEGIN SIGNED MESSAGE ############
send me $ 10,000 to the account 9589234485239
############## BEGIN SIGNATURE ###############
0x64ce88bd59abad6c3f2247f9109bac5d2c1b7d6L
0x5a39c115fef0ff943740a0cbef07a762478520f6L
############# END SIGNED MESSAGE #############
~~~
Write in Gideon's accout number there: 0102128506010 and dispatch it.
You can send a message via online messager

Lupanov M.Iu.

## Solution

This looks like a simple message forgery task - made much easier by the fact that we are told that CRC32 is used as the hashing function, rather than a secure alrgorithm.

The basic idea is that we do not know the keys associated with the signature, and may only change the text of the message. CRC32 has a very small domain, so simply iterating through padding bytes wouldn't take long. However, because of the way CRC's are calculated, we can simply append 4 bytes and have direct control over the resulting value. This means we can alter the message to whatever we want, and it will retain the same 'hash' value, making the signature valid.

Initially, I thought I was having problems with the padding, as the message was a different length with 4 bytes appended, but it turned out it was just my text editor inserting a newline every time I saved the file :|. The term for this is 'patching' the message and there exists a handful of tools that will add the last 4 bytes - I found a nice python script that will actually alter _any_ 4 sequential bytes in the given file to give us the CRC output we want. After trying a few different offsets within the file, I kept getting messages along the lines of "We don't understand the message" - appending 5 spaces and altering the last 4 gave us the win.

`forcecrc32.py patched.txt 47 0d1bffe1`