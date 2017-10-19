import homparser.homdefyacc as hdy


# Test it out
data = open('tests/testinput').read()
program = hdy.parser.parse(data)
