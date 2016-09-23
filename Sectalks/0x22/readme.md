Here is the image we are given:
![Totally just an image](glorious_9f1c14d12dd8346047d00d2368c35e4a.png)

Given the context, it's probably not a regular image. The first thing we
should do when given any random file, is obviously run strings on it.
That didn't actually turn anything up this time, but it's always worth a
try. Next step I usually take is binwalk - and hey, that is more like it!

```
[root:~/Desktop]# binwalk -e glorious_9f1c14d12dd8346047d00d2368c35e4a.png

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
0             0x0             PNG image, 638 x 479, 8-bit/color RGB, non-interlaced
41            0x29            Zlib compressed data, default compression
208045        0x32CAD         Zip archive data, at least v2.0 to extract, compressed size: 901, uncompressed size: 1579, name: e.pyc
209084        0x330BC         End of Zip archive

```

If we use the -e flag with binwalk, it will extract everything it finds
into a handy directory for us. The interesting file is e.pyc -
a compiled python file. Provided it hasn't been encrypted,
.pyc files are relatively easy to decompile back to regular .py
using 'uncompyle'. If you don't already have it (probably don't) just 
`pip install uncompyle2` then use it with `uncompyle6 [file.pyc]`

```
[root:...00d2368c35e4a.png.extracted]# uncompyle6 e.pyc
# Python bytecode 2.7 (62211) disassembled from Python 2.7
# Embedded file name: ./e.py
# Compiled at: 2016-06-10 17:41:11
from PIL import Image
import sys
from re import sub
import base64
if len(sys.argv) != 3:
    print 'usage: ./e.py [in_img] [in_data] saves to out.png'
    sys.exit(0)
f = open(sys.argv[2])
d_clear = f.read().rstrip()
f.close()

def encode(text):
    return sub('(.)\\1*', lambda m: str(len(m.group(0))) + m.group(1), text)


d = encode(d_clear)
o = ''
for c in d:
    o += bin(ord(c))[2:].rjust(8, '0')

o_a = [ o[n:n + 2] for n in range(0, len(o), 2) ]
in_img = Image.open(sys.argv[1])
in_pixels = in_img.convert('RGB')
in_l = in_img.load()
width, height = in_img.size
if len(o_a) > width * height:
    print 'error: not enough canvas to paint with'
    sys.exit(0)
for i in range(0, len(o_a)):
    temp_x = i % width
    temp_y = i / width
    r, g, b = in_pixels.getpixel((temp_x, temp_y))
    new_r = int(bin(r)[2:8] + o_a[i], 2)
    in_l[temp_x, temp_y] = (new_r, g, b)

print 'finish: wrote %d times' % len(o_a)
in_img.save('out.png')
# okay decompiling e.pyc

```

So we can see a python script that appears to be hiding data
in the red pixels after a simple compression then binary conversion.
Presumably this is done on the original file. Constructing a script
to do the opposite is simple, just work backwards. There are three
major steps that need reversing, if we start at the last point of
the original python file:

``` python
in_img = Image.open(sys.argv[1])
in_pixels = in_img.convert('RGB')
in_l = in_img.load()
width, height = in_img.size
if len(o_a) > width * height:
    print 'error: not enough canvas to paint with'
    sys.exit(0)
for i in range(0, len(o_a)):
    temp_x = i % width
    temp_y = i / width
    r, g, b = in_pixels.getpixel((temp_x, temp_y))
    new_r = int(bin(r)[2:8] + o_a[i], 2)
    in_l[temp_x, temp_y] = (new_r, g, b)

```
We can see that it is appending an element of `o_a` to the r
value of each pixel. `o_a` is just a list consisting of two bits
`['00', '10', '11']` of an arbitrary length (we don't know how big
the message is). So, to reverse this step, we simply need to take
the last two bits of each r value of each pixel, then store it in a
list. Bearing in mind, this list will be way too big, and consist of
mostly junk (the original code only encodes as many pixels as
it needs).

```python
rev_o_a = []
for i in range(0, width * height):
  temp_x = i % width
  temp_y = i / width
  r, g, b = in_pixels.getpixel((temp_x, temp_y))
  rev_o_a.append(bin(r)[-2:])
```

moving up through the file - we have the equivalent of `o_a`, so we
need to get it back to `o`, then `d`, then `d_clear`. To turn our list
into a binary string is trivial:

```python
rev_o = "".join(rev_o_a)
```

Now going from `o` to `d` is easy.

```python
for c in d:
    o += bin(ord(c))[2:].rjust(8, '0')
```

So, it's just taking the ascii value of each character, converting it
to binary and right-aligning it to be exactly 8 bits wide. Thanks to
the right align we can just convert every 8 bits into an ascii
character

```python
rev_d = ""
for i in range(0, len(rev_o),8):
  rev_d += chr(int(rev_o[i:i+8],2))

```

Which brings us to the complicated looking `encode()` function.

```python
def encode(text):
    return sub('(.)\\1*', lambda m: str(len(m.group(0))) + m.group(1), text)
```

It's not that complicated - all it does is take a string, and perform
a simple 'compression' function on it. A string of `hello` would turn
into `1h1e2l1o`. An integer representing the number of repeats,
followed by the character that repeats. Since we can be relatively
sure that nothing in our flag will repeat more than 9 times, we can
simply look at every pair of characters in the string, and rebuild
`d_clear` from that. Additionally, as soon as we hit a character pair
that doesn't start with a number, we can be pretty sure that we don't
care about the rest.

```python
rev_d_clear = ""

for i in range(0, len(rev_d), 2):
  if not rev_d[i].isdigit():
    break
  rev_d_clear+= int(d[i])*d[i+1]
```

After that, we have the decoded original value. See unhide.py for the
runnable decoder.
