CSE191 Crypto
=============

This project provides a language for testing adversaries in the context of
UCSD's CSE 107 course.

See [setup instructions](INSTALL.md) to get started.

Interpreter (lang)
------------------
The interpreter is written in Python and uses PLY to lex and parse the
language. The current implementation runs multiple interpreters in Docker
containers. By using Docker, we can implement memory constraints and limit
damage to the server in case of a vulnerability. As each code run is
stateless, interpreter instances can run on different machines and round
robinned. The interpreter server runs a thrift service, currently implemented
with ThriftPy since Apache Thrift's Python bindings do not support Python 3.

Front End (web)
---------------
The front end is currently a rudimentary interface for a thrift client. Thanks
to the language's similarity to JavaScript, the code editor uses CodeMirror's
JavaScript syntax support for easy editing. Since there are some differences
in syntax, it can occasionally be misleading, but it is often more convenient
than problematic.

Grading
-------
On top of simply running code, there is a way to 'grade' code. We can pass the
target code to be graded (typically the adversary code) and the grader code.
By separating the target and grader code, we can guarantee that the target
code cannot interfere with a well-written grader code.  The grader code must
provide a function called grader, which receives the main function from the
target code. Presumably, the grader code runs a series of test inputs and
checks against expected outputs and return its verdict. The grader environment
can also be extended to include special functions that may be useful only for
the grader.
