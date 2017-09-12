#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import base64
import binascii
import gmpy2
from gmpy2 import mpz

### key1_pub.pem ###

#Public-Key: (1024 bit)
#Modulus:
#    00:ad:6d:d4:00:cd:d6:8e:ec:61:d7:c5:4b:15:67:
#    e1:66:71:d7:40:1e:bb:a0:ab:e6:b3:91:57:5f:82:
#    71:ee:ea:d7:8a:de:10:d0:96:4d:01:74:dc:fd:2e:
#    54:13:dc:1a:07:5e:0e:7f:83:d1:43:bf:76:c1:c1:
#    ab:a5:a5:01:10:3e:51:8c:51:71:14:9d:00:09:eb:
#    d2:92:55:a2:f1:1d:be:56:99:bd:2f:a9:7f:ea:c9:
#    22:9c:f0:7b:1e:aa:de:70:6d:79:25:3a:b9:d9:78:
#    72:77:1e:6d:e6:51:e2:29:96:95:8f:7f:5f:42:ea:
#    0a:0d:dd:b5:06:ae:b9:e2:c3
#Exponent: 65537 (0x10001)
#Modulus=AD6DD400CDD68EEC61D7C54B1567E16671D7401EBBA0ABE6B391575F8271EEEAD78ADE10D0964D0174DCFD2E5413DC1A075E0E7F83D143BF76C1C1ABA5A501103E518C5171149D0009EBD29255A2F11DBE5699BD2FA97FEAC9229CF07B1EAADE706D79253AB9D97872771E6DE651E22996958F7F5F42EA0A0DDDB506AEB9E2C3
#writing RSA key
#-----BEGIN PUBLIC KEY-----
#MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCtbdQAzdaO7GHXxUsVZ+FmcddA
#Hrugq+azkVdfgnHu6teK3hDQlk0BdNz9LlQT3BoHXg5/g9FDv3bBwaulpQEQPlGM
#UXEUnQAJ69KSVaLxHb5Wmb0vqX/qySKc8Hseqt5wbXklOrnZeHJ3Hm3mUeIplpWP
#f19C6goN3bUGrrniwwIDAQAB
#-----END PUBLIC KEY-----


### key2_pub.pem ###

#Public-Key: (1024 bit)
#Modulus:
#    00:ad:6d:d4:00:cd:d6:8e:ec:61:d7:c5:4b:15:67:
#    e1:66:71:d7:40:1e:bb:a0:ab:e6:b3:91:57:5f:82:
#    71:ee:ea:d7:8a:de:10:d0:96:4d:01:74:dc:fd:2e:
#    54:13:dc:1a:07:5e:0e:7f:83:d1:43:bf:76:c1:c1:
#    ab:a5:a5:01:10:3e:51:8c:51:71:14:9d:00:09:eb:
#    d2:92:55:a2:f1:1d:be:56:99:bd:2f:a9:7f:ea:c9:
#    22:9c:f0:7b:1e:aa:de:70:6d:79:25:3a:b9:d9:78:
#    72:77:1e:6d:e6:51:e2:29:96:95:8f:7f:5f:42:ea:
#    0a:0d:dd:b5:06:ae:b9:e2:c3
#Exponent: 343223 (0x53cb7)
#Modulus=AD6DD400CDD68EEC61D7C54B1567E16671D7401EBBA0ABE6B391575F8271EEEAD78ADE10D0964D0174DCFD2E5413DC1A075E0E7F83D143BF76C1C1ABA5A501103E518C5171149D0009EBD29255A2F11DBE5699BD2FA97FEAC9229CF07B1EAADE706D79253AB9D97872771E6DE651E22996958F7F5F42EA0A0DDDB506AEB9E2C3
#writing RSA key
#-----BEGIN PUBLIC KEY-----
#MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCtbdQAzdaO7GHXxUsVZ+FmcddA
#Hrugq+azkVdfgnHu6teK3hDQlk0BdNz9LlQT3BoHXg5/g9FDv3bBwaulpQEQPlGM
#UXEUnQAJ69KSVaLxHb5Wmb0vqX/qySKc8Hseqt5wbXklOrnZeHJ3Hm3mUeIplpWP
#f19C6goN3bUGrrniwwIDBTy3
#-----END PUBLIC KEY-----

######## FUNCTIONS ###############
def gcd(a,b):
    """gcd(a,b): calculate gdc between 2 integers a and b"""
    if b==0:
        return a
    else:
        r=a%b
        return gcd(b,r)

def extended_euclide(u,v):
  """ Find the couple (x,y) such as u*x + v*y = 1 (u > v) and return the couple (a,b)"""
  # Initialization
  x = 0
  y = 0

  # Divided/Divisor
  a = u
  b = v

  # Multiple/Remainder
  m = a/b
  r = a%b
  print a," = ", m,"*", b, "+", r

  # First iteration
  x = 1
  y = -m
  print "So 343223 * (", x, ") + 65537 * (", y, ") = ", r

  # Second iteration
  a = b
  b = r
  m = a/b
  r = a%b
  print "However, ", a," = ", m,"*", b, "+", r

  x_old = x
  y_old = y

  x = -x*m 
  y = 1 - y*m
  print "So 343223 * (", x, ") + 65537 * (", y, ") = ", r

  # Change !
  a = b
  b = r
  m = a/b
  r = a%b

  # We can continue in a loop
  while (r != 0):
    print "However, ", a," = ", m,"*", b, "+", r
    # Save before change
    x_old_backup = x
    y_old_backup = y
    # Calculate
    x = x_old - m*x
    y = y_old - m*y
    # Store backup
    x_old = x_old_backup
    y_old = y_old_backup
    print "So 343223 * (", x, ") + 65537 * (", y, ") = ", r
    # Changement
    a = b
    b = r
    m = a/b
    r = a%b

  return (x,y)

   
######## MAIN ##################

# Get back public key 1 and 2 with the modulus

N = int('AD6DD400CDD68EEC61D7C54B1567E16671D7401EBBA0ABE6B391575F8271EEEAD78ADE10D0964D0174DCFD2E5413DC1A075E0E7F83D143BF76C1C1ABA5A501103E518C5171149D0009EBD29255A2F11DBE5699BD2FA97FEAC9229CF07B1EAADE706D79253AB9D97872771E6DE651E22996958F7F5F42EA0A0DDDB506AEB9E2C3',16) 
e1 = 343223
e2 = 65537 

print "Modulus: ", N
print "e1: ", e1, " and e2: ", e2

print "gcd(e1,e2): ", gcd(e1,e2)
if (gcd(e1,e2) == 1):
  # gcd(e1,e2) = 1 so thanks to the Bezout's theorem, there is a couple (x,y) such as: x*e1 + y*e2 = 1
  # However, C1 = M^e1 and C2 = M^e2
  # So C1^x*C2^y = M^(e1*x)*M(e2*y) = M^(e1*x+e2*y)= M
  # Let's find out (x,y) such as 65537*x + 343223*y = 1
  (x,y) = extended_euclide(e1,e2)
  print "Solution: x = ", x, " et y = ", y
else:
  x = -1
  y = -1


# Get cipher messages (read => decode_base64 => hexlify => int(base 16))
f1 = open("message1","r")
c1 = int(binascii.hexlify(base64.b64decode(f1.read())),16)
f1.close()
f2 = open("message2","r")
c2 = int(binascii.hexlify(base64.b64decode(f2.read())),16)
f2.close()

# Inverse modular
if y < 0:
    _, c1, __ = gmpy2.gcdext(c1, N)
elif x < 0:
    _, c2, __ = gmpy2.gcdext(c2, N)

# Calculate power and result of our formula
p1 = pow(c1,abs(y),N)
p2 = pow(c2,abs(x),N)
M = (p1 * p2) % N
print ("%x" % M).decode('hex')
