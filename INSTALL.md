[Local Setup](#local-setup)

[Server Setup](#server-setup)

Local Setup
===========
Local setup is intended for single user use for testing/debugging. For
simplicity, we assume that you run the language server on port 8001 and the
webserver on port 8000. Make sure these ports are free.

OS X: Install [Homebrew][homebrew] and run `brew install git python3`

1. Clone the repository:
    `git clone --recursive https://github.com/jamesmkwan/cse191 && cd cse191`
2. Create virtual environment:
    `pyvenv venv && source venv/bin/activate`
3. Setup and run language server:
    `cd lang && python3 setup.py install && python3 -m cse191_lang 8001`
4. Open new terminal and cd to cse191 directory
5. Enter virtual environment in second terminal:
    `source venv/bin/activate`
6. Setup and run web server:
    `cd web && python3 setup.py install && python3 runserver.py 127.0.0.1:8001`
7. Visit [http://127.0.0.1:8000/](http://127.0.0.1:8000/) on your browser

Server Setup
============
Easy setup
----------
Use the cse191 [Ansible][ansible] role in the [deploy](deploy) directory. It
has been tested on a Ubuntu 14.04 x64 machine on Digital Ocean.

Custom setup
------------
We recommend that you sandbox the interpreter instances with either
[Docker][docker] or virtual machines, so that you can limit resource usage.

1. Install the [cse191\_lang](lang) package with the setup.py inside the directory
2. Run instance(s) of the interpreter server on unique ports.
    For 8001: `python3 -m cse191_lang 8001`
3. Add each server as a line to (new) file in web/cse191\_web/server.
    Following the previous example, server would have a single line `127.0.0.1:8001`
4. Change into [web](web) directory and run `python3 setup.py install`
5. Use [uwsgi][uwsgi] to run the webserver instance (see sample [uwsgi.ini](web/uwsgi.ini))

[homebrew]: http://brew.sh/
[ansible]: http://docs.ansible.com/intro_installation.html#installation
[docker]: https://docs.docker.com/
[uwsgi]: https://uwsgi-docs.readthedocs.org/en/latest/
