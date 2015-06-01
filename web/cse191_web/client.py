import functools
import sys
from thriftpy.rpc import make_client
from types import ModuleType

from .thrift import lang_thrift

class Wrapper(ModuleType):
    def __init__(self):
        for attr in ['__builtins__', '__doc__', '__name__', '__package__', '__file__']:
            setattr(self, attr, getattr(sys.modules[__name__], attr, None))

    def __getattr__(self, name):
        return functools.partial(rpc_call, name)

def rpc_call(call, server, *args):
    client = make_client(lang_thrift.CodeExecutor, *server)
    return getattr(client, call)(*args)

assert __name__ != '__main__'
sys.modules[__name__] = Wrapper()
