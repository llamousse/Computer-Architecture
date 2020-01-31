"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0 # program counter
        self.register = [0] * 8
        self.ram = [0] * 256
        self.flag = [0] * 3 # flag for CMP (LT, GT, E)

    def load(self):
        """Load a program into memory."""
        
        address = 0
        program = []

        if len(sys.argv) != 2:
            print("Usage: file.py filename", file=sys.stderr)
            sys.exit(1)

        try:
            # open file
            with open(sys.argv[1]) as f:
                for line in f:
                    # ignore comments and spaces
                    comment_split = line.strip().split("#")
                    num = comment_split[0]
        
                    if num == "":
                        continue  # ignore blank lines
        
                    # integer type            
                    x = int(num, 2)
        
                    # load all parts into program
                    program.append(x)
        
        except FileNotFoundError:
            print(f"{sys.argv[0]}: {sys.argv[1]} not found")
            sys.exit(2)

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
            self.fl,
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
        self.ram[address] = value

    def run(self):
        """Run the CPU."""

        # load program into memory
        self.load()

        # initialize variables for easy call distinction below
        LDI = 0b10000010
        PRN = 0b01000111
        HLT = 0b00000001
        MUL = 0b10100010
        PUSH = 0b01000101
        POP = 0b01000110
        CALL = 0b01010000
        RET = 0b00010001
        ADD = 0b10100000
        CMP = 0b10100111
        JMP = 0b01010110
        JEQ = 0b01010101
        JNE = 0b01010110

        IR = self.pc
        SP = 243

        running = True

        while running:
            # execute instructions
            operand_a = self.ram_read(IR + 1)
            operand_b = self.ram_read(IR + 2)

            if self.ram[IR] == LDI:
                # set value of operand_b into operand_a
                self.ram_write(operand_a, operand_b)
                # increase IR by 3
                IR += 3
            
            elif self.ram[IR] == PRN:
                # print and increment
                print(f"Printing: {self.ram[self.ram[IR + 1]]}")
                IR += 2

            elif self.ram[IR] == MUL:
                val = self.ram_read(operand_a) * self.ram_read(operand_b)
                print(f"MUL: {self.ram_read(operand_a)} * {self.ram_read(operand_b)}")
                self.ram_write(operand_a, val)
                IR += 3
            
            elif self.ram[IR] == PUSH:
                # decrement SP
                SP -= 1
                # copy value in the given register to the address pointed to
                # by SP
                item = self.ram_read(operand_a)
                self.ram_write(SP, item)
                # increment IR by 2
                IR += 2

            
            elif self.ram[IR] == POP:
                # pop value at the top of the stack into given register
                item = self.ram_read(SP)
                # copy value from address pointed to by SP
                self.ram_write(operand_a, item)
                # increment SP
                SP += 1
                # increment IR by 2
                IR += 2

            elif self.ram[IR] == CALL:
                SP -= 1
                # write address of SP = IR
                self.ram_write(SP, IR)
                # set IR to RAM value of register operand_a
                IR = self.ram_read(operand_a)

            elif self.ram[IR] == RET:
                # set instruction register to the ram value of 
                # SP (stack pointer) incr by 2
                IR = self.ram_read(SP) + 2

            elif self.ram[IR] == ADD:
                # add value of two registers: operand_a + operand_b
                total_value = self.ram_read(operand_a) + self.ram_read(operand_b)
                # store result in registerA: operand_a
                self.ram_write(operand_a, total_value)
                IR += 3
            
            elif self.ram[IR] == CMP:
                # compare values in two registers
                # if values are equal, set 'E' equal flag to 1
                # otherwise, set it to 0
                if self.ram_read(operand_a) == self.ram_read(operand_b):
                    self.flag[0] = 0    # 3 = Less Than flag
                    self.flag[1] = 0    # 4 = Greater Than flag
                    self.flag[2] = 1    # 5 = Equal flag
                
                # regA > regB, set Greater-Than 'G' flag to 1
                # otherwise set it to 0
                elif self.ram_read(operand_a) > self.ram_read(operand_b):
                    self.flag[0] = 0
                    self.flag[1] = 1
                    self.flag[2] = 0

                # if regA < regB, set Less-Than 'L' flag to 1
                # otherwise, set it to 0
                elif self.ram_read(operand_a) < self.ram_read(operand_b):
                    self.flag[0] = 1
                    self.flag[1] = 0
                    self.flag[2] = 0
                
                # increase IR by 3
                IR += 3
            
            elif self.ram[IR] == JMP:
                # if 'E' flag is clear (false, 0) - jump to address stored
                # in given register
                if self.flag[2] == 0:
                    IR = self.ram_read(operand_a)
                else:
                    IR += 2

            elif self.ram[IR] == JEQ:
                # if equal flag == true, jump to address stored in register
                if self.flag[2] == 1:
                    IR = self.ram_read(operand_a)
                else:
                    IR += 2

            elif self.ram[IR] == JNE:
                # if E flag is clear/false, jump to address stored in 
                # the given register
                if self.flag[2] == 0:
                    IR = self.ram_read(operand_a)
                else:
                    IR += 2

            elif self.ram[IR] == HLT:
                running = False
                print(f"HALT! No more running - end")
            
            else:
                print(f"Error: Unknown command")
                IR += 1