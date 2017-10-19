# ------------------------------------------------------------
# homdeflex.py
# Parse a small subset of C
# ------------------------------------------------------------
import ply.lex as lex

# List of token names.   This is always required
reserved = {
    'if' : 'IF',
    'else' : 'ELSE',
    'for' : 'FOR',
    'join' : 'JOIN',
    'sequential' : 'SEQUENTIAL',
    'int' : 'INT',
    'float' : 'FLOAT',
    'bool' : 'BOOL',
    'returns' : 'RETURNS',
    'locals' : 'LOCALS',
    'True' : 'TRUE',
    'False' : 'FALSE'
}

tokens = [
    'AND',
    'COLON',
    'COMMA',
    'DIV',
    'EQ',
    'EQEQ',
    'EXCLAMATION',
    'GEQ',
    'GT',
    'IDENT',
    'LBRACE',
    'LBRACKET',
    'LEQ',
    'LPAREN',
    'LT',
    'MINUS',
    'NEQ',
    'NUMBER',
    'OR',
    'PLUS',
    'QUESTION',
    'RBRACE',
    'RBRACKET',
    'RPAREN',
    'SEMICOLON',
    'TILDE',
    'SEPARE',
    'TIMES',
] + list(reserved.values())



# Regular expression rules for simple tokens
t_INT = r'int'
t_FLOAT = r'float'
t_BOOL = r'bool'
t_AND = r'\&\&'
t_COLON = r'\:'
t_COMMA = r'\,'
t_EQ = r'\='
t_EQEQ = r'\=\='
t_GEQ = r'>='
t_GT = r'>'
t_JOIN = r'join'
t_LBRACE = r'\{'
t_LBRACKET = r'\['
t_LEQ = r'<='
t_LT = r'<'
t_MINUS = r'-'
t_NEQ = r'\!\='
t_EXCLAMATION = r'!'
t_OR = r'\|\|'
t_PLUS = r'\+'
t_QUESTION = r'\?'
t_RBRACE = r'\}'
t_RBRACKET = r'\]'
t_SEMICOLON = r'\;'
t_SEPARE = '\|'
t_TILDE = r'\~'
t_TIMES   = r'\*'
t_DIV  = r'/'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'


# A regular expression rule with some action code
def t_NUMBER(t):
    r'\d+\.*\d*'
    t.value = int(t.value)
    return t


def t_IDENT(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'IDENT')
    return t

# EOF handling rule

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()