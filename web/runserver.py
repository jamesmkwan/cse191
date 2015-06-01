from cse191_web import app
from cse191_web.util import servers
import itertools
import sys

for a in itertools.islice(sys.argv, 1, None):
    ip, _, port = a.partition(':')
    servers.append((ip, int(port)))

app.run(debug=True, port=8000)
