## Task text

### Clone Attack

Gravity Falls is under clones attack. Find the real Dipper and save the town

## Solution

We are given a zip full of images (a fair few!). A handy tool to look at image metadata (at least on kali) is `identify` Using `identify -verbose` on one of the images we can see a bunch of info about it:

~~~
Image: a2lGu9cpu1BwenzC.jpg
  Format: JPEG (Joint Photographic Experts Group JFIF format)
  Mime type: image/jpeg
  Class: DirectClass
  Geometry: 193x400+0+0
  Resolution: 72x72
  Print size: 2.68056x5.55556
  Units: PixelsPerInch
  Type: TrueColor
  Endianess: Undefined
  Colorspace: sRGB
  Depth: 8-bit
  Channel depth:
    red: 8-bit
    green: 8-bit
    blue: 8-bit
  Channel statistics:
    Pixels: 77200
    Red:
      min: 0 (0)
      max: 255 (1)
      mean: 189.903 (0.744717)
      standard deviation: 93.8289 (0.367957)
      kurtosis: -0.842952
      skewness: -0.963782
    Green:
      min: 0 (0)
      max: 255 (1)
      mean: 178.252 (0.699026)
      standard deviation: 91.4573 (0.358656)
      kurtosis: -1.19494
      skewness: -0.696072
    Blue:
      min: 0 (0)
      max: 255 (1)
      mean: 173.78 (0.681491)
      standard deviation: 90.9233 (0.356562)
      kurtosis: -1.2435
      skewness: -0.587732
  Image statistics:
    Overall:
      min: 0 (0)
      max: 255 (1)
      mean: 180.645 (0.708411)
      standard deviation: 92.0785 (0.361092)
      kurtosis: -1.10607
      skewness: -0.749659
  Rendering intent: Perceptual
  Gamma: 0.454545
  Chromaticity:
    red primary: (0.64,0.33)
    green primary: (0.3,0.6)
    blue primary: (0.15,0.06)
    white point: (0.3127,0.329)
  Background color: white
  Border color: srgb(223,223,223)
  Matte color: grey74
  Transparent color: black
  Interlace: JPEG
  Intensity: Undefined
  Compose: Over
  Page geometry: 193x400+0+0
  Dispose: Undefined
  Iterations: 0
  Compression: JPEG
  Quality: 90
  Orientation: Undefined
  Properties:
    comment: Flag is MD5sum of this file. Its TRUE
    date:create: 2016-11-24T17:10:38-05:00
    date:modify: 2016-11-02T23:56:08-04:00
    jpeg:colorspace: 2
    jpeg:sampling-factor: 1x1,1x1,1x1
    signature: 447df3a1e9a0be21948802a1edfcb0383f11f20afd7582f8c4cd6f7ac738c16c
  Profiles:
    Profile-8bim: 76 bytes
    Profile-iptc: 64 bytes
      City[1,90]: 0x00000000: 254700                                        -%
      unknown[1,0]:
      Image Name[2,5]: Ксерокопия  номер  915
      unknown[2,0]:
  Artifacts:
    filename: a2lGu9cpu1BwenzC.jpg
    verbose: true
  Tainted: False
  Filesize: 26.6KB
  Number pixels: 77.2K
  Pixels per second: 7.72MB
  User time: 0.010u
  Elapsed time: 0:01.009
  Version: ImageMagick 6.8.9-9 Q16 i686 2016-06-29 http://www.imagemagick.org
~~~

One of the interesting bits is the comment:
~~~
Properties:
    comment: Flag is MD5sum of this file. Its TRUE
~~~

So we need to find the original, and submit the md5 of that. Presumably, this means that all of the images are slightly different in some way - so a simple bash one liner will show us all of the unique details:

`for f in *.jpg; do  identify -verbose $f; done | sort -u`

This command iterates over each jpg file in the directory, runs the imagemagick identify utility on it, and pipes the output into the 'sort' command. The sort command sorts every line, and removes duplicates (-u) to only show us unique lines. This should give us an idea of what we might be looking for.

~~~
Artifacts:
Background color: white
  Blue:
  blue: 8-bit
  blue primary: (0.15,0.06)
Border color: srgb(223,223,223)
Channel depth:
Channel statistics:
Chromaticity:
    City[1,90]: 0x00000000: 254700                                        -%
Class: DirectClass
Colorspace: sRGB
  comment: Flag is MD5sum of this file. Its TRUE
Compose: Over
Compression: JPEG
  date:create: 2016-11-24T17:10:38-05:00
  date:modify: 2016-11-02T23:56:07-04:00
  date:modify: 2016-11-02T23:56:08-04:00
Depth: 8-bit
Dispose: Undefined
Elapsed time: 0:01.000
Elapsed time: 0:01.009
Elapsed time: 0:01.010
Elapsed time: 0:01.019
Endianess: Undefined
  filename: 07snLOxf2k0rRrT3.jpg
  ...snip...
  filename: ZZHazeaBrYUOdf7f.jpg
Filesize: 26.6KB
Format: JPEG (Joint Photographic Experts Group JFIF format)
Gamma: 0.454545
Geometry: 193x400+0+0
  Green:
  green: 8-bit
  green primary: (0.3,0.6)
Image: 07snLOxf2k0rRrT3.jpg
...snip...
Image: N9E8oy6VvrhwgjA0.jpg
    Image Name[2,5]: Ксерокопия  номер  000
    Image Name[2,5]: Ксерокопия  номер  001
    ...snip...
    Image Name[2,5]: Ксерокопия  номер  999
    Image Name[2,5]: Оригинальный Диппер
Image: nB19ZzUPu1xGt34A.jpg
...snip...
Image: ZZHazeaBrYUOdf7f.jpg
Intensity: Undefined
Interlace: JPEG
Iterations: 0
  jpeg:colorspace: 2
  jpeg:sampling-factor: 1x1,1x1,1x1
    kurtosis: -0.842952
    kurtosis: -1.10607
    kurtosis: -1.19494
    kurtosis: -1.2435
Matte color: grey74
    max: 255 (1)
    mean: 173.78 (0.681491)
    mean: 178.252 (0.699026)
    mean: 180.645 (0.708411)
    mean: 189.903 (0.744717)
Mime type: image/jpeg
    min: 0 (0)
Number pixels: 77.2K
Orientation: Undefined
  Overall:
Page geometry: 193x400+0+0
  Pixels: 77200
Pixels per second: 0B
Pixels per second: 3.86MB
Pixels per second: 7.72MB
Print size: 2.68056x5.55556
  Profile-8bim: 76 bytes
  Profile-iptc: 64 bytes
Profiles:
Properties:
Quality: 90
  Red:
  red: 8-bit
  red primary: (0.64,0.33)
Rendering intent: Perceptual
Resolution: 72x72
  signature: 447df3a1e9a0be21948802a1edfcb0383f11f20afd7582f8c4cd6f7ac738c16c
    skewness: -0.587732
    skewness: -0.696072
    skewness: -0.749659
    skewness: -0.963782
    standard deviation: 90.9233 (0.356562)
    standard deviation: 91.4573 (0.358656)
    standard deviation: 92.0785 (0.361092)
    standard deviation: 93.8289 (0.367957)
Tainted: False
Transparent color: black
Type: TrueColor
Units: PixelsPerInch
    unknown[1,0]:
    unknown[2,0]:
User time: 0.000u
User time: 0.010u
  verbose: true
Version: ImageMagick 6.8.9-9 Q16 i686 2016-06-29 http://www.imagemagick.org
  white point: (0.3127,0.329)
~~~

A whole bunch of garbage - I've removed the 'image filename' and most of the 'Image Name' things, in retrospect this was a bad way of doing it. The cyrillic in the 'Image Name' portion translates to 'no photocopy xxx' - and when looking over the results initially I completely missed the other text:  `Оригинальный Диппер` which roughly translates to 'the real dipper' (thanks to my teammate Snades who spotted it!). So we are looking for the file that has this text in it - another dirty bash one liner:

`for f in *; do if grep Оригинальный $f; then echo "$f";fi; done`

which gives us

`Binary file atvF2wf1tfB2IkuV.jpg matches
atvF2wf1tfB2IkuV.jpg`

so the flag:
~~~
root@kali:~/Desktop/ctf/Junior/dipper (1)# md5sum atvF2wf1tfB2IkuV.jpg
cd4d19b8471cecbc8ea7544de59db368  atvF2wf1tfB2IkuV.jpg
~~~

