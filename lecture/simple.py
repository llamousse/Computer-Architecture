############# LECTURE DAY 3 ################
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
    print(memory)
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
​
​
    else:
        print(f"Error: Unknown command: {command}")
        sys.exit(1)

############ LECTURE DAY 2 #################
# import sys
# ​
# PRINT_BEEJ     = 1  # 0000 0001
# HALT           = 2  # 0000 0010
# PRINT_NUM      = 3
# SAVE           = 4  # Saves a value to a registers
# PRINT_REGISTER = 5
# ADD            = 6
# ​
# memory = [0] * 256
# registers = [0] * 8
# ​
# pc = 0
# running = True
# ​
# def load_memory(filename):
#     try:
#         address = 0
#         with open(filename) as f:
#             for line in f:
#                 # Ignore comments
#                 comment_split = line.split("#")
#                 num = comment_split[0].strip()
# ​
#                 if num == "":
#                     continue  # Ignore blank lines
# ​
#                 value = int(num)   # Base 10, but ls-8 is base 2
# ​
#                 memory[address] = value
#                 address += 1
# ​
#     except FileNotFoundError:
#         print(f"{sys.argv[0]}: {filename} not found")
#         sys.exit(2)
# ​
# if len(sys.argv) != 2:
#     print("Usage: file.py filename", file=sys.stderr)
#     sys.exit(1)
# ​
# load_memory(sys.argv[1])
# ​
# print(memory)
# ​
# while running:
#     # Execute instructions in memory
# ​
#     command = memory[pc]
# ​
#     if command == PRINT_BEEJ:
#         print("Beej!")
#         pc += 1
# ​
#     elif command == PRINT_NUM:
#         num = memory[pc+1]
#         print(num)
#         pc += 2
# ​
#     elif command == HALT:
#         running = False
#         pc += 1
# ​
#     elif command == SAVE:
#         num = memory[pc + 1]
#         reg = memory[pc + 2]
#         registers[reg] = num
#         pc += 3
# ​
#     elif command == ADD:
#         reg_a = memory[pc + 1]
#         reg_b = memory[pc + 2]
#         registers[reg_a] += registers[reg_b]
#         pc += 3
# ​
#     elif command == PRINT_REGISTER:
#         reg = memory[pc + 1]
#         print(registers[reg])
#         pc += 2
# ​
#     else:
#         print(f"Error: Unknown command: {command}")
#         sys.exit(1)


############### LECTURE DAY 1 ################
# import sys
# ​
# # op code - to make it human readable
# PRINT_BEEJ = 1  # 0000 0001
# HALT = 2  # 0000 0010
# PRINT_NUM = 3
# SAVE = 4  # Saves a value to a register
# PRINT_REGISTER = 5
# ADD = 6
# ​
# memory = [
#     PRINT_BEEJ,
#     SAVE,  # Saves the value 65 to register 2
#     65,
#     2,
#     SAVE,  # Saves the value 20 to register 3
#     20,
#     3,
#     ADD,  # ADD the values in r2 += r3
#     2,
#     3,
#     PRINT_REGISTER,  # Print the value in r2
#     2,
#     PRINT_BEEJ,
#     PRINT_BEEJ,
#     PRINT_BEEJ,
#     HALT,
# ]
# ​
# register = [0] * 8
# ​
# pc = 0 # program counter
# running = True
# ​
# while running:
#     # Execute instructions in memory
# ​
#     command = memory[pc]
#     ​
#     if command == PRINT_BEEJ:
#         print("Beej!")
#         pc += 1
#     ​
#     elif command == PRINT_NUM:
#         num = memory[pc+1]
#         print(num)
#         pc += 2
#     ​
#     elif command == HALT:
#         running = False
#         pc += 1
#     ​
#     elif command == SAVE:
#         num = memory[pc + 1]
#         reg = memory[pc + 2]
#         register[reg] = num
#         pc += 3
#     ​
#     elif command == ADD:
#         reg_a = memory[pc + 1]
#         reg_b = memory[pc + 2]
#         register[reg_a] += register[reg_b]
#         pc += 3
#     ​
#     elif command == PRINT_REGISTER:
#         reg = memory[pc + 1]
#         print(register[reg])
#         pc += 2
#     ​
#     else:
#         print(f"Error: Unknown command: {command}")
#         sys.exit(1)