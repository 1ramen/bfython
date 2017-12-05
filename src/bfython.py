"""Brainf**k interpreter"""
import core
from IO.args import argparser

def main():
    """Load and execute a brainf**k source file"""
    args = argparser.parse_args()
    tokens = core.parser.lex(args.file, args.comment)
    tape = core.parser.parse(tokens, args.length, args.size, args.wrapping, args.endofloop)
    core.parser.dump(args.dumpfile, tape)
    pass

if __name__ == "__main__":
    main()