import elgamalUtils
import our_random
import random
import credentials
import time

from pbkdf2 import pbkdf2


def generateP(size=512):
    time1 = time.time()

    large_safe_prime = our_random.getSafePrime(size)

    time2 = time.time()

    time2 = time.time()

    diff = time2 - time1

    #print(large_safe_prime, "temps de recherche de p = ", diff, " secondes")

    return large_safe_prime


def generateG(p):

    g = our_random.getGenerator(p)
    return g


def generatePrivateKey():

    s = credentials.generate_credentials(22)
    salt = "salt"
    priv = pbkdf2(s, salt, 1000, 30)  
    key_size = len(priv)
    priv = int.from_bytes(priv, 'big')
    return priv


def generatePublicKey(priv, g, p):

    pub = elgamalUtils.exponentiation_rapide(g, priv, p)

    return pub


def generateSharedSecret(pub, priv, p):

    shared = elgamalUtils.exponentiation_rapide(pub, priv, p)

    return shared


def cipher(message, shared, p):

    ciphered = (shared * message) % p

    return ciphered


def decipher(ciphered, shared, p):

    plain = ciphered * elgamalUtils.calcul_inverse(shared, p) % p
    return plain

""" Exemple de chiffrement entre le sereur E et un votant

# E_server

p = generateP(512)
print("large_prime = ", p)

g = generateG(p)
print("generator = ", g)

priv = generatePrivateKey()
print("private_key = ", priv)

pub = generatePublicKey(priv, g, p)
print("public_key = ", pub)



# votant

m = 15121515412155454998987431321345487521354654512132132131315464684654545548498

y = random.randint(2, p-1)
print("y = ", y)

c1 = elgamalUtils.exponentiation_rapide(g, y, p)
print("c1 = ", c1)

s = elgamalUtils.exponentiation_rapide(pub, y, p)
print("s = ", s)

c2 = (s * m) % p
print("c2 = ", c2)


# E_server

s_E = elgamalUtils.exponentiation_rapide(c1, priv, p)
print("s_E = ", s_E)

m = ( c2 * elgamalUtils.calcul_inverse(s_E, p) ) % p
print("m = ", m)

"""