import ply.lex

tokens = (
    'STR',
    'ID',
    'NUM',
    'NL',

    'RETURN',
    'FUNCTION',
    'TRUE',
    'FALSE',

    'VAR',

    'LBRACK',
    'RBRACK',
    'LPAREN',
    'RPAREN',
    'COMMA',
    'COLON',

    'IF',
    'ELSE',
    'WHILE',
    #'FOR',
    'LBRACE',
    'RBRACE',

    'ASSIGN',
    'ADD',
    'SUB',
    'MUL',
    'MOD',
    'CAT',
    'XOR',
    'LT',
    'GT',
    'LTE',
    'GTE',
    'EQ',
)

reserved = (
    'function',
    'return',
    'var',
    'if',
    'else',
    'while',
    'True',
    'False',
)
binops = {
    '=': 'assign',
    '+': 'add',
    '-': 'sub',
    '*': 'mul',
    '%': 'mod',
    '||': 'cat',
    '^': 'xor',
    '<': 'lt',
    '>': 'gt',
    '<=': 'lte',
    '>=': 'gte',
    '==': 'eq',
}

#t_BIN = r'0b[01]*'

t_LPAREN = r'\('
t_RPAREN = r'\)'
t_COMMA = ','
t_LBRACE = '{'
t_RBRACE = '}'
t_LBRACK = r'\['
t_RBRACK = r'\]'
t_COLON = ':'

t_ignore = ' \t'

def t_BINOP(t):
    r'[\!\#\$\%\&\*\+\.\/\<\=\>\?\@\\\^\|\-\~]+'
    if t.value in binops:
        t.type = binops[t.value].upper()
        return t

def t_STR(t):
    r'"([^"\\]|\\"|\\\\)*"'
    t.value = t.value[1:-1]
    t.value = t.value.replace(r'\"', '"')
    t.value = t.value.replace(r'\\', '\\')
    return t

def t_HEX(t):
    r'0x[0-9a-fA-F]+'
    t.value = int(t.value, 16)
    t.type = 'NUM'
    return t

def t_NUM(t):
    r'-?\d+'
    t.value = int(t.value)
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    if t.value in reserved:
        t.type = t.value.upper()
    return t

def t_NL(t):
    r'[;\r\n]+'
    t.lexer.lineno += t.value.count('\n')
    return t

def t_error(t):
    raise Exception("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lexer = ply.lex.lex()
