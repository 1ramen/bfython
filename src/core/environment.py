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
