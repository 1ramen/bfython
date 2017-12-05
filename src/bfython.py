"""Brainf**k interpreter"""
import core
from IO.args import argparser

def main():
    """Load and execute a brainf**k source file"""
    # parse the command line arguments
    args = argparser.parse_args()
    # generate tokens from a file
    tokens = core.parser.lex(args.file, args.comment)
    # execute the code and generate a resulting tape
    tape = core.parser.parse(tokens, args.length, args.size, args.wrapping, args.endofloop)
    # dump the tape to a file
    if args.dumpfile is not None:
        core.parser.dump(args.dumpfile, tape)

if __name__ == "__main__":
    main()