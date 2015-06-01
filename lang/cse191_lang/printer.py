from bitarray import bitarray

from . import constructs

def formatter(out):
    def p(*xs):
        s = []
        for x in xs:
            if isinstance(x, constructs.Str):
                s.append(x.str)
            elif isinstance(x, bitarray):
                n = x.length() % 8
                if n:
                    s.append(str(x))
                else:
                    s.append('0x%s' % ''.join('%02x' % a for a in x.tobytes()))
            else:
                s.append(str(x))
        out(''.join(s))
    return p
