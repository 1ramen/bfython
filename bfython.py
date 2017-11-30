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
            i = self.value

            if self.wrapping is True:
                # if the value has exceeded the maximum, reset it to zero
                self.value = self.value + 1 if self.value < self.size else 0
            else:
                # clamp new value within bounds of [0, self.max]
                self.value = min(max(self.value + 1, 0), self.size)

        def dec(self) -> None:
            """Decrement the cell"""
            if self.wrapping is True:
                # if the value has exceeded the maximum, reset it to zero
                self.value = self.value - 1 if self.value > 0 else self.size
            else:
                # clamp new value within bounds of [0, self.max]
                self.value = min(max(self.value - 1, 0), self.size)

        def output(self) -> None:
            """Print the contents of the cell to the console"""
            print(str(self))

        def input(self) -> None:
            """Get input from the user"""
            try:
                # get user input as ASCII text and convert it to an int, clamping into the cell size
                self.value = min(max(ord(input()[0]), 0), self.size)
            # if the user input can't convert to integer, don't do anything
            except ValueError:
                pass

    class Tape:
        """Brainf**k tape"""
        def __init__(self, length: int, size: int, wrapping: bool):
            # memory
            self.memory = [BF.Cell(size, wrapping)] * length
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

        def inc(self) -> None:
            """Increment active cell"""
            self.active.inc()

        def dec(self) -> None:
            """Decrement active cell"""
            self.active.dec()

        def output(self) -> None:
            """Print out active cell"""
            self.active.output()

        def input(self) -> None:
            """Get new cell value from user"""
            self.active.input()

    class Bytecode(list):
        """Alias for list"""
        pass

    def __init__(self, length: int = 256, size: int = 255, wrapping: bool = True, eol: int = 0):
        # various settings
        self.wrapping, self.length, self.size, self.eol = wrapping, length, size, eol
        # initialize memory and execution stuff
        self.tape, self.loops, self.cmdp = BF.Tape(self.length, self.size, self.wrapping), [], 0
        # command dict
        self.CMDS = {
            '+': self.inc,
            '-': self.dec,
            '>': self.right,
            '<': self.left,
            ',': self.input,
            '.': self.output,
            '[': self.loop,
            ']': self.close,
        }

    def __str__(self):
        return str(self.tape)

    @property
    def pointer(self):
        return self.tape.pointer

    @property
    def active(self):
        return self.tape.active

    def right(self) -> None:
        """Increment pointer"""
        self.tape.right()

    def left(self) -> None:
        """Decrement pointer"""
        self.tape.left()

    def inc(self) -> None:
        """Increment active cell"""
        self.tape.inc()

    def dec(self) -> None:
        """Decrement active cell"""
        self.tape.dec()

    def output(self) -> None:
        """Print out active cell"""
        self.tape.output()

    def input(self) -> None:
        """Get new cell value from user"""
        self.tape.input()

    def loop(self) -> None:
        """Begin a loop"""
        self.loops.append(self.cmdp)

    def close(self) -> None:
        """Close a loop"""
        if self.active == self.eol:
            self.loops.pop()
        else:
            try:
                self.cmdp = self.loops[-1]
            except IndexError:
                raise Exception("unmatched close bracket ({})".format(self.cmdp))

    @staticmethod
    def load(self, file) -> Bytecode:
        pass

    @staticmethod
    def execute(bytecode: Bytecode, length: int = 256, size: int = 255, wrapping: int = True, eol: int = 0) -> Tape:
        """Execute bytecode"""
        # setup the environment
        env = BF(length, size, wrapping, eol)
        while env.cmdp < len(bytecode):
            cmd = bytecode[env.cmdp]
            print(env.tape)
            try:
                # run whatever command is specified
                env.CMDS[cmd]()
            except KeyError:
                # if the command is not found check to see if it's a loop
                raise Exception("unkown command ({})".format(i))
            env.cmdp += 1

        # make sure all loops are closed
        if len(env.loops) > 0:
            raise Exception("unmatched open bracket ({})".format(env.loops[-1]))

        # return the tape
        return env.tape

    @staticmethod
    def interpret(file: str, length: int = 256, size: int = 255, wrapping: bool = True, eol: int = 0) -> Tape:
        """Interpret given source file"""
        return BF.execute(BF.load(file), length, size, wrapping, eol)

    @staticmethod
    def dump(tape: Tape, file: str = "dump.txt") -> str:
        """Dump tape to file"""
        try:
            open(file, "w").write(str(tape))
        except (PermissionError, FileNotFoundError):
            pass
        return tape

def main():
    """Main function"""
    BF.dump(BF.execute(['+']), "dump.txt")

if __name__ == "__main__":
    main()
