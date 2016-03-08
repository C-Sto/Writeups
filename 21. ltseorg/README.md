#### Solution

First we have a look at the ruby file. We notice that what we need to get the flag 
is a 'success' response from the python file

```ruby
    exec = "python ./tlseorg.py --check #{Shellwords.shellescape s1} #{Shellwords.shellescape s2}"
        out = `#{exec}`
    puts out
    if out == "Success\n"
      conn.puts "FLAG"
```

After looking at the python file, it seems it is possible to generate a hash collision wil some effort, but something
caught my eye..

``` python

def check(hashstr1, hashstr2):
  hash1 = binascii.unhexlify(hashstr1);hash2 = binascii.unhexlify(hashstr2)
  if hashstr1 == hashstr2 or hash1 == hash2: return False
  elif hash(hash1) == hash(hash2): return True
  return False
  
```

The check function appears to do a fairly thorough test for equality, but not quite thorough enough.
Passing in a two strings with different lengths of null bytes will result in an equality check failing,
but the hash function relies on the value passed in (which is zero for both strings)
will result in the same hash. Much easier than generating a collision the manual way.

```
gimme str 1  
\0x00
gimme str 2  
\0x00\0x00
BKPCTF{really? more crypto?}
```
