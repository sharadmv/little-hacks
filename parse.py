import ast
import sys
import io

class Visitor(ast.NodeVisitor):

    def __init__(self, file=sys.stdout):
        ast.NodeVisitor.__init__(self)
        self.level = 0
        self.file = file

    def visit_Assign(self, node):
        self.p("(assign")
        self.indent()
        self.p("(targetlist")
        self.indent()
        for target in node.targets:
            self.visit(target)
        self.dedent()
        self.p(")")
        self.visit(node.value)
        self.dedent()
        self.p(")")

    def visit_Name(self, node):
        self.p("(id %s)" % node.id)

    def visit_Tuple(self, node):
        self.p("(tuple")
        self.indent()
        for elem in node.elts:
            self.visit(elem)
        self.dedent()
        self.p(")")

    def visit_Call(self, node):
        sef.p("(call")
        self.indent()
        self.visit(node.func)
        self.p("(exprlist")
        self.indent()
        for elem in node.args:
            self.visit(elem)
        self.dedent()
        self.p(")")
        self.dedent()
        self.p(")")

    def visit_FunctionDef(self, node):
        self.p("(def")
        self.indent()

        self.p("(id %s)" % node.name)
        self.p("(formalslist")
        self.indent()

        for formal in node.args.args:
            self.p("(id %s)" % formal.arg)

        self.dedent()
        self.p(")")

        self.p("(block")
        self.indent()
        for line in node.body:
            self.visit(line)

        self.dedent()
        self.p(")")

        self.dedent()
        self.p(")")

    def visit_Return(self, node):
        self.p("(return")
        self.indent()
        self.visit(node.value)
        self.dedent()
        self.p(")")

    def visit_Num(self, node):
        self.p("(num %s)" % node.n)

    def visit_BinOp(self, node):
        self.p("(binop")
        self.indent()

        self.visit(node.left)
        self.visit(node.right)
        self.p("(op %s)" % get_op(node.op))
        self.dedent()
        self.p(")")

    def visit_BoolOp(self, node):
        self.p("(boolop")
        self.indent()

        self.p("(exprlist")
        self.indent()
        for val in node.values:
            self.visit(val)
        self.dedent()
        self.p(")")
        self.p("(op %s)" % get_op(node.op))
        self.dedent()
        self.p(")")

    def indent(self):
        self.level += 1

    def dedent(self):
        self.level -= 1

    def p(self, text):
        make_indent(self.level, self.file)
        self.file.write(text)
        self.file.write('\n')

def make_indent(value, file):
    file.write("    "*value)

def get_op(obj):
    objects = {
        ast.Add : "add",
        ast.Sub : "sub",
        ast.Mult : "mul",
        ast.Div : "div",
        ast.Mod : "mod",
        ast.Pow : "pow",
        ast.LShift : "ls",
        ast.RShift : "rs",
        ast.BitOr : "bor",
        ast.BitXor : "bxor",
        ast.BitAnd : "band",
        ast.FloorDiv : "fdiv",
        ast.And : "and",
        ast.Or : "or"
    }
    return objects[type(obj)]

def parse(code):
    node = ast.parse(code)
    sio = io.StringIO()
    visitor = Visitor(sio)
    visitor.p("(module")
    visitor.indent()
    visitor.visit(node)
    visitor.dedent()
    visitor.p(")")
    return visitor.file.getvalue()

if __name__ == "__main__":
    from argparse import ArgumentParser
    argparse = ArgumentParser()
    argparse.add_argument("file")
    args = argparse.parse_args()
    text = open(args.file).read()
    ast = parse(text)
    print(ast)
