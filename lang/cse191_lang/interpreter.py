import itertools
import traceback

from .yacc import parse
from .builtins import builtins
from . import constructs
from . import printer
from .grader_tools import grader_tools

class Env:
    def __init__(self, parent=None, builtins=None):
        self._parent = parent
        self._env = {}
        self._builtins = builtins

    def __contains__(self, k):
        return k in self._env

    def __getitem__(self, k):
        try:
            return self._env[k]
        except KeyError:
            if self._parent:
                return self._parent[k]
            # Stripping leading $ allows us to access built-ins when needed
            # without worrying about user overriding them
            return self._builtins[k]

    def __setitem__(self, k, v):
        if k in self._env:
            self._env[k] = v
        elif self._parent:
            self._parent[k] = v
        else:
            raise KeyError(k)

    def decl(self, k, v=None):
        assert k not in self._env, ("%s was previously declared" % k)
        self._env[k] = v

class Return(Exception):
    def __init__(self, value):
        self.value = value

def run_code(code, base_env=None, out=None):
    """Run user code

    Args:
        code (str): the code to run
        base_env (Env): top level environment to include
        out (list): existing output list to append to

    Returns:
        Env, str: A tuple of the resulting environment and a line-separated
            string of output data from the print function
    """
    x = builtins.copy()
    if out is None:
        out = []
    x['print'] = printer.formatter(lambda x: out.append(x))
    if base_env:
        x.update(base_env)
    env = Env(builtins=x)
    run(parse(code.strip('\r\n') + '\n'), env)
    return (env, '\n'.join(out))

def grade_code(code, grader):
    """Grade user code

    Args:
        code (str): the code to grade (must have "main" function)
        grader (str): the code to grade (must have "grade" function that
            takes as a single argument the "main" function of the
            code to grade)

    Returns:
        str, str: A tuple of the string returned by the grade function and
            a line-separated string of any output data from the print
            function
    """
    out = []
    try:
        env, _ = run_code(code, out=out)
        assert 'main' in env, "Target code has no main function"

        grader_env, _ = run_code(grader, grader_tools, out)
        grade = grader_env['grader'](env['main'])
        return (str(grade), '\n'.join(out) or None)
    except Exception:
        return (None, "%s\n%s" % ('\n'.join(out), traceback.format_exc()))

def run(node, env, ticks=None):
    if ticks is None:
        ticks = [1000000]
    assert ticks[0] > 0, "Exceeded maximum number of ticks"
    ticks[0] -= 1

    recurse = lambda x: run(x, env, ticks)

    if isinstance(node, constructs.Id):
        return env[node.id]

    elif isinstance(node, constructs.While):
        while True:
            cond = recurse(node.condition)
            assert isinstance(cond, bool)
            if cond is False:
                break
            assert cond is True
            recurse(node.do)

    elif isinstance(node, constructs.If):
        cond = recurse(node.condition)
        assert isinstance(cond, bool)
        if cond is True:
            recurse(node.then)
        else:
            recurse(node.otherwise)

    elif isinstance(node, constructs.Decl):
        env.decl(node.decl.id)

    elif isinstance(node, constructs.Assign):
        if isinstance(node.target, constructs.Id):
            env[node.target.id] = recurse(node.expr)
        elif isinstance(node.target, constructs.Index):
            target = recurse(node.target.array)
            assert isinstance(target, list), "Type is not indexable"

            index = recurse(node.target.index)

            try:
                target[index] = recurse(node.expr)
            except IndexError:
                raise IndexError((target, index))
        else:
            raise NotImplementedError("Cannot assign to %s" % type(node.target))

    elif isinstance(node, constructs.Index):
        try:
            return recurse(node.array)[recurse(node.index)]
        except IndexError:
            raise IndexError((node.array, node.index))

    elif isinstance(node, constructs.Stmts):
        recurse(node.stmt)
        if node.rest:
            recurse(node.rest)

    elif isinstance(node, constructs.Return):
        raise Return(recurse(node.expr))

    elif isinstance(node, constructs.Call):
        func = recurse(node.callee)
        params = [recurse(param) for param in node.params]
        return func(*params)

    elif isinstance(node, constructs.Func):
        def f(*a):
            e = Env(env)
            assert(len(a) == len(node.args))
            for arg, val in zip(node.args, a):
                e.decl(arg.id, val)
            try:
                run(node.stmts, e, ticks)
            except Return as r:
                return r.value
        env.decl(node.name.id, f)

    elif isinstance(node, constructs.Num):
        return node.num

    elif isinstance(node, constructs.Bool):
        return node.value

    elif isinstance(node, constructs.Str):
        return node

    elif node is not None:
        raise NotImplementedError(type(node))
