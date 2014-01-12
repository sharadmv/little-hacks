class LHError(Exception):
    pass

class LHReturn(Exception):
    def __init__(self, val):
        self.val = val

class Frame:
    def __init__(self, parent=None):
        self.bindings = {}
        self.parent = parent

    def set(self, name, value):
        self.bindings[name] = value

    def get(self, name):
        if name in self.bindings:
            return self.bindings[name]
        if not self.parent:
            raise LHError("variable lookup error - %s" % name)
        return self.parent.get(name)

class LHFunc:
    def __init__(self, params, body, frame):
        self.body = body
        self.frame = frame
        self.params = params

    def call(self, args):
        frame = Frame(self.frame)
        for param, arg in zip(self.params, args):
            frame.set(param, arg)
        return self.body.eval(frame)


def _PRINT(env, *args):
    print(*list(map(lambda x: x.eval(env), args)))

NATIVE = {
    "_PRINT" :  _PRINT
}
