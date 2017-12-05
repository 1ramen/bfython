"""Setup the arguments for cli use"""
import argparse
argparser = argparse.ArgumentParser(description="Brainf**k interpreter")
argparser.add_mutually_exclusive_group()
argparser.add_argument('file', type=str, help="file to interpret")
argparser.add_argument('-l', '--length', metavar='', type=int, default=256, help="length of tape")
argparser.add_argument('-s', '--size', metavar='', type=int, default=255, help="size of each cells")
argparser.add_argument('-w', '--wrapping', metavar='', type=bool, default=True, help="whether to wrap cell values")
argparser.add_argument('-e', '--endofloop', metavar='', type=int, default=0, help="value to end a loop on")
argparser.add_argument('-c', '--comment', metavar='', type=str, default='#', help="symbol for a comment")
argparser.add_argument('-d', '--dumpfile', metavar='', type=str, help="file to dump memory to (if none is provided file will not be dumped)")