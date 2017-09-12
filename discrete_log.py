#! /usr/bin/python

def factor(n, startFrom=2):
    """returns a list of prime factors of n,
    knowing min possible >= startFrom."""
    if n <= 1:  return [ ]
    d = startFrom
    factors = [ ]
    while n >= d*d:
      if n % d == 0:
        factors.append(d)
        n = n/d
      else:
        d += 1 + d % 2  # 2 -> 3, odd -> odd + 2
    factors.append(n)
    return factors

def gcd(a,b):
  """Returns the gcd of its inputs times the sign of b if b is nonzero,
  and times the sign of a if b is 0.
  """
  while b != 0:
      a,b = b, a % b
  return a


def xgcd(a,b):
    """Extended GCD:
    Returns (gcd, x, y) where gcd is the greatest common divisor of a and b
    with the sign of b if b is nonzero, and with the sign of a if b is 0.
    The numbers x,y are such that gcd = ax+by."""
    prevx, x = 1, 0;  prevy, y = 0, 1
    while b:
        q, r = divmod(a,b)
        x, prevx = prevx - q*x, x  
        y, prevy = prevy - q*y, y
        a, b = b, r
    return a, prevx, prevy

# EXPLANATION:
# Mathematical analysis reveals that at each stage in the calculation
# the current remainder can be expressed in the form ax + by for some
# integers x, y.  Moreover, the x-sequence and y-sequence are
# generated by the recursion (where q is the integer quotient of the
# current division):
#
#         new x = prev x - q * x;   new y = prev y - q * y
#
# and where the initial values are x = 0, prev x = 1, y = 1, prev y = 0.
# Moreover, upon termination the x and y sequences have gone one step
# too far, (as has the remainder), so return the previous x, y values. 

def mgcd(a,b):
    """Returns (gcd, x, y, s, t) where
    gcd is the greatest common divisor of a and b, with the sign of b 
    if b is nonzero, and with the sign of a if b is 0;
    the numbers x,y, s, t are such that
       gcd = xa+yb
         0 = sa+tb
    and abs(xt-ys) = 1
    Otherwise put: the determinant of matrix (hence m in name)
        x y
        s t
    has magnitude 1, and multiplied by column vector
           a
           b
    is column vector
           gcd
           0
    """
    prevx, x = 1, 0;  prevy, y = 0, 1
    while b:
        q, r = divmod(a, b)
        x, prevx = prevx - q*x, x  
        y, prevy = prevy - q*y, y
        a, b = b, r
    return a, prevx, prevy, x, y

##    Change from xgcd:
##    The coefficients for next iteration of xgcd that give 0 there,
##    and are excluded on purpose, are just included here as the last two
##    returned values, so only the end of the last line is differentfrom xgcd.



def ChineseRemainder(pairs):
    '''Return the solution to the Chinese Remainder Theorem, (x, M)
    Pairs contains tuples (a, m) with all m's positive and coprime.
    Return the smallest nonnegative integer x so 
    x mod m  = a mod m for each (a, m) in pairs.
    M is the product ofthe m's.

    >>> pairs = [(2, 3), (3, 4), (1, 5)]
    >>> x, M = ChineseRemainder(pairs)
    >>> (x, M)
    (11, 60)
    >>> for (a, m) in pairs:
    ...     print (a % m, x % m)
    2 2
    3 3
    1 1
    '''
    (a, m)=pairs[0]
    for (b,p) in pairs[1:]:
        k=((b-a)*xgcd(m,p)[1]) % p #moduli coprime so inverse exists for m mod p
        a=(a+m*k) % (m*p)# joining a mod m and b mod p gives a mod(mp)
        m *= p # mod mp
    return (a,m)

def countConsecutiveSame(seq):
    '''Given a sequence, return a list of (item, consecutive_repetitions).'''
    if not seq: return []
    current = NotImplemented
    n = 0
    pairs = []
    for e in seq:
        if e == current:
            n += 1
        else:
            if n > 0:
                pairs.append((current, n))
            n = 1
            current = e
    pairs.append((current, n))
    return pairs

def factorMultiplicity(n):
    return countConsecutiveSame(factor(n))

	
def PohligHellmanModP(beta, alpha, p, verbose=True):
    ''' Solves discrete log problem alpha^x = beta mod p, and returns x,
     using Pohlig-Hellman reduction to prime factors of p-1. 
    '''
    congruenceList=[getXModP(beta, alpha, p, q, r)
                    for (q, r) in factorMultiplicity(p-1)]
    (x,m)=ChineseRemainder(congruenceList)
    if verbose: print ("Given", beta,"=", alpha,"^x mod",p, "\n","x=", x)
    assert pow(int(alpha), int(x), int(p)) == beta % p
    return x

def discreteLogModP(a, b, p):  # brute force version
    '''Returns x so pow(a, x, p) is b mod p, or None if no solution.'''
    a_x = 1
    b %= p
    for x in range(p-1):
        if a_x == b: return x
        a_x = a_x * a % p
    return None

def getXModP(beta, alpha, p, q, r):
    ''' return (x, q**r) with (p-1)/q**r = k, 0 <= x < q**r, os
    beta^(x*k) = alpha^k mod p
    '''
    oDiv = (p-1)/q # first divided group order
    bCurrent=beta
    xFinal=0  # returns x=x0+x1q+x2q^2+...+xiq^i with 0<=xi<q-1
    alphaRaisedModp=pow(alpha, oDiv, p)
    qPow = 1
    alphaInv = xgcd(alpha, p)[1]
    for i in range(0,r):
        betaRaisedModp=pow(bCurrent, oDiv, p)
        xCurrent = discreteLogModP(alphaRaisedModp, betaRaisedModp, p)
        xFinal += xCurrent*qPow
        #now we calculate the next beta, power of q, order factor
        bCurrent = bCurrent*pow(alphaInv, xCurrent*qPow, p) % p
        qPow *= q
        oDiv /= q
    return (xFinal,qPow)

def PohligHellman(beta, alpha, order, verbose=True):
    ''' Solves discrete log problem alpha^x = beta in group of given order,
     and returns x, using Pohlig-Hellman reduction to prime factors of order. 
    '''
    print ('PohligHellman for group elements not written')

def discreteLog(a, b, bound):  # brute force version for group elements a, b
    '''Returns x so a**x = b for x < bound, or None if no solution.'''
    a_x = 1
    for x in range(bound):
        if a_x == b: return x
        a_x *= a
    return None

def getX(beta, alpha, order, q, r):
    ''' return (x, q**r) with order/q**r = k, 0 <= x < q**r, so
    beta**(x*k) = alpha**k, alpha and beta in group of given order.
    '''
    print ('getX for group elements not written')

def testGenModP(a, p):  # want generator base for discrete log (and Pohlig-Hellman)
    '''True if a generates Fp* for prime p.'''
    b = a
    for i in range(1, p-1):
        if b == 1:
            return False
        b = b*a % p
    assert b == 1
    return True

if __name__ == '__main__':
    p = 7863166752583943287208453249445887802885958578827520225154826621191353388988908983484279021978114049838254701703424499688950361788140197906625796305008451719
    y = 6289736695712027841545587266292164172813699099085672937550442102159309081155467550411414088175729823598108452032137447608687929628597035278365152781494883808
    g = 2862392356922936880157505726961027620297475166595443090826668842052108260396755078180089295033677131286733784955854335672518017968622162153227778875458650593
PohligHellmanModP(y, g, p)
##    PohligHellmanModP(95, 37, 2017)
##    PohligHellmanModP(19, 95, 3001)
##    PohligHellmanModP(7531, 6, 8101)