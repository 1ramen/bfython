"""Brainfuck interpreter"""
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
            return self.value.__str__()

        def inc(self) -> int:
            """Increment the cell"""
            if self.wrapping is True:
                # if the value has exceeded the maximum, reset it to zero
                self.value = self.value + 1 if self.value >= self.size else 0
            else:
                # clamp new value within bounds of [0, self.max]
                self.value = min(max(self.value + 1, 0), self.size)

            # return the new value
            return self.value

        def dec(self) -> int:
            """Decrement the cell"""
            if self.wrapping is True:
                # if the value has exceeded the maximum, reset it to zero
                self.value = self.value - 1 if self.value <= 0 else self.size
            else:
                # clamp new value within bounds of [0, self.max]
                self.value = min(max(self.value - 1, 0), self.size)

            # return the new value
            return self.value

        def out(self) -> chr:
            """Print the contents of the cell to the console"""
            print(self.__str__())
            return self.__str__()

        def inp(self) -> int:
            """Get input from the user"""
            try:
                # get user input as ASCII text and convert it to an int, clamping into the cell size
                self.value = min(max(ord(input()[0]), 0), self.size)
            # if the user input can't convert to integer, don't do anything
            except ValueError:
                pass

            # return the new value
            return self.value

    class Tape:
        """Brainf**k tape"""
        def __init__(self, length: int, size: int, wrapping: bool):
            # memory
            self.memory = [BF.Cell(size, wrapping)] * length
            # pointer to active cell
            self._pointer = BF.Cell(length, wrapping)

        @property
        def pointer(self) -> int:
            """Get pointer value"""
            return self._pointer.value

        @property
        def active(self) -> int:
            """Get active cell"""
            return self.memory[self.pointer]

        def __str__(self) -> int:
            return self.memory.__str__()

        def right(self) -> int:
            """Increment the pointer"""
            return self._pointer.inc()

        def left(self) -> int:
            """Decrement the pointer"""
            return self._pointer.dec()

        def inc(self) -> int:
            """Increment active cell"""
            return self.active.inc()

        def dec(self) -> int:
            """Decrement active cell"""
            return self.active.dec()

        def out(self) -> chr:
            """Print out active cell"""
            return self.active.out()

        def inp(self) -> int:
            """Get new cell value from user"""
            return self.active.inp()

    class Bytecode(list):
        """Alias for list"""
        pass

    def __init__(self, length: int = 256, size: int = 255, wrapping: bool = True):
        # whether to overflow/underflow values
        self.wrapping = wrapping
        # the number of cells
        self.length = length
        # max cell value
        self.size = size
        # initialize the memory tape
        self.tape = BF.Tape(self.length, self.size, self.wrapping)

    def __str__(self):
        return self.tape.__str__()

    def right(self) -> int:
        """Increment pointer"""
        return self.tape.right()

    def left(self) -> int:
        """Decrement pointer"""
        return self.tape.left()

    def inc(self) -> int:
        """Increment active cell"""
        return self.tape.inc()

    def dec(self) -> int:
        """Decrement active cell"""
        return self.tape.dec()

    def out(self) -> chr:
        """Print out active cell"""
        return self.tape.out()

    def inp(self) -> int:
        """Get new cell value from user"""
        return self.tape.inp()

    @staticmethod
    def load(source: str) -> BF.Bytecode:
        """Convert file to bytecode"""
        pass

    @staticmethod
    def execute(bytecode: BF.Bytecode,
                length: int = 256,
                size: int = 255,
                wrapping: int = True,
                eol: int = 0) -> BF.Tape:
        """Execute bytecode"""

    @staticmethod
    def interpret(source: str,
                  length: int = 256,
                  size: int = 255,
                  wrapping: int = True,
                  eol: int = 0) -> BF.Tape:
        """Interpret given source file"""
        return BF.execute(BF.load(source), length, size, wrapping, eol)

    @staticmethod
    def dump(tape: BF.Tape, file: str = "dump.txt") -> str:
        """Dump tape to file"""
        try:
            open(file, "w").write(tape.__str__())
        except (PermissionError, FileNotFoundError):
            pass
        return tape.__str__()

def main():
    pass

if __name__ == "__main__":
    main()
