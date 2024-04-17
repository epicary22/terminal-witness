import sys

# clear the screen
sys.stdout.write("\033[2J")
# put the cursor at (0, 0)
sys.stdout.write("\033[H")
# flush the output
sys.stdout.flush()

# read in 5 characters
my_chars = sys.stdin.read(5)
# print out those 5 characters
sys.stdout.write(my_chars)
