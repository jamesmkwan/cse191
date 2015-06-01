from setuptools import setup

setup(
    name='cse191_web',
    version='0.0.1',
    author='James Kwan',
    author_email='jmkwan@ucsd.edu',
    packages=[],
    #url='http://pypi.python.org/pypi/cse191',
    license='LICENSE.txt',
    description="Firewall rule management and automation tools",
    #long_description=open('README.txt').read(),
    install_requires=[
        'flask',
        'thriftpy',
    ],
)
