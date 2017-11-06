# TODO Implement basic Brainf**k environment

class bfenv:
    def __init__(self):
        """Setup the environment"""
        # Define the memory for the environment
        self.mem = [0] * 256
        # Setup variables
        self._max = 255
        self.pointer = 0

    def move(self, value):
        """Adjust the pointer"""
        self.pointer += value
        # Make sure the pointer is in the range of the data set
        if self.pointer > len(self.mem):
            raise Exception("Pointer out of range!")

    def add(self, value):
        """Adjust the current cell"""
        self.mem[self.pointer] += value
        if self.mem[self.pointer] > self._max:
            raise Exception("Overflow! @ cell {0:02x}".format(self.pointer))
