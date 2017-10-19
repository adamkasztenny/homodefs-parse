from homparser import homdeflex,homdefyacc


# Test it out
data = open('tests/testinput').read()

lexer = homdeflex.lexer
parser = homdefyacc.parser

# Give the lexer some input
lexer.input(data)

# Tokenize
# while True:
#     tok = lexer.token()
#     if not tok:
#         break      # No more input
#     print(tok)

result = parser.parse(data)

print result