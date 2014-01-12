import sys

from parse import parse
from nodes import *
from argparse import ArgumentParser

argparse = ArgumentParser()
argparse.add_argument("file", nargs='?')
argparse.add_argument("-i", action="store_true")
argparse.add_argument("-a", action="store_true")

def repl(env):
    while True:
        sys.stdout.write("> ")
        code = input()
        ast = parse(code)
        try:
            result = ast.eval(env)
            if result != None:
                print(result)
        except LHError as e:
            print(e)

if __name__ == "__main__":
    args = argparse.parse_args()
    env = Frame()
    if args.file:
        prelude = open('lib/prelude.py').read()
        text = open(args.file).read()
        ast = parse(prelude+'\n'+text, module=True)
        if args.a:
            print(ast)
            sys.exit(0)
        ast.eval(env)
    if args.i:
        repl(env)
