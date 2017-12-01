"""Brainf**k interpreter"""
class BF:
    """Environment for running brainf**k"""
    class IO:
        """Getch implementation. Credit to Phylliida on SO"""
        class _GetchUnix:
            def __init__(self):
                import tty, sys, termios # import termios now or else you'll get the Unix version on the Mac

            def __call__(self):
                import sys, tty, termios
                fd = sys.stdin.fileno()
                old_settings = termios.tcgetattr(fd)
                try:
                    tty.setraw(sys.stdin.fileno())
                    ch = sys.stdin.read(1)
                finally:
                    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
                return ch

        class _GetchWindows:
            def __init__(self):
                import msvcrt

            def __call__(self):
                import msvcrt
                return msvcrt.getch()

        class _GetchMacCarbon:
            """
            A function which returns the current ASCII key that is down;
            if no ASCII key is down, the null string is returned.  The
            page http://www.mactech.com/macintosh-c/chap02-1.html was
            very helpful in figuring out how to do this.
            """
            def __init__(self):
                import Carbon
                Carbon.Evt #see if it has this (in Unix, it doesn't)

            def __call__(self):
                import Carbon
                if Carbon.Evt.EventAvail(0x0008)[0]==0: # 0x0008 is the keyDownMask
                    return ''
                else:
                    #
                    # The event contains the following info:
                    # (what,msg,when,where,mod)=Carbon.Evt.GetNextEvent(0x0008)[1]
                    #
                    # The message (msg) contains the ASCII char which is
                    # extracted with the 0x000000FF charCodeMask; this
                    # number is converted to an ASCII character with chr() and
                    # returned
                    #
                    (what,msg,when,where,mod)=Carbon.Evt.GetNextEvent(0x0008)[1]
                    return chr(msg & 0x000000FF)

        class _Getch:
            """Gets a single character from standard input.  Does not echo to the
        screen. From http://code.activestate.com/recipes/134892/"""
            def __init__(self):
                try:
                    self.impl = BF.IO._GetchWindows()
                except ImportError:
                    try:
                        self.impl = BF.IO._GetchMacCarbon()
                    except (AttributeError, ImportError):
                        self.impl = BF.IO._GetchUnix()

            def __call__(self): return self.impl()

        @staticmethod
        def getch() -> chr:
            inkey = BF.IO._Getch()
            import sys
            for i in range(sys.maxsize):
                k=inkey()
                if k != '':break
            print(k,end='')
            return k

        @staticmethod
        def cprint(text: str, color: str = None):
            from termcolor import colored
            if color is None:
                print(text)
                return
            print(colored(text, color))

    class Cell:
        """Individual cells in a brainf**k tape"""
        def __init__(self, size: int = 255, wrapping: bool = True):
            # maximum cell value
            self.size = size
            # whether to wrap the cell
            self.wrapping = wrapping
            # the cell's value
            self.value = 0

        def __str__(self):
            return str(self.value)

        def inc(self) -> None:
            """Increment the cell"""
            if self.wrapping is True:
                # if the value has exceeded the maximum, reset it to zero
                self.value = self.value + 1 if self.value < self.size - 1 else 0
            else:
                # clamp new value within bounds of [0, self.max]
                self.value = min(max(self.value + 1, 0), self.size - 1)

        def dec(self) -> None:
            """Decrement the cell"""
            if self.wrapping is True:
                # if the value has exceeded the maximum, reset it to zero
                self.value = self.value - 1 if self.value > 0 else self.size - 1
            else:
                # clamp new value within bounds of [0, self.max]
                self.value = min(max(self.value - 1, 0), self.size - 1)

        def output(self) -> None:
            """Print the contents of the cell to the console"""
            print(chr(self.value),end='')

        def input(self) -> None:
            """Get input from the user"""
            try:
                # get user input as ASCII text and convert it to an int, clamping into the cell size
                k = BF.IO.getch()
                self.value = min(max(ord(k), 0), self.size)
            # if the user input can't convert to integer, don't do anything
            except ValueError:
                pass

    class Tape:
        """Brainf**k tape"""
        def __init__(self, length: int, size: int, wrapping: bool):
            # memory
            self.memory = [BF.Cell(size, wrapping) for e in range(length)]
            # pointer to active cell
            self._pointer = BF.Cell(length, wrapping)

        def __str__(self):
            return ','.join(str(e) for e in self.memory)

        def echo(self):
            BF.IO.cprint(str(self), "blue")

        @property
        def pointer(self) -> int:
            """Get pointer value"""
            return self._pointer.value

        @property
        def active(self):
            """Return the active cell"""
            return self.memory[self.pointer]

        def right(self) -> None:
            """Increment the pointer"""
            self._pointer.inc()

        def left(self) -> None:
            """Decrement the pointer"""
            self._pointer.dec()

    def __init__(self, length: int = 256, size: int = 255, wrapping: bool = True, eol: int = 0):
        # various settings
        self.wrapping, self.length, self.size, self.eol = wrapping, length, size, eol
        # initialize memory and execution stuff
        self.tape, self.loops, self.cmdp = BF.Tape(self.length, self.size, self.wrapping), [], 0
        # command dict
        self.CMDS = {
            '+': self.tape.active.inc,
            '-': self.tape.active.dec,
            ',': self.tape.active.input,
            '.': self.tape.active.output,
            '>': self.tape.right,
            '<': self.tape.left,
            '[': self.loop,
            ']': self.close,
        }

    def __str__(self):
        return str(self.tape)

    @property
    def pointer(self):
        """Return the environment's current pointer value"""
        print("pointer: {}".format(self.tape.pointer))
        return self.tape.pointer

    @property
    def active(self):
        """Return the active cell"""
        return self.tape.active

    def loop(self) -> None:
        """Begin a loop"""
        self.loops.append(self.cmdp)

    def close(self) -> None:
        """Close a loop"""
        if self.active.value == self.eol:
            self.loops.pop()
        else:
            try:
                self.cmdp = self.loops[-1]
            except IndexError:
                raise Exception("unmatched close bracket ({})".format(self.cmdp))

    @staticmethod
    def interpret(source, length: int = 256, size: int = 255, wrapping: int = True, eol: int = 0, comment: chr = ';') -> Tape:
        """Execute string"""
        try:
            file = open(source)
            source = []
            for line in file:
                for ch in line:
                    if ch == comment:
                        break
                    source += ch
        except (PermissionError, FileNotFoundError):
            pass

        # setup the environment
        env = BF(length, size, wrapping, eol)
        try:
            while env.cmdp < len(source):
                cmd = source[env.cmdp]
                try:
                    # run whatever command is specified
                    env.CMDS[cmd]()
                except KeyError:
                    # if the command is not found check to see if it's a loop
                    raise Exception("unkown command ({})".format(env.cmdp))
                env.cmdp += 1
        except KeyboardInterrupt:
            return env.tape

        # make sure all loops are closed
        if len(env.loops) > 0:
            raise Exception("unmatched open bracket ({})".format(env.loops[-1]))

        print()
        # return the tape
        return env.tape

    @staticmethod
    def dump(tape: Tape, file: str = "dump.txt") -> str:
        """Dump tape to file"""
        open(file, "w").write(str(tape))
        return tape

def main():
    """Main function"""
    # setup parser for taking command line arguments
    import argparse
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

if __name__ == "__main__":
    main()
