import ast


class ImportLister(ast.NodeVisitor):
    def visit_Import(self, node):
        for name in node.names:
            print(name.name)

tree = ast.parse(code)
ImportLister().visit(tree)
# put your code here