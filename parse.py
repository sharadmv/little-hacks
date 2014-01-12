import ast
import sys
import io
from nodes import *

class FileVisitor(ast.NodeVisitor):

    def __init__(self, file=sys.stdout):
        ast.NodeVisitor.__init__(self)
        self.level = 0
        self.file = file

    def visit_Compare(self, node):
        self.p("(binop")
        self.indent()
        self.visit(node.left)
        self.visit(node.comparators[0])
        self.p("(op %s)" % get_op(node.ops[0]))
        self.dedent()
        self.p(")")

    def visit_If(self, node):
        self.p("(if")
        self.indent()
        self.visit(node.test)
        self.p("(body")
        self.indent()
        for item in node.body:
            self.visit(item)
        self.dedent()
        self.p(")")
        self.dedent()
        self.p(")")

    def visit_Assign(self, node):
        self.p("(assign")
        self.indent()
        self.visit(node.targets[0])
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
        self.p("(call")
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
        ast.Or : "or",
        ast.Eq : "eq",
        ast.Lt : "lt",
        ast.Gt : "gt",
        ast.LtE : "lte",
        ast.GtE : "gte",
    }
    return objects[type(obj)]

def ast_parse(code, module):
    node = ast.parse(code)
    #print(ast.dump(node))
    sio = io.StringIO()
    visitor = FileVisitor(sio)
    if module:
        visitor.p("(module")
        visitor.indent()
    visitor.visit(node)
    if module:
        visitor.dedent()
        visitor.p(")")
    return visitor.file.getvalue()


def tokenize(string):
    lst = []
    curword = ""
    for char in string:
        if char in (" ", "\n"):
            if curword != "":
                lst.append(curword)
                curword = ""
            continue
        if char == "(" or char == ")":
            if curword != "":
                lst.append(curword)
                curword = ""
            lst.append(char)
        else:
            curword += char
    return lst

    if string == "":
        return lst
    if string[0] == "(":
        return lst + ["("] + tokenize(string[1:])
    elif string[0] == ")":
        return lst + [")"] + tokenize(string[1:])
    elif string[0] in (" ", "\n"):
        print("S1", string)
        print("S2", string[1:])
        return lst + tokenize(string[1:])
    else:
        word, index = get_first_word(string)
        return lst + [word] + tokenize(string[index:])
    return lst

def get_first_word(string):
    buffer = ""
    i = 0
    char = string[i]
    while char not in (" ", "\n", "(", ")"):
        buffer += char
        i += 1
        char = string[i]
    return buffer, i


def read(tokens):
    if (tokens[0] == '('):
        tokens.pop(0)
        name = tokens.pop(0)
        children = []
        while tokens[0] != ")":
            children.append(read(tokens))
        node = NODES[name](children)
        tokens.pop(0)
        return node
    else:
        return tokens.pop(0)

def parse(text, module=False):
    tokens = tokenize(ast_parse(text, module))
    return read(tokens)

if __name__ == "__main__":
    from argparse import ArgumentParser
    argparse = ArgumentParser()
    argparse.add_argument("file")
    args = argparse.parse_args()
    text = open(args.file).read()
    ast_str = ast_parse(text, sys.stdout)
    tokens = tokenize(ast_str)
    ast = read(tokens)
    print(ast)
