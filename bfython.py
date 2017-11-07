# TODO Implement basic Brainf**k environment

import * from getch

class Bfython:
    # define some aliases to values for bytecode execution
    INC,DEC,NCP,DCP,RD,WRT,OLP,CLP = 0,1,2,3,4,5,6,7
    # define a dict for converting to bytecode
    bcdict = {
        '+': INC
        '-': DEC
        '>': NCP
        '<': DCP
        '.': RD
        ',': WRT
        '[': OLP
        ']': CLP
    }
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

    def incp(self):
        """Increments pointer"""
        self.move(1)

    def decp(self):
        """Decrements pointer"""
        self.move(-1)

    def add(self, value):
        """Adjust the current cell"""
        self.mem[self.pointer] += value
        # Make sure the cell doesn't overflow
        if self.mem[self.pointer] > self._max:
            raise Exception("Overflow! @ cell {0:02x}".format(self.pointer))

    def inc(self):
        """Increment current cell"""
        self.add(1)

    def dec(self):
        """Decrement current cell"""
        self.add(-1)

    def read(self):
        """Reads console and set current cell"""
        print(chr(self.mem[self.pointer]))

    def write(self):
        """Reads char from console and sets current cell to its int value"""
        self.mem[self.pointer] = ord(_Getch())

    def load(self, source):
        """Runs a .bf file"""
        self.bytecode = []
        # loop through all the lines in a source file
        for line in open(source, "r"):
            # remove all whitespace
            line.translate(dict.fromkeys(map(ord, whitespace)))
            # loop through all the characters in the line
            for char in line:
                if char == ';':
                    break
                else:
                    # add this command to the bytecode
                    try:
                        self.bytecode += bcdict[char]
                    except:
                        raise Exception("Unrecognized command character!")

    def execute(self):
        for i in range(0, len(self.bytecode)):
            if self.bytecode[i] == INC:
                self.add(1)
            elif self.bytecode[i] == DEC:
                self.add(-1)
            elif self.bytecode[i] == NCP:
                self.move(1)
            elif self.bytecode[i] == DCP:
                self.move(-1)
            elif self.bytecode[i] = RD:
                self.read()
            elif self.bytecode[i] = WRT:
                self.write()