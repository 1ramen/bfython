"""Environment for running brainf**k code in"""
class Cell:
    """Individual storage unit for a tape"""
    def __init__(self, size: int, wrapping: bool):
        self.size = size
        self.wrapping = wrapping
        self.value = 0

    def __str__(self):
        return '[{}]'.format(self.value)

    def clamp(self, value):
        """Clamp a value into the cell's bounds"""
        return min(max(value, 0), self.size)

    def increment(self):
        """Increment cell value"""
        if self.wrapping:
            self.value = 0 if self.value + 1 > self.size else self.value + 1
        else:
            self.value = self.clamp(self.value + 1)

    def decrement(self):
        """Decrement cell value"""
        if self.wrapping:
            self.value = self.size if self.value - 1 < 0 else self.value - 1
        else:
            self.value = self.clamp(self.value - 1)

    def input(self):
        """Set the cell value to user input"""
        from IO.getch import getch
        self.value = self.clamp(getch())

    def output(self):
        """Print the current cell value"""
        from termcolor import colored
        print(colored(chr(self.value), 'blue'))

class Tape:
    """Memory for brainf**k environment"""
    def __init__(self, length: int, size: int, wrapping: bool):
        self.length = length
        self.size = size
        self.wrapping = wrapping
        self._memory = [Cell(self.size, self.wrapping) for e in range(self.length)]
        self._pointer = Cell(self.length, self.wrapping)

    def __str__(self):
        return ''.join(str(e) for e in self._memory)

    @property
    def active(self):
        return self._memory[self._pointer.value]

    def increment_pointer(self):
        self._pointer.increment()

    def decrement_pointer(self):
        self._pointer.decrement()

class Environment:
    def __init__(self, length: int, size: int, wrapping: bool, end_of_loop: int):
        self.length = length
        self.size = size
        self.wrapping = wrapping
        self.tape = Tape(self.length, self.size, self.wrapping)
        self.end_of_loop = end_of_loop
        self.loop_stack = []
        self.cmdp = 0
        self.TOKENS = {
            '+': self.tape.active.increment,
            '-': self.tape.active.decrement,
            '.': self.tape.active.output,
            ',': self.tape.active.input,
            '>': self.tape.increment_pointer,
            '<': self.tape.decrement_pointer,
            '[': self.open_loop,
            ']': self.close_loop,
        }

    def open_loop(self):
        """Add the current command pointer to the loop stack"""
        self.loop_stack.append(self.cmdp)

    def close_loop(self):
        """Escape a loop or return to the beginning"""
        if self.tape.active.value == self.end_of_loop:
            self.loop_stack.pop()
        else:
            try:
                self.cmdp = self.loop_stack[-1]
            except IndexError:
                raise Exception("unmatched end of loop ({})".format(self.cmdp))

    def execute(self, source: str):
        while self.cmdp < len(source):
            token = source[self.cmdp]
            try:
                self.TOKENS[token]()
            except KeyError:
                raise Exception("unrecognized command ({})".format(self.cmdp))
            self.cmdp += 1