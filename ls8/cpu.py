"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0 # program counter
        self.register = [0] * 8
        self.ram = [0] * 8

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()
    
    def ram_read(self, value):
        return self.ram[value]

    def ram_write(self, address, value):
        return self.ram[address] = value

    def run(self):
        """Run the CPU."""

        # load program into memory
        self.load()

        # initialize variables for easy call distinction below
        LDI = 0b10000010
        PRN = 0b01000111
        HLT = 0b00000001
        IR = self.pc

        operand_a = self.ram_read(IR + 1)
        operand_b = self.ram_read(IR + 2)

        running = True

        while running:
            # execute instructions
            
            if self.ram[IR] == LDI:
                # set value of operand_b into operand_a
                self.ram_write(operand_a, operand_b)
                # increase IR by 3
                IR += 3
            
            elif self.ram[IR] == PRN:
                # print and increment
                print(f"Printing: {self.ram[self.ram[IR + 1]]}")
                IR += 2

            # elif self.ram[IR] == HLT:
            #     running = False
            #     sys.exit(1)
            
            # else:
            #     print(f"Error: Unknown command: {command}")
            #     sys.exit(1)