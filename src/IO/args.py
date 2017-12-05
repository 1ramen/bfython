"""Setup the arguments for cli use"""
import argparse
parser = argparse.ArgumentParser(description="Brainf**k interpreter")
parser.add_argument('-f', '--file', metavar='', type=str, required=True, help="file to interpret")
parser.add_argument('-l', '--length', metavar='', type=int, default=256, help="length of tape")
parser.add_argument('-s', '--size', metavar='', type=int, default=255, help="size of each cells")
parser.add_argument('-w', '--wrapping', metavar='', type=bool, default=True, help="whether to wrap cell values")
parser.add_argument('-e', '--endofloop', metavar='', type=int, default=0, help="value to end a loop on")
parser.add_argument('-c', '--comment', metavar='', type=str, default='#', help="symbol for a comment")
parser.add_argument('-d', '--dump', metavar='', type=str, help="file to dump memory to (if none is provided file will not be dumped)")