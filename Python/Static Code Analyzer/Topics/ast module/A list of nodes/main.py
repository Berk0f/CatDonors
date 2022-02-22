import ast

expression = "(34 + 6) * (23**2 - 7 + 45**2)"

tree = ast.parse(expression)

print(len([node for node in ast.walk(tree)]))

# put your code here
