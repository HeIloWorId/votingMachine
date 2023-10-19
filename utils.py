def toHex(bytes):
    return hex(int.from_bytes(bytes, 'big') )

def toBinary(a, size):
    binary = [int(x) for x in list('{0:0b}'.format(a))]
    while len(binary) < size:
        binary.insert(0,0)
    return binary

def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def leftrotate(x, c):
    """ Left rotate the number x by c bytes."""
    x &= 0xffffffff
    return ((x << c) | (x >> (32 - c))) & 0xffffffff


def ascii_toBinaryList(message):
    binary_list = []    
    for char in message:
        binary_list+=(toBinary(ord(char),8))
    return binary_list

def bytes_toBinaryList(bytes):
    bytes_as_bits = ''.join(format(byte, '08b') for byte in bytes)
    list = [] 
    for bit in bytes_as_bits:
            list.append(int(bit))
    return list

def padding(bits): # on ajoute '1' puis des '0' jusquà obtenir une longueur congru à 448 mod 512
    bits.append(1)
    while ((len(bits) % 512) != 448):
        bits.append(0)
    return bits

def messageLength64Bits(length):
    message_length_bits = toBinary(length & 0xffffffffffffffff, 64)
    return message_length_bits

def chunker(bits, chunk_length=32): # pas codé par moi
    # divides list of bits into desired byte/word chunks, 
    # starting at LSB 
    chunked = []
    for b in range(0, len(bits), chunk_length):
        chunked.append(bits[b:b+chunk_length])
    return chunked

def chunks(bits):
    M = [bits[i:i + 512] for i in range(0, len(bits), 512)]
    length = len(M)
    for n in range(length):
        M[n] = chunker(M[n]) 
    return M

def binatodeci(binary): # pas codé par moi
    return sum(val*(2**idx) for idx, val in enumerate(reversed(binary)))

def chunks32_toInt(bits):
    numberOf512Chunks = len(bits)
    for i in range(numberOf512Chunks):
        for j in range(16):
            bits[i][j] = binatodeci(bits[i][j])
    return bits

def extendChunkTo80(chunk):
    chunk+=([0]*64)
    return chunk