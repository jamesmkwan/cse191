import sys
from . import server

usage = "Usage: %s <binding>" % sys.argv[0]

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(usage)
        sys.exit(1)
    server.serve(sys.argv[1])
