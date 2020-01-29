import sys

# python3 file.py filename

if len(sys.argv) != 2:
    print("Usage: file.py filename", file=sys.stderr)
    sys.exit(1)

try:
    with open(sys.argv[1]) as f:
        commands = []
        for line in f:
            # ignore comments
            comment_split = line.strip().split("#")

            # val = comment_split[0]
            # print(val)

            num = comment_split[0]

            if num == "":
                continue # ignore blank lines

            x = int(num, 2)
            print(f"{x:08b}: {x:d}")
            commands.append(x)

except FileNotFoundError:
    print(f"{sys.argv[0]}: {sys.argv[1]} not found")
    sys.exit(2)