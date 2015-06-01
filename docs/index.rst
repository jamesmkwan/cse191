.. cse191 documentation master file, created by
   sphinx-quickstart on Sat May 30 11:18:36 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

CSE191
======
.. toctree::
   :maxdepth: 2

operators
---------
.. function:: x == y

   :return: True if x is equal to y, False otherwise
   :rtype: bool

.. function:: x < y

   :param int x: first number
   :param int y: second number
   :return: True if x is less than y, False otherwise
   :rtype: bool

.. function:: x <= y

   :param int x: first number
   :param int y: second number
   :return: True if x is less than or equal to y, False otherwise
   :rtype: bool

.. function:: x > y

   :param int x: first number
   :param int y: second number
   :return: True if x is greater than y, False otherwise
   :rtype: bool

.. function:: x >= y

   :param int x: first number
   :param int y: second number
   :return: True if x is greater than or equal to y, False otherwise
   :rtype: bool

.. function:: x + y

   :param int x: first number
   :param int y: second number
   :return: x plus y
   :rtype: int

.. function:: x - y

   :param int x: first number
   :param int y: second number
   :return: x minus y
   :rtype: int

.. function:: x % y

   :param int x: first number
   :param int y: second number
   :return: x mod y
   :rtype: int

.. function:: x || y

   :param bitarray x: first string
   :param bitarray y: second string
   :return: the concatenation of x and y
   :rtype: bitarray

.. function:: x ^ y

   :param bitarray x: first string
   :param bitarray y: second string of the same length
   :return: the XOR of each bit in x and y
   :rtype: bitarray

.. function:: s[x:y]

   :param bitarray s: string
   :param bitarray x: start point (inclusive)
   :param bitarray y: end point (exclusive)
   :return: a substring of s
   :rtype: bitarray

.. function:: s[i]

   :param array s: an array created by the array() function call
   :param int i: index of element desired (counting from 0)
   :return: the element at position i of array s

builtins
---------------------------

.. automodule:: cse191_lang.builtins
    :members:
    :show-inheritance:

grader tools
-------------------------------

.. automodule:: cse191_lang.grader_tools
    :members:
    :show-inheritance:

interpreter
------------------------------

.. automodule:: cse191_lang.interpreter
    :members:
    :show-inheritance:

thrift API
-------------------------

.. automodule:: cse191_lang.server
    :members:
    :show-inheritance:
