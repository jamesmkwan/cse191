import collections
from textwrap import dedent

from . import app

Problem = collections.namedtuple('Problem', ['name', 'prompt', 'starter_code', 'grader_code'])
problems = {}

def slugify(s, allowed_chars=set('abcdefghijklmnopqrstuvwxyz1234567890-')):
    r = ''.join([c for c in s.lower().replace(' ', '-') if c in allowed_chars])
    if not len(r):
        r = 'blank'
    return r

def new_problem(name, prompt, starter_code, grader_code):
    problem = Problem(name, dedent(prompt), dedent(starter_code), dedent(grader_code))

    slug = slugify(name)
    if slug in problems:
        raise Exception("Problem naming conflict")

    problems[slug] = problem

def find_problem(name):
    return problems[slugify(name)]

def list_problems():
    return sorted(p.name for p in problems.values())

new_problem(
    'PS1-1',
    r'''
    Let \(\textbf{Z}_{10} = {0, 1, 2, \dots, 9}\). Consider the symmetric encryption scheme
    in which a message \(M = M[1] M[2] M[3] M[4] \in \textbf{Z}_{10}^4\) is a four-digit string,
    a key \(\pi\) \(\leftarrow\) Perm(\(\textbf{Z}_10\)) is a random permutation on \(\textbf{Z}_10\), and the
    ciphertext \(C = C[1] C[2] C[3] C[4] = \mathcal{E}_\pi(M) \in \textbf{Z}_{10}^4\) is computed as follows:
    <br>
    \(\underline{\mathcal{E}_\pi(M)}\)<br>
    For \(i = 1, \dots, 4\) do<br>
    &nbsp;&nbsp;&nbsp;&nbsp;\(P[i] \leftarrow (M[i] + i) \text{mod} 10\)<br>
    &nbsp;&nbsp;&nbsp;&nbsp;\(C[i] \leftarrow \pi(P[i])\)<br>
    Return C
    ''',
    '''
    function invert(x) {
      var y = array(len(x))
      var i = 0
      while (i < len(x)) {
        y[x[i]] = i
        i = i + 1
      }
      return y
    }

    function main(pi, c) {
      var m = array(4)
      var pi_inv = invert(pi)
      var i = 0
      while (i < 4) {
        m[i] = (pi_inv[c[i]] - (i + 1)) % 10
        i = i + 1
      }
      return m
    }
    ''',
    '''
    function grader(dec) {
      var Z10 = get_Z10()
      var pi = get_Z10()
      var m = array(4)

      var run = 0
      var success = 0
      var c
      var d
      while (run < 20) {
        m[0] = randnum(0, 10)
        m[1] = randnum(0, 10)
        m[2] = randnum(0, 10)
        m[3] = randnum(0, 10)

        print("[", run, "] Message: ", m)
        c = enc(pi, m)
        print("[", run, "] Encrypted: ", c)

        d = dec(pi, c)
        print("[", run, "] Decrypted: ", d)

        if (m == d) {
          success = success + 1
        }
        run = run + 1
      }

      return sprint(percentage(success, run), " success rate")
    }

    function enc(pi, m) {
      var p = array(4)
      var c = array(4)
      var i = 0
      while (i < 4) {
        p[i] = (m[i] + i + 1) % 10
        c[i] = pi[p[i]]
        i = i + 1
      }
      return c
    }

    function get_Z10() {
      var Z10 = array(10)
      var i = 0
      while (i < 10) {
        Z10[i] = i
        i = i + 1
      }
      return Z10
    }

    function shuffle(a) {
      var i = 0
      var n = len(a)
      var j
      var tmp
      while (i <= n - 2) {
        j = randnum(i, n)

        tmp = a[i]
        a[i] = a[j]
        a[j] = tmp

        i = i + 1
      }
      return a
    }
    '''
)

new_problem(
    'PS2-1',
    r'''
    \(\underline{F_{K_1 || K_2}(x_1 || x_2)}\)<br>
    \(y_1 \leftarrow \text{AES}_{x_1}(K_1)\)<br>
    \(y_2 \leftarrow \text{AES}_{K_1}(x_2 \oplus K_2)\)<br>
    Return \(y_1 || y_2\)<br><br>

    Given \((X, C)\) such that \(C = F_K(X)\), recover \(K\).
    ''',
    '''
    function main(x, c) {
      var x1 = x[0:128]
      var x2 = x[128:256]
      var c1 = c[0:128]
      var c2 = c[128:256]

      var k1 = aes_128_inverse(x1, c1)
      var k2 = aes_128_inverse(k1, c2) ^ x2
      return k1 || k2
    }
    ''',
    '''
    function f(k1, k2, x1, x2) {
      var y1 = aes_128(x1, k1)
      var y2 = aes_128(k1, x2 ^ k2)
      return y1 || y2
    }

    function grade(main) {
      var k1 = randbits(128)
      var k2 = randbits(128)

      var x1 = randbits(128)
      var x2 = randbits(128)

      var c = f(k1, k2, x1, x2)
      var x = x1 || x2

      return main(x, c) == k1 || k2
    }

    function grader(main) {
      var i = 1
      var p = 0
      var m = 10
      while (i <= m) {
        if (grade(main)) {
          p = p + 1
        }
        i = i + 1
      }

      return sprint(percentage(p, m), " success rate")
    }
    '''
)

new_problem(
    'PS2-2',
    r'''
    \(F_K(x) = \text{AES}_K(x) || \text{AES}_K^{-1}(x)\)<br>
    Show that F is not a secure PRF by presenting a practical adversary with high advantage.
    ''',
    '''
    function main(fn) {
      var x = fn(zeros(128))
      var x1 = x[0:128]
      var x2 = x[128:256]

      var y = fn(x1)
      var y1 = y[0:128]
      var y2 = y[128:256]

      if (y2 == zeros(128)) {
        return 1
      } else {
        return 0
      }
    }
    ''',
    '''
    function f(k, x) {
      var a = aes_128(k, x)
      var b = aes_128_inverse(k, x)
      return a || b
    }

    function guarded_query(delegate) {
      var previous_queries = array(100)
      var i = 0
      function inner(x) {
        previous_queries[i] = x
        var j = 0
        while (j < i) {
          if (previous_queries[j] == x) {
            failfast("Repeat call to oracle")
          }
          j = j + 1
        }
        i = i + 1
        return delegate(x)
      }
      return inner
    }

    function test_real(main) {
      var k = randbits(128)
      function fn(x) {
        return f(k, x)
      }
      print("Successfully identified real world")
      return main(guarded_query(fn)) == 1
    }

    function test_ideal(main) {
      function fn(x) {
        return randbits(128)
      }
      print("Successfully identified ideal world")
      return main(guarded_query(fn)) == 0
    }

    function grade(main) {
      var n = randnum(0, 2) == 0
      if (n) {
        return test_real(main)
      } else {
        return test_ideal(main)
      }
    }

    function grader(main) {
      var i = 1
      var p = 0
      var m = 100
      while (i <= m) {
        if (grade(main)) {
          p = p + 1
        }
        i = i + 1
      }

      return sprint(percentage(p, m), " success rate")
    }
    '''
)
