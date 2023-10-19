import random
import math


def pgcd(a, b):  # Calcul du pgcd avec l'algorithme d'Euclide
    r0 = a
    r1 = b
    while (r1 != 0):
        r = r0 % r1
        if r == 0:
            return r1
        r0 = r1
        r1 = r


def exponentiation_rapide(a, e, m):

    resultat = 1
    pui = a
    puissances_succ = []

    binary = [int(x) for x in bin(e)[2:]]
    binary = binary[::-1]

    for j in range(len(binary)):

        if(binary[j] == 1):
            resultat *= pui

        pui = pui**2 % m

    resultat = resultat % m

    return resultat


def prime_factors(n):
    i = 2
    factors = []
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            factors.append(i)
    if n > 1:
        factors.append(n)
    return factors


def temoin_miller(n, a, d, s):

    x = exponentiation_rapide(a, d, n)

    if (x == 1 or x == (n-1)):

        return False

    for r in range(s-1):

        x = x**2 % n
        if x == n-1:
            return False

    return True


def rabin_miller(n, k=7):

    if n in [2, 3, 5, 7, 11, 13]:
        return True

    if n % 2 == 0 or n < 2:
        return False

    s = 1
    d = (n-1)

    while d % 2 == 0:
        s += 1
        d //= 2

    for _ in range(k):

        a = random.randint(2, n-1)
        if (temoin_miller(n, a, d, s)):

            return False

    return True


def indicatrice_euler(m):

    if (rabin_miller(m) == True):
        return m-1

    diviseurs_premiers = []

    i = 2

    while rabin_miller(m) == False:
        print(m)
        while (i < (math.floor(math.sqrt(m))+1)):
            if (m % i == 0 and rabin_miller(i) == True):
                diviseurs_premiers.append(i)
            i += 1

        m //= i

    return diviseurs_premiers


"""def calcul_inverse(a, m):

    if(pgcd(a, m) != 1):

        phi = 1

    if(rabin_miller(m) == True):
        phi = m-1

    else:
        factors = prime_factors(m)
        print("flag")
        for p in factors:
            phi *= (p-1)

    inverse = exponentiation_rapide(a, phi-1, m)
    return inverse"""

def calcul_inverse(a, m):
    
    s = 0; old_s = 1
    t = 1; old_t = 0
    r = m; old_r = a

    while r != 0:
      quotient = old_r//r 
      old_r, r = r, old_r - quotient*r
      old_s, s = s, old_s - quotient*s
      old_t, t = t, old_t - quotient*t

    return old_s % m
