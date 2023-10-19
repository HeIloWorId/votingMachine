from collections import defaultdict
from pbkdf2 import pbkdf2
import time
from our_random import toInt, getRandom, getSafePrime, getGenerator, puissance_modulaire

base_58 = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"

"""
xorshift_seed = time.time_ns()

def xorshift():
  global xorshift_seed
  xorshift_seed ^= xorshift_seed << 15
  xorshift_seed ^= xorshift_seed >> 21
  xorshift_seed ^= xorshift_seed >> 4
  xorshift_seed %= int("ffffffff", 16) # modulo 2 puissance 32, 2 puissance 16 en réalité car le premier bit sert juste pour le signe
  return xorshift_seed """



def generate_credentials(size=14):
    credentials = []
    for i in range (0,size):
        random_number = toInt(getRandom(64)) % 58
        credentials.append(random_number)
    credentials = add_checksum(credentials)
    return(credential_toString(credentials))

def add_checksum(cred):
    checksum_bytes = bytes()
    for i in cred:
        checksum_bytes+=(i.to_bytes(1, 'big'))
    
    int_checksum = int.from_bytes(checksum_bytes, 'big')
    int_checksum = (53 - int_checksum) % 53

    cred.append(int_checksum)
    return cred

def credential_toString(credential):
    credential_string = ""
    for i in credential:
        credential_string+=base_58[i]

    return credential_string

def generate_parameters():
    parameters = []
    q = getSafePrime(512)
    g = getGenerator(q)
    parameters.append(q)
    parameters.append(g)
    return parameters


def generate_pub(credential, parameters):
    s_bytes = pbkdf2(credential, "salt", 1000, 30)
    s = int.from_bytes(s_bytes, 'big') 
    q = parameters[0]
    g = parameters[1]
    s = s % q
    pub = puissance_modulaire(g,s,q)
    return pub




