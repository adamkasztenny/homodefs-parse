import homparser.homdefyacc as hdy


# Test it out
data = open('tests/testinput').read()
program = hdy.parser.parse(data)

print program.join.argsl[0].type.baseType == 'int'
print program.join.locals[0].type.baseType == 'int'
print program.sequential.locals[0].type.baseType == 'int'