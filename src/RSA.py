import gmpy2 as g
import base64
import math
from pyasn1.codec.der import encoder, decoder
from pyasn1.type import univ
from random import randrange, randint, getrandbits
from abc import ABC, abstractmethod, abstractstaticmethod


class Key(ABC):
    def __init__(self, x, n):
        self.x = x
        self.n = n
        self.chunk_size = math.ceil(self.n.bit_length() / 8 - 1)
        self.pkcs1_seq = univ.Sequence()
        self.pkcs1_seq.setComponentByPosition(0, univ.Integer(self.x))
        self.pkcs1_seq.setComponentByPosition(1, univ.Integer(self.n))

    def encode(self):
        return base64.encodestring(encoder.encode(self.pkcs1_seq))

    @abstractmethod
    def export_to(self, dir):
        pass

    @abstractstaticmethod
    def import_from(self, fn):
        pass


class PrivateKey(Key):
    def export_to(self, dir):
        fn = dir + 'private_key.der'
        with open(fn, 'wb+') as file:
            file.write(self.encode())
        return fn

    @staticmethod
    def import_from(fn):
        with open(fn, 'rb') as file:
            params = decoder.decode(base64.decodestring(file.read()))
        return PrivateKey(params[0][0]._value, params[0][1]._value)

    def decrypt_file(self, fn):
        content_blocks = []
        with open(fn,  'r') as file:
            cipher_blocks = file.read().split('\n')
            for cipher in cipher_blocks:
                text_block = "{:0x}".format(g.powmod(int(cipher), self.x, self.n))
                if len(text_block) % 2 != 0:  # padding
                    text_block = '0' + text_block

                text_block = ''.join([chr(int(text_block[i:i+2], 16))
                                      for i in range(0, len(text_block), 2)])
                content_blocks.append(text_block)

        with open(fn,  'w') as file:
            content = ''.join(content_blocks)
            file.write(content)


class PublicKey(Key):
    def export_to(self, dir):
        fn = dir + 'public_key.der'
        with open(fn, 'wb+') as file:
            file.write(self.encode())
        return fn

    @staticmethod
    def import_from(fn):
        with open(fn, 'rb') as file:
            params = decoder.decode(base64.decodestring(file.read()))
        return PublicKey(params[0][0]._value, params[0][1]._value)

    def encrypt_file(self, fn, encoding="ascii"):
        cipher_blocks = []
        with open(fn,  'r') as file:
            chunk = file.read(self.chunk_size)
            while chunk:
                chunk_encoded = "".join("{:02x}".format(c)
                                        for c in chunk.encode(encoding))
                cipher = g.powmod(int(chunk_encoded, 16), self.x, self.n)
                cipher_blocks.append(str(cipher))
                chunk = file.read(self.chunk_size)

        with open(fn,  'w') as file:
            content = '\n'.join(cipher_blocks)
            file.write(content)

# Generate RSA Keys


def generate_keys(key_size, n_tests=30):
    assert(key_size >= 16)
    p = get_prime(key_size//2, n_tests)
    q = get_prime(key_size//2, n_tests)
    n = p*q
    phi = (p - 1)*(q - 1)
    e = get_small_rel_prime(phi)
    d = get_inv_mul(e, phi)
    return PublicKey(e, n), PrivateKey(d, n)

# Get a prime number of n bits.
def get_prime(n_bits, n_tests):
    x = get_randbitsodd(n_bits)
    while not is_prime(x, n_tests):
        x = get_randbitsodd(n_bits)
    return x

# Miller-Rabin algorithm for primality test
# Ref: https://www.youtube.com/watch?v=x1WrtPHNPiY
# Ref: http://www.cmi.ac.in/~shreejit/primality.pdf
def is_prime(number, n_tests):
    def find_t_u(n):
        u, t = n - 1, 0
        while u % 2 == 0:
            t += 1
            u //= 2
        return t, u

    def witness(a, u, t, n):
        x = g.powmod(a, u, n)
        if x == 1:
            return False
        for i in range(t):
            if g.powmod(a, 2**i*u, n) == (n-1):
                return False
        return True

    assert(number != 2)  # 2 is Prime but it's not recommended to use
    assert(number % 2 != 0)  # Cannot be even

    t, u = find_t_u(number)
    for _ in range(n_tests):
        a = randint(2, number-1)
        if witness(a, u, t, number):
            return False
    return True


# Get a small relative prime of phi.
def get_small_rel_prime(phi):
    for e in range(3, phi, 2):
        a, _, _ = xgcd(e, phi)
        if a == 1:
            return e
    raise Exception("Could not find e parameter")


# Get modular multiplicative inverse
def get_inv_mul(e, n):
    gcd, x, _ = xgcd(e, n)
    if gcd != 1:
        raise Exception('Modular inverse does not exist')

    return x % n


# Extended Euclidean Algorithm
# Ref: https://anh.cs.luc.edu/331/notes/xgcd.pdf
def xgcd(a, b):
    x0, x1 = 1, 0
    y0, y1 = 0, 1
    while b:
        q = a // b
        x1, x0 = x0 - q*x1, x1
        y1, y0 = y0 - q*y1, y1
        a, b = b, a % b

    return a, x0, y0


# Get a random odd number of n bits.
def get_randbitsodd(n_bits):
    return randrange(pow(2, n_bits-1)+1, pow(2, n_bits), 2)
