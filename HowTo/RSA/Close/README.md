I'm assuming that you've read the overview on RSA, so I won't explain
 it's parts again. I *will* refer to them, though, so if you need a memory
 jog, look back at it.

When primes P and Q are too close together, it becomes extremely easy to 
break RSA. This is not immediately obvious from the public key, and in most cases
if the primes were generated the normal way, it's almost impossible for them to be close enough
for this attack to be possible. Nevertheless, home brew crypto implementations 
do exist out there, and more importantly there are flags to get in CTFs.

The general overview is that if P and Q are close together, simply factoring from 
the square root of N should result in either P or Q in a very short amount of time. 
There are lots of mathy ways to do this, I've included rsa-close.py so that 
you can use the right algorithms without needing too much research.

First, we need to factor N. Since the primes are close together, Fermats method
will do nicely. You don't need to understand how it works, but it starts at 
about the square root of n, which is what we want for this weakness.

``` python

def fermat(n, verbose=True):
    a = isqrt(n) #integer square root, 
    b2 = a*a - n
    b = isqrt(n)
    count = 0
    while b*b != b2:
        if verbose:
            print('Trying: a=%s b2=%s b=%s' % (a, b2, b))
        a = a + 1
        b2 = a*a - n
        b = isqrt(b2)
        count += 1
    p=a+b
    q=a-b
    assert n == p * q
    if verbose:
        print('a=',a)
        print('b=',b)
        print('p=',p)
        print('q=',q)
        print('pq=',p*q)
    return p, q
    
```

If this worked, we have p and q and RSA is broken. All that's left is to 
use p, q, n and e to find d.

To find D, we can use a modification on Eulers method. We need Phi(N) and E.

Since we know P and Q, Phi is easy to calculate. Phi(N) = (P-1)\*(Q-1)

E is already given to us in the public key. The extended\_gcd function is given:

``` python
def ext_gcd(a,b, verbose = True):
    s = 0
    old_s = 1
    t = 1
    old_t = 0
    r = b
    old_r = a
    while r!=0:
        quot = old_r/r
        old_r, r = r, old_r - (quot * r)
        old_s, s = s, old_s - (quot * s)
        old_t,t  = t, old_t - (quot * t)
    if verbose:
        print "Bez cof: " + str(old_s) + " " + str(old_t)
        print "gcd: " + str(old_r)
        print "quot: " + str(t) + " " + str(s)
    if old_t < 0: return old_t+a
    return old_t
```

This function will return D, which is the private exponent. Simply use the numbers
we know to turn it into a private key, and decrypt whatever the public key has encrypted!