```
Dance
55

judges: dwn, xan

Some prefer the stanky leg, others prefer the dab, but what dance moves do you have?

nc 4.31.182.242 9001

```

After loading up the supplied binary locally and looking at the memory during execution
we can see that we need to have the memory region 12 bytes before EBP matching the byte
string given. If we supply enough padding, we can put the values there - however entering 
raw bytes in bash is hard, so instead we echo with the flags -ne

```
echo -ne "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\x12\xetc " | nc 1.2.3.4 1234
```

