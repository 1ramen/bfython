"""Brainf**k interpreter"""
class BF:
    """Environment for running brainf**k"""
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
                self.value = min(max(input()[]), 0), self.size)
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

        # return the tape
        return env.tape

    @staticmethod
    def dump(tape: Tape, file: str = "dump.txt") -> str:
        """Dump tape to file"""
        open(file, "w").write(str(tape))
        return tape

def main():
    """Main function"""
    BF.dump(BF.interpret(',++.'), "dump.txt")

if __name__ == "__main__":
    main()
