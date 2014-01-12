from impl import *
from runtime import *

class AST:
    def __init__(self, children):
        self.children = children

    def child(self, i):
        return self.children[i]

    def arity(self):
        return len(self.children)
    def dump(self, level=0):
        string = "    "*level
        string += ("(%s" % self.name) + "\n"
        string += "\n".join(list(map(lambda x : x.dump(level+1), self.children)))
        string += "\n"
        string += "    "*level
        string += ")"
        return string

    def __str__(self):
        return self.dump(0)

class ModuleAST(AST):
    name = "module"

    def eval(self, env):
        for stmt in self.children:
            stmt.eval(env)

class IdAST(AST):
    name = "id"
    def __init__(self, children):
        AST.__init__(self, children)
        self.id = self.children[0]

    def dump(self, level=0):
        return "    "*level + "(%s %s)" % (self.name, self.id)

    def eval(self, env):
        return env.get(self.id)

class AssignAST(AST):
    name = "assign"

    def __init__(self, children):
        AST.__init__(self, children)
        self.lhs, self.rhs = self.children

    def eval(self, env):
        rhs = self.rhs.eval(env)
        env.set(self.lhs.id, rhs)

class TargetListAST(AST):
    name = "targetlist"

class NumAST(AST):
    name = "num"
    def __init__(self, children):
        AST.__init__(self, children)
        self.value = self.children[0]

    def dump(self, level=0):
        return "    "*level + "(%s %s)" % ("num", self.children[0])

    def eval(self, env):
        return int(self.value)

class CallAST(AST):
    name = "call"

    def __init__(self, children):
        AST.__init__(self, children)
        self.id = self.child(0).id
        self.args = self.child(1).children

    def eval(self, env):
        if self.id[0] == "_":
            return NATIVE[self.id](env, *self.args)
        func = env.get(self.id)
        return func.call(list(map(lambda x : x.eval(env), self.args)))

class ExprListAST(AST):
    name = "exprlist"

class FormalsListAST(AST):
    name = "formalslist"

class DefAST(AST):
    name = "def"

    def __init__(self, children):
        AST.__init__(self, children)
        self.id = self.child(0).id
        self.formals = self.child(1)
        self.body = self.child(2)

    def eval(self, env):
        func = LHFunc(list(map(lambda x : x.id, self.formals.children)), self.body, env)
        env.set(self.id, func)

class ReturnAST(AST):
    name = "return"

    def eval(self, env):
        raise LHReturn(self.child(0).eval(env))

class BlockAST(AST):
    name = "block"

    def eval(self, env):
        for stmt in self.children:
            try:
                stmt.eval(env)
            except LHReturn as e:
                return e.val
        return None


class BinopAST(AST):
    name = "binop"

    def __init__(self, children):
        AST.__init__(self, children)
        self.left = self.child(0)
        self.right = self.child(1)
        self.op = self.child(2)

    def eval(self, env):
        left = self.left.eval(env)
        right = self.right.eval(env)
        return self.op.call([left, right])

class BoolOpAST(AST):
    name = "boolop"

    def __init__(self, children):
        AST.__init__(self, children)
        self.args = self.child(0)
        self.op = self.child(1).op

    def eval(self, env):
        return BOOLOPS[self.op](self.args.children, env)

class OpAST(AST):
    name = "op"

    def __init__(self, children):
        AST.__init__(self, children)
        self.op = self.child(0)

    def dump(self, level=0):
        return "    "*level + "(%s %s)" % ("op", self.children[0])

    def call(self, args):
        return BINOPS[self.op](*args)

class IfAST(AST):
    name = "if"

    def __init__(self, children):
        AST.__init__(self, children)
        self.test = self.child(0)
        self.body = self.child(1)
    def eval(self, env):
        cond = self.test.eval(env)
        if cond:
            self.body.eval(env)

class BodyAST(ModuleAST):
    pass

NODES = {
    "module" : ModuleAST,
    "assign" : AssignAST,
    "targetlist" : TargetListAST,
    "id" : IdAST,
    "num" : NumAST,
    "call" : CallAST,
    "exprlist" : ExprListAST,
    "def" : DefAST,
    "formalslist" : FormalsListAST,
    "return" : ReturnAST,
    "block" : BlockAST,
    "body" : BodyAST,
    "op" : OpAST,
    "binop" : BinopAST,
    "boolop" : BoolOpAST,
    "if" : IfAST,
}

