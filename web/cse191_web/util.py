import traceback
from . import client
from . import app
from .thrift import lang_thrift
import os.path
import random

servers = []
with open(os.path.join(os.path.dirname(__file__), 'servers'), 'r') as f:
    for l in f:
        ip, _, port = l.partition(':')
        servers.append((ip, int(port)))

def get_server():
    assert servers, "No servers specified"
    return random.choice(servers)

def run_code(code, func=None, *args):
    try:
        env, out = client.run_code(get_server(), code + '\n')
        if func:
            assert func in env, ('No %s defined' % func)
            return env[func](*args), out
        else:
            return None, out
    except lang_thrift.RuntimeException as x:
        return None, "Error: %s" % x.msg
    except Exception:
        return None, "Error: %s" % traceback.format_exc()

def grade_code(code, grade, *args):
    try:
        output = client.grade_code(get_server(), code + '\n', grade + '\n')
        return output.grade, output.debug
    except lang_thrift.RuntimeException as x:
        return None, "Error: %s" % x.msg
    except Exception:
        return None, "Error: %s" % traceback.format_exc()
