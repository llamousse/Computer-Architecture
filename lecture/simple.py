# LECTURE DAY 4
import sys
​
PRINT_BEEJ     = 1  # 0000 0001
HALT           = 2  # 0000 0010
PRINT_NUM      = 3
SAVE           = 4  # Saves a value to a registers
PRINT_REGISTER = 5
ADD            = 6
PUSH           = 7
POP            = 8
​
​
memory = [0] * 32
registers = [0] * 8
​
​
SP = 7
​
​
pc = 0
running = True
​
​
​
def load_memory(filename):
​
    try:
        address = 0
        with open(filename) as f:
            for line in f:
                # Ignore comments
                comment_split = line.split("#")
                num = comment_split[0].strip()
​
                if num == "":
                    continue  # Ignore blank lines
​
                value = int(num)   # Base 10, but ls-8 is base 2
​
                memory[address] = value
                address += 1
​
    except FileNotFoundError:
        print(f"{sys.argv[0]}: {filename} not found")
        sys.exit(2)
​
​
if len(sys.argv) != 2:
    print("Usage: file.py filename", file=sys.stderr)
    sys.exit(1)
​
load_memory(sys.argv[1])
​
while running:
    # Execute instructions in memory
    # print(memory)
    # print(registers)
​
    command = memory[pc]
​
    if command == PRINT_BEEJ:
        print("Beej!")
        pc += 1
​
    elif command == PRINT_NUM:
        num = memory[pc+1]
        print(num)
        pc += 2
​
    elif command == HALT:
        running = False
        pc += 1
​
    elif command == SAVE:
        num = memory[pc + 1]
        reg = memory[pc + 2]
        registers[reg] = num
        pc += 3
​
    elif command == ADD:
        reg_a = memory[pc + 1]
        reg_b = memory[pc + 2]
        registers[reg_a] += registers[reg_b]
        pc += 3
​
    elif command == PRINT_REGISTER:
        reg = memory[pc + 1]
        print(registers[reg])
        pc += 2
​
    elif command == PUSH:
        reg = memory[pc + 1]
        val = registers[reg]
        # Decrement the SP.
        registers[SP] -= 1
        # Copy the value in the given register to the address pointed to by SP.
        memory[registers[SP]] = val
        # Increment PC by 2
        pc += 2
​
    elif command == POP:
        reg = memory[pc + 1]
        # Copy the value from the address pointed to by SP to the given register.
        val = memory[registers[SP]]
        registers[reg] = val
        # Increment SP.
        registers[SP] += 1
        # Increment PC by 2
        pc += 2
    
    elif command == CALL:
        print(f"CALLING SR AT ADDRESS {subroutine_address % 256}")
        # the address of the ***instruction*** _directly after_ `CALL` is pushed onto the stack.
        # this allows us to return to where we left off when the subroutine finishes executing.
        val = pc + 2
        registers[SP] -= 1
        memory[registers[SP]] = val

        # the PC is set to the address stored in the given register.
        reg = memory[pc + 1]
        subroutine_address = registers[reg] 
        
        # we jump to that location in RAM and execute the first instruction in the subroutine. 
        # the PC can move forward or backwards from its current location.
        pc = subroutine_address
        # pass

    elif command == RET:
        # return from subroutine.
        # pop the value from the top of the stack and store it in the `PC`
        return_address = registers[SP]
        print(f"RETURNING TO ADDRESS {return_address % 256}")
        pc = memory[return_address]
        # increment the SP by 1
        registers[SP] += 1
        # pass
​
​
    else:
        print(f"Error: Unknown command: {command}")
        sys.exit(1)