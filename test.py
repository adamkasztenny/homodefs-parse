import homparser.homdeflex

# Test it out
data = open('tests/testinput').read()

lexer = homparser.homdeflex.lexer
parser = homparser.homdefyacc.parser

# Give the lexer some input
lexer.input(data)

# Tokenize
while True:
    tok = lexer.token()
    if not tok:
        break      # No more input
    print(tok)
