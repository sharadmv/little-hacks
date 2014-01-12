BINOPS = {
    "add" : lambda x, y: x + y,
    "sub" : lambda x, y: x - y,
    "mul" : lambda x, y: x * y,
    "div" : lambda x, y: x / y,
    "mod" : lambda x, y: x % y,
    "pow" : lambda x, y: x ** y,
    "ls" : lambda x, y: x << y,
    "rs" : lambda x, y: x >> y,
    "fdiv" : lambda x, y: x // y,
    "eq" : lambda x, y: x == y,
    "lt" : lambda x, y: x < y,
    "gt" : lambda x, y: x > y,
    "lte" : lambda x, y: x <= y,
    "gte" : lambda x, y: x >= y,
}

def lh_and(args, env):
    val = True
    for elem in args:
        val = val and elem.eval(env)
        if not val:
            break
    return val

def lh_or(args, env):
    val = False
    for elem in args:
        val = val or elem.eval(env)
        if val:
            break
    return val

BOOLOPS = {
    "and" : lh_and,
    "or" : lh_or
}
