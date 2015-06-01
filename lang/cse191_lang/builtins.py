from Crypto.Cipher import AES
from Crypto.Random import random
from Crypto.Hash import SHA
from bitarray import bitarray
import itertools
from . import constructs
from . import printer

builtins = {}

def builtin(f):
    builtins[f.__name__] = f
    return f

def op(f):
    builtins['$' + f.__name__] = f

@op
def eq(x, y):
    """Compare two variables with =="""
    return x == y

@op
def lt(x, y):
    assert isinstance(x, int)
    assert isinstance(y, int)
    return x < y

@op
def gt(x, y):
    assert isinstance(x, int)
    assert isinstance(y, int)
    return x > y

@op
def lte(x, y):
    assert isinstance(x, int)
    assert isinstance(y, int)
    return x <= y

@op
def gte(x, y):
    assert isinstance(x, int)
    assert isinstance(y, int)
    return x >= y

@op
def add(x, y):
    assert isinstance(x, int)
    assert isinstance(y, int)
    return x + y

@op
def sub(x, y):
    assert isinstance(x, int)
    assert isinstance(y, int)
    return x - y

@op
def mul(x, y):
    assert isinstance(x, int)
    assert isinstance(y, int)
    return x * y

@op
def mod(x, y):
    assert isinstance(x, int)
    assert isinstance(y, int)
    return x % y

@op
def cat(x, y):
    assert isinstance(x, bitarray)
    assert isinstance(y, bitarray)
    return x + y

@op
def xor(x, y):
    assert isinstance(x, bitarray)
    assert isinstance(y, bitarray)
    assert x.length() == y.length()
    return x ^ y

@op
def substr(s, x, y):
    assert isinstance(s, bitarray)
    assert isinstance(x, int)
    assert isinstance(y, int)
    return s[x:y]

@op
def index(s, x):
    assert isinstance(s, list)
    assert isinstance(x, int)
    return s[x]

@builtin
def ones(x):
    """Create a string of x ones

    Args:
        x (int): number of ones

    Returns:
        bitarray: x ones
    """
    assert isinstance(x, int)
    return bitarray('1') * x

@builtin
def zeros(x):
    """Create a string of x zeros

    Args:
        x (int): number of zeros

    Returns:
        bitarray: x zeros
    """
    assert isinstance(x, int)
    return bitarray('0') * x

@builtin
def to_number(x):
    """Convert a bitarray to an int

    Args:
        x (bitarray): binary number

    Returns:
        int: integer number
    """
    assert isinstance(x, bitarray)
    return int(x.to01(), 2)

@builtin
def to_bits(x, y):
    """Convert an int to a bitarray

    Args:
        x (int): integer number
        y (int): number of bits

    Returns:
        bitarray: the number as binary
    """
    assert isinstance(x, int)
    assert x >= 0
    a = [True if x == '1' else False for x in bin(x)[2:]]
    assert len(a) <= y
    return bitarray(itertools.chain([False for _ in range(y - len(a))], a))

@builtin
def aes_128(key, msg):
    """AES encrypt a 128 bit message with a 128 bit key

    Args:
        key (bitarray): 128-bit key to use
        msg (bitarray): 128-bit message to use

    Returns:
        bitarray: cipher
    """
    assert isinstance(key, bitarray)
    assert isinstance(msg, bitarray)
    assert key.length() == 128
    assert msg.length() == 128
    cipher = AES.new(key.tobytes(), AES.MODE_ECB)
    r = bitarray()
    r.frombytes(cipher.encrypt(msg.tobytes()))
    return r

@builtin
def aes_128_inverse(key, msg):
    """AES decrypt a 128 bit cipher with a 128 bit key

    Args:
        key (bitarray): 128-bit key to use
        cipher (bitarray): 128-bit cipher to use

    Returns:
        bitarray: message
    """
    assert isinstance(key, bitarray)
    assert isinstance(msg, bitarray)
    assert key.length() == 128
    assert msg.length() == 128
    cipher = AES.new(key.tobytes(), AES.MODE_ECB)
    r = bitarray()
    r.frombytes(cipher.decrypt(msg.tobytes()))
    return r

@builtin
def randnum(x, y):
    """
    Generate a random int between x (inclusive) and y (exclusive)

    Args:
        x (int): inclusive lower bound
        y (int): exclusive upper bound

    Returns:
        int: random number
    """
    assert isinstance(x, int)
    assert isinstance(y, int)
    assert y - x < 2147483648, "Range too large" # 2 ** 31
    return random.randrange(x, y)

@builtin
def randbits(x):
    """
    Generate a random bitarray of length x

    Args:
        x (int): length of the bitarray

    Returns:
        bitarray: random bitarray of length x
    """
    assert isinstance(x, int)
    assert x < 4096, "Too many bits requested"
    return to_bits(random.getrandbits(x), x)

@builtin
def sha1(x):
    """
    Calculate the SHA1 hash of a bitarray

    Args:
        x (bitarray): bitarray to hash

    Returns:
        bitarray: SHA1 digest
    """
    assert isinstance(x, bitarray)
    h = SHA.new()
    h.update(x.tobytes())
    r = bitarray()
    r.frombytes(h.digest())
    return r

@builtin
def array(x):
    """
    Construct an array of size x (not a bitarray)

    Args:
        x (int): size of the array

    Returns:
        array: array of size x
    """
    assert isinstance(x, int)
    assert x < 4096, "Array too large"
    return [None] * x

@builtin
def failfast(x):
    """
    Immediately end execution of program

    Args:
        x (str): message to display
    """
    assert isinstance(x, constructs.Str)
    assert False, x.str

@builtin
def sprint(*x):
    """
    Combine multiple values into a single string (note: NOT sprintf)
    """
    r = None
    def out(a):
        nonlocal r
        r = a
    printer.formatter(out)(*x)
    return r

builtin(len)
