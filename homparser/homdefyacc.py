import ply.yacc as yacc
from homdeflex import tokens
import homdefast as ast

precedence = (
    ('nonassoc',    'IFX'),
    ('nonassoc',    'ELSE'),
)


def p_program(p):
    '''program : joinspec sequentialspec'''
    p[0] = ast.Program(p[1], p[2])


def p_joinspec(p):
    '''joinspec : JOIN LPAREN arglist SEPARE arglist RPAREN RETURNS LPAREN identlist RPAREN LOCALS LPAREN arglist RPAREN statement'''
    p[0] = ast.JoinSpec(p[3], p[5], p[9], p[13], p[15])


def p_joinspec_decl_error(p):
    '''joinspec : JOIN error RPAREN block'''
    print "Bad join declaration."

def p_joinspec_body_error(p):
    '''joinspec : JOIN LPAREN arglist SEPARE arglist RPAREN RETURNS LPAREN identlist RPAREN LOCALS LPAREN arglist RPAREN error'''
    print "Bad join body."

def p_sequentialspec(p):
    '''sequentialspec : SEQUENTIAL LPAREN arglist RPAREN RETURNS LPAREN identlist RPAREN LOCALS LPAREN arglist RPAREN statement'''
    p[0] = ast.SequentialSpec(p[3], p[7], p[11], p[13])


# List or arguments
def p_arglist_mutliple(p):
    ''' arglist : arglist COMMA arg'''
    if p[1] is []:
        p[0] = p[1].append(p[3])
    else:
        p[0] = [p[3]]

def p_arglist_singleton(p):
    '''arglist : arg'''
    p[0] = [p[1]]


def p_arglist_empy(p):
    '''arglist :'''
    p[0] = list()

def p_arg(p):
    '''arg : type IDENT'''
    p[0] = ast.Argument(p[1], ast.Var(p[2], p[1]))

def p_arglist_error(p):
    '''arg : error'''
    print "Argument error"

# List of identifiers
def p_identlist_singleton(p):
    '''identlist : identifier'''
    p[0] = [p[1]]


def p_identlist_mutliple(p):
    '''identlist : identifier COMMA identlist'''
    if p[1] is []:
        p[0] = p[1].append(p[3])
    else:
        p[0] = list(p[3])


def p_identlist_empty(p):
    '''identlist :'''
    p[0] = list()


# <primary-expression> ::= <identifier>
#   \alt <constant>
#   \alt <string-literal>
#   \alt '(' <expression> ')'
def p_constant(p):
    '''constant : NUMBER
    | TRUE
    | FALSE'''
    p[0] = ast.Constant(p[1])

def p_postfixExpr(p):
    '''postfixExpression : constant
    | identifier
    | LPAREN expression RPAREN'''
    p[0] = p[1]

def p_identifer(p):
    '''identifier : IDENT'''
    p[0] = ast.Var(p[0], None)

def p_postfixExpr_array_access(p):
    '''postfixExpression : postfixExpression LBRACKET expression RBRACKET'''
    p[0] = ast.ArrayAccess(p[1], p[3])


def p_postfixExpr_funccall(p):
    '''postfixExpression : IDENT LPAREN expressionlist RPAREN'''
    p[0] = ast.FunctionCall(p[1], p[3])


def p_unary_expression(p):
    '''unaryExpression : unop unaryExpression'''
    p[0] = ast.UnaryExpr(p[1], p[2])


def p_unary_expression_id(p):
    '''unaryExpression : postfixExpression'''
    p[0] = p[1]


def p_unop(p):
    '''unop : PLUS
    | MINUS
    | EXCLAMATION
    | TILDE'''
    p[0] = p[1]


def p_multiplicativeExpr_id(p):
    '''multiplicativeExpression : unaryExpression'''
    p[0] = p[1]


def p_multiplicativeExpr(p):
    '''multiplicativeExpression : multiplicativeExpression multop unaryExpression'''
    p[0] = ast.BinaryExpr(p[2], p[1], p[3])


def p_multop(p):
    '''multop : TIMES
    | DIV'''
    p[0] = p[1]


def p_additiveExpr_id(p):
    '''additiveExpression : multiplicativeExpression'''
    p[0] = p[1]


def p_additiveExpr(p):
    '''additiveExpression : additiveExpression addop multiplicativeExpression'''
    p[0] = ast.BinaryExpr(p[2], p[1], p[3])


def p_addop(p):
    '''addop : PLUS
    | MINUS'''
    p[0] = p[1]


def p_relationalExpression_id(p):
    '''relationalExpression : additiveExpression'''
    p[0] = p[1]


def p_relationalExpression(p):
    '''relationalExpression : relationalExpression compop additiveExpression'''
    p[0] = ast.BinaryExpr(p[2], p[1], p[3])


def p_compop(p):
    '''compop : LT
    | LEQ
    | GT
    | GEQ'''
    p[0] = p[1]


def p_equalityExpression_id(p):
    '''equalityExpression : relationalExpression'''
    p[0] = p[1]


def p_equalityExpression(p):
    '''equalityExpression : equalityExpression eqop relationalExpression'''
    p[0] = ast.BinaryExpr(p[2], p[1], p[3])


def p_eqop(p):
    '''eqop : EQEQ
    | NEQ'''
    p[0] = p[1]


def p_andExpression_id(p):
    '''andExpression : equalityExpression'''
    p[0] = p[1]


def p_andExpression(p):
    '''andExpression : andExpression AND equalityExpression'''
    p[0] = ast.BinaryExpr(p[2], p[1], p[3])


def p_orExpression_id(p):
    '''orExpression : andExpression'''
    p[0] = p[1]


def p_orExpression(p):
    '''orExpression : orExpression OR andExpression'''
    p[0] = ast.BinaryExpr(p[2], p[1], p[3])


def p_conditionalExpression_id(p):
    '''conditionalExpression : orExpression'''
    p[0] = p[1]


def p_conditionalExpression(p):
    '''conditionalExpression : orExpression QUESTION expression COLON expression'''
    p[0] = ast.ConditionalExpression(p[1], p[3], p[5])


def p_expression(p):
    '''expression : conditionalExpression'''


def p_expressionlist_singleton(p):
    '''expressionlist : expression'''
    p[0] = list(p[1])


def p_expressionlist_list(p):
    '''expressionlist : expressionlist COMMA expression'''
    p[0] = p[1].append(p[3])


def p_expressionlist_empty(p):
    '''expressionlist :'''
    p[0] = list()


# Statements
def p_statementlist(p):
    '''statementlist : statementlist statement'''
    if p[1] is None:
        p[0] = list()
    else:
        p[0] = p[1].append(p[2])


def p_statementlist_empty(p):
    '''statementlist :'''
    p[0] = list()


def p_assignment(p):
    '''assignmentStatement : postfixExpression EQ expression'''
    p[0] = ast.Assignment(p[1], p[3])

def p_assignment_increment(p):
    '''assignmentStatement : IDENT PLUS PLUS'''
    p[0] = ast.Assignment(p[1], ast.BinaryExpr(p[2], p[1], ast.Constant(0)))

def p_assignment_decrement(p):
    '''assignmentStatement : IDENT MINUS MINUS'''
    p[0] = ast.Assignment(p[1], ast.BinaryExpr(p[2], p[1], ast.Constant(0)))

def p_assignment_rh_error(p):
    '''assignmentStatement : postfixExpression EQ error'''
    print "Error on left hand side of assignment"


def p_assignment_lh_error(p):
    '''assignmentStatement : error EQ expression'''
    print "Error on left hand side of assignment"


def p_statement(p):
    '''statement : assignmentStatement SEMICOLON
    | iterationStatement
    | selectionStatement
    | block'''
    p[0] = p[1]

def p_assignStmt_error(p):
    '''statement : error SEMICOLON'''
    print "Error in statement, rule : <statement>;."


def p_conditional2(p):
    '''selectionStatement : IF LPAREN expression RPAREN statement ELSE statement'''
    p[0] = ast.SelectionStatement(p[3], p[5], p[7])


def p_conditional(p):
    '''selectionStatement : IF LPAREN expression RPAREN statement %prec IFX'''
    p[0] = ast.SelectionStatement(p[3], p[5], None)


def p_iteration(p):
    '''iterationStatement : FOR LPAREN assignmentStatement SEMICOLON expression SEMICOLON assignmentStatement RPAREN statement'''
    p[0] = ast.IterationStatement(p[3],p[4], p[6],p[8])


def p_block(p):
    '''block : LBRACE statementlist RBRACE'''
    p[0] = ast.Block(p[2])


# Types


def p_type_base(p):
    '''type : INT
    | FLOAT
    | BOOL'''
    p[0] = ast.Type(p[1], False)

def p_type_ptr(p):
    '''type : type TIMES'''
    p[0] = ast.Type(p[1], True)


def p_error(p):
    print p
# Error



parser = yacc.yacc()