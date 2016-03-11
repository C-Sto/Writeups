def isqrt(n):
    x = n
    y = (x + 1) // 2
    while y < x:
        x = y
        y = (x + n // x) // 2
    return x

def fermat(n, verbose=True):
    a = isqrt(n)
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
