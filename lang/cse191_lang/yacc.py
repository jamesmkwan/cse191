import ply.yacc
from collections import namedtuple as t

from .lex import tokens, lexer, binops
from .builtins import builtins
from . import constructs

precedence = (
    ('right', 'ASSIGN'),
    ('left', 'CAT'),
    ('left', 'XOR'),
    ('left', 'ADD', 'SUB'),
    ('left', 'MUL'),
)

def p_stmts(t):
    '''stmts : stmt stmts
             | '''
    if len(t) == 3:
        t[0] = constructs.Stmts(t[1], t[2])
    else:
        t[0] = None

def p_func(t):
    'stmt : FUNCTION ID LPAREN args RPAREN LBRACE stmts RBRACE'
    t[0] = constructs.Func(constructs.Id(t[2]), t[4], t[7])

def p_args(t):
    '''args : non_empty_args
            | '''
    if len(t) == 2:
        t[0] = t[1]
    else:
        t[0] = []

def p_non_empty_args(t):
    '''non_empty_args : ID COMMA non_empty_args
                      | ID'''
    t[0] = [constructs.Id(t[1])]
    if len(t) == 4:
        t[0].extend(t[3])

def p_params(t):
    '''params : non_empty_params
              | '''
    if len(t) == 2:
        t[0] = t[1]
    else:
        t[0] = []

def p_non_empty_params(t):
    '''non_empty_params : expr COMMA non_empty_params
                        | expr'''
    t[0] = [t[1]]
    if len(t) == 4:
        t[0].extend(t[3])

def p_if(t):
    'stmt : IF LPAREN expr RPAREN LBRACE stmts RBRACE opt_else'
    t[0] = constructs.If(t[3], t[6], t[8])

def p_opt_else(t):
    '''opt_else : ELSE LBRACE stmts RBRACE
                | '''
    if len(t) == 5:
        t[0] = t[3]
    else:
        t[0] = None

def p_while(t):
    'stmt : WHILE LPAREN expr RPAREN LBRACE stmts RBRACE'
    t[0] = constructs.While(t[3], t[6])

def p_assignable_index(t):
    'assignable : expr2 LBRACK expr RBRACK'
    t[0] = constructs.Index(t[1], t[3])

def p_assignable_id(t):
    'assignable : ID'
    t[0] = constructs.Id(t[1])

def p_expr3_str(t):
    'expr3 : STR'
    t[0] = constructs.Str(t[1])

def p_expr3_bool_true(t):
    'expr3 : TRUE'
    t[0] = constructs.Bool(True)

def p_expr3_bool_false(t):
    'expr3 : FALSE'
    t[0] = constructs.Bool(False)

def p_expr3_num(t):
    'expr3 : NUM'
    t[0] = constructs.Num(t[1])

def p_expr3_id(t):
    'expr3 : assignable'
    t[0] = t[1]

def p_expr3(t):
    'expr3 : LPAREN expr RPAREN'
    t[0] = t[2]

def p_expr2_call(t):
    'expr2 : expr2 LPAREN params RPAREN'
    t[0] = constructs.Call(t[1], t[3])

def p_expr2(t):
    'expr2 : expr3'
    t[0] = t[1]

def p_expr(t):
    'expr : expr2'
    t[0] = t[1]

def p_expr_binops(t):
    '''expr : expr2 ADD expr
            | expr2 SUB expr
            | expr2 MUL expr
            | expr2 MOD expr
            | expr2 CAT expr
            | expr2 XOR expr
            | expr2 LT expr
            | expr2 GT expr
            | expr2 LTE expr
            | expr2 GTE expr
            | expr2 EQ expr
    '''
    # $ is not a character that the user can use in an identifier
    # We use it as a prefix for internal functions (in this case, binary ops)
    t[0] = constructs.Call(constructs.Id('$' + binops[t[2]]), (t[1], t[3]))

def p_expr2_substr(t):
    'expr2 : expr2 LBRACK expr COLON expr RBRACK'
    t[0] = constructs.Call(constructs.Id('$substr'), (t[1], t[3], t[5]))

def p_stmt_decl(t):
    'stmt : VAR ID NL'
    t[0] = constructs.Decl(constructs.Id(t[2]))

def p_stmt_assign(t):
    'stmt : assignable ASSIGN expr NL'
    t[0] = constructs.Assign(t[1], t[3])

def p_stmt_decl_assign(t):
    'stmt : VAR ID ASSIGN expr NL'
    id = constructs.Id(t[2])
    decl = constructs.Decl(id)
    asgn = constructs.Assign(id, t[4])
    t[0] = constructs.Stmts(decl, constructs.Stmts(asgn, None))

def p_stmt_expr(t):
    'stmt : expr NL'
    t[0] = t[1]

def p_stmt_return(t):
    'stmt : RETURN expr NL'
    t[0] = constructs.Return(t[2])

def p_stmt_nl(t):
    'stmt : NL'
    t[0] = None

def p_error(p):
    raise Exception("Syntax error at: %r" % p)

yacc = ply.yacc.yacc(debug=False, tabmodule='foo', outputdir='/tmp')
def parse(s):
    lex = lexer.clone()
    return yacc.parse(s, lexer=lex)
