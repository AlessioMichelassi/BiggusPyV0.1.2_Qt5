# st = 'def foo():\n    print ("hello") \n\ndef bla():\n    a = 1\n    b = 2\nc= a+b\nprint(c)'

code = """
def add_and_multiply(a, b, c):
    d = a + b
    e = d * c
    return e

x = add_and_multiply(1, 2, 3)
y = add_and_multiply(4, 5, 6)
z = x + y
print(z)
"""

import ast

tree = ast.parse(code)
for function in tree.body:
    if isinstance(function, ast.FunctionDef):
        # Just in case if there are loops in the definition
        lastBody = function.body[-1]
        while isinstance(lastBody, (ast.For, ast.While, ast.If)):
            lastBody = lastBody.Body[-1]
        lastLine = lastBody.lineno
        if isinstance(code, str):
            code = code.split("\n")
        returnCode = ""
        for i, line in enumerate(code, 1):
            if i in range(function.lineno, lastLine + 1):
                returnCode += line
        print(returnCode)

code = """
if 1 == 1 and 2 == 2 and 3 == 3:
     test = 1
"""
node = ast.parse(code)
a = ast.get_source_segment(code, node.body[0])
print(a)