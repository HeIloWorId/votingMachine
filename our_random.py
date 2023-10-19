import os
import random


first_primes_list = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, # prise sur le net et permet d'éviter de faire du rabin miller pour rien
                     31, 37, 41, 43, 47, 53, 59, 61, 67,
                     71, 73, 79, 83, 89, 97, 101, 103,
                     107, 109, 113, 127, 131, 137, 139,
                     149, 151, 157, 163, 167, 173, 179,
                     181, 191, 193, 197, 199, 211, 223,
                     227, 229, 233, 239, 241, 251, 257,
                     263, 269, 271, 277, 281, 283, 293,
                     307, 311, 313, 317, 331, 337, 347, 349]



p = 30000000091 
q = 40000000003 

M = p*q

seed = int.from_bytes(os.urandom(4), 'big')


def getParity(x):
    if x % 2 == 0:
      return 0
    else:
      return 1  

def toInt(bits):
  poids = 2**(len(bits)-1)
  res = 0
  for bit in bits:
    res+=(bit*poids)
    poids//=2
  return res

    
def BlumBlumShub(desired_bits_number):
    global seed
    #seed = int.from_bytes(os.urandom(4), 'big')
    random_sequence = []
    for i in range(desired_bits_number):
        seed = (seed**2) % M
        random_sequence.append(getParity(seed))
    
    return random_sequence

def getRandom(size):
  random = BlumBlumShub(size)
  if len(random) == size :
    return random
  while len(random) < size:
    random.insert(0)


def getPrimeCandidate(size):
  candidate = getRandom(size-2)
  candidate.append(1)
  candidate.insert(0, 1)
  return toInt(candidate)


def miller_rabin(n, k=7):

    if n == 2:
        return True

    if n % 2 == 0:
        return False

    r, s = 0, n - 1
    while s % 2 == 0:
        r += 1
        s //= 2
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, s, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def isDivisibleByFirstPrimes(x):
  for prime in first_primes_list:
    if(x % prime == 0):
      return True
  return False

def getPrime(size):
  candidate = getPrimeCandidate(size)
  while miller_rabin(candidate) != True:
    candidate = getPrimeCandidate(size)
    if (isDivisibleByFirstPrimes(candidate) == True):
      candidate = getPrimeCandidate(size)
  return candidate

def getSafePrime(size):
  q = getPrime(size-1)
  while(miller_rabin(2*q + 1) != True):
    q = getPrime(size-1)
  

  return (2*q + 1)

def puissance_modulaire(x, y, n):
    """puissance modulaire: (x**y)%n avec x, y et n entiers"""
    result = 1
    while y>0:
        if y&1>0:
            result = (result*x)%n
        y >>= 1
        x = (x*x)%n    
    return result

def getGenerator(safePrime):
    p = safePrime
  
    q = (p-1) // 2
 
    #g = random.randint(1, p-1)
    g=2
    while( puissance_modulaire(g, 2, p) == 1 or puissance_modulaire(g, q, p) == 1 ):
      #g = random.randint(1, p-1)
      g+=1
      
    return g

  








