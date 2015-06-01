from setuptools import setup

setup(
    name='CSE191 Language',
    version='0.0.1',
    author='James Kwan',
    author_email='jmkwan@ucsd.edu',
    packages=['cse191_lang'],
    #url='http://pypi.python.org/pypi/cse191',
    license='LICENSE.txt',
    description="Firewall rule management and automation tools",
    install_requires=[
        'bitarray',
        'ply==3.4',
        'pycrypto',
        'thriftpy',
    ],
)
