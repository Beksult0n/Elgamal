import sympy
import random
import time
import math

def get_prime(bits):
    bits = int(bits)
    p = sympy.randprime(2**(bits - 2), 2**(bits - 1))
    return p

def isprime(n):
    try:
        n = int(n)
        return sympy.isprime(n)
    except:
        return False

def check(p, g):
    try:
        p = int(p)
        g = int(g)
        return g < p
    except:
        return False


def get_all_primitive_roots(p, limit=1000):
    """p soni uchun limitta primitiv ildizni topish."""
    p = int(p)
    g = sympy.primitive_root(p)
    if g is None:
        return []

    phi = p - 1
    primitive_roots = set()

    for k in range(1, limit):
        if sympy.gcd(k, phi) == 1:
            root = pow(g, k, p)
            primitive_roots.add(root)

    return sorted(primitive_roots)

def is_primitive_root(g, p):
    g = int(g)
    p = int(p)
    return sympy.is_primitive_root(g, p)


def get_primitive_root_r(p):
    p = int(p)
    return sympy.primitive_root(p)



def get_random(p):
    p = int(p)
    return random.randint(p//2, p-1)

def gen_public(p, g, x):
    p = int(p)
    g = int(g)
    x = int(x)
    y = pow(g, x, p)
    return y

def el_enc(msg, p, g, y, b):
    p = int(p)
    g = int(g)
    y = int(y)
    b = int(b)

    msg_int = int.from_bytes(msg.encode(), 'big')

    c1 = pow(g, b, p)
    c2 = pow(y, b, p) * msg_int % p
    return c1, c2

def el_dec(p, c1, c2, x):
    p = int(p)
    c1 = int(c1)
    c2 = int(c2)
    x = int(x)

    s = pow(c1, x, p)
    s_inv = pow(s, p-2, p)
    dec_int = c2 * s_inv % p

    # Convert integer back to bytes then to string
    byte_length = (dec_int.bit_length() + 7) // 8
    dec_bytes = dec_int.to_bytes(byte_length, 'big')
    try:
        return dec_bytes.decode()
    except UnicodeDecodeError:
        return dec_bytes


def brute(p, g, y):
    p = int(p)
    g = int(g)
    y = int(y)
    start_time = time.time()
    m = math.isqrt(p - 1) + 1
    baby_steps = {}
    for j in range(m):
        val = pow(g, j, p)
        baby_steps[val] = j

    g_inv_m = pow(g, -m, p)
    gamma = y

    for i in range(m):
        if gamma in baby_steps:
            end_time = time.time()
            return i * m + baby_steps[gamma], end_time - start_time
        gamma = (gamma * g_inv_m) % p

    end_time = time.time()
    return None, end_time - start_time

def qayta_b(p, known_msg, c2_known, c2_target):
    p = int(p)
    c2_known = int(c2_known)
    c2_target = int(c2_target)

    m1 = int.from_bytes(known_msg.encode(), 'big')

    def modinv(a, p):
        return pow(a, p - 2, p)

    ratio = c2_target * modinv(c2_known, p) % p
    m2 = m1 * ratio % p

    byte_length = (m2.bit_length() + 7) // 8
    msg_bytes = m2.to_bytes(byte_length, 'big')
    try:
        return msg_bytes.decode('utf-8')
    except UnicodeDecodeError:
        return msg_bytes.hex()
