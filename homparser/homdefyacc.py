import ply.yacc as yacc
from homdeflex import tokens
import homdefast as ast

def p_program(p):
    '''program: joinspec sequentialspec'''
    ast.Program(p[1], p[3])

def p_joinspec(p):
    '''joinspec: JOIN LPAREN arglist SEPARATOR arglist RPAREN RETURNS identlist LOCALS arglist block'''
    ast.JoinSpec(p[3], p[5], p[8], p[10], p[11])

def p_sequentialspec(p):
    '''sequentialpec: SEQUENTIAL LPAREN arglist RPAREN RETURNS identlist LOCALS arglist block'''
    ast.JoinSpec(p[3], p[6], p[8], p[9])

# List or arguments
def p_arglist_singleton(p):
    '''arglist: arg'''
    list(p[1])

def p_arglist_mutliple(p):
    ''' arglist: arg COMMA arglist'''
    list(p[1]).extend(p[3])

def p_arglist_empy(p):
    '''arglist:'''
    list()

def p_arg(p):
    '''arg: type ID'''
    ast.Argument(p[0], p[1])

# List of identifiers
def p_identlist_singleton(p):
    '''identlist: ID'''
    list(p[1])

def p_identlist_mutliple(p):
    '''identlist: ID COMMA identlist'''
    list(p[1]).extend(p[3])

def p_identlist_empy(p):
    '''identlist:'''
    list()


def p_binary_expression(p):
    '''binexp : expression PLUS expression
    | expression MINUS expression
    | expression TIMES expression
    | expression DIV expression'''



def p_block(p):
    '''statement: LBRACE RBRACE'''


parser = yacc.yacc()