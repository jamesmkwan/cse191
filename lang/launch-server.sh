#!/bin/sh
python3 setup.py install
exec python3 -m cse191_lang 8000
