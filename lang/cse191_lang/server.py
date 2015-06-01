from thriftpy.rpc import make_server
import traceback

from .thrift import lang_thrift
from . import interpreter

class Dispatcher:
    def run_code(self, code):
        try:
            _, out = interpreter.run_code(code)
            print("Got %r. Result: %r" % (code, out))
            return out
        except Exception:
            raise lang_thrift.RuntimeException(traceback.format_exc())

    def grade_code(self, code, grader):
        try:
            grade, debug = interpreter.grade_code(code, grader)
            print("Got %r, %r. Result: %r, %r" % (code, grader, grade, debug))
            return lang_thrift.GradeOutput(grade, debug)
        except Exception:
            raise lang_thrift.RuntimeException(traceback.format_exc())

def serve(port, server='0.0.0.0'):
    """
    Run as a thrift service (interpreter)

    Args:
        port (int): the port to listen on
        server (str): ip to bind to (default: 0.0.0.0)
    """
    server = make_server(lang_thrift.CodeExecutor, Dispatcher(), server, port)
    server.serve()
