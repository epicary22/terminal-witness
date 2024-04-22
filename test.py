import sys

# clear the screen
sys.stdout.write("\033[2J")
# put the cursor at (0, 0)
sys.stdout.write("\033[H")
# flush the output
sys.stdout.flush()

# read in a line
my_line = sys.stdin.readline()
for i in range(52, 87):
	# turn the text purple
	sys.stdout.write(f"\033[38;5;{i}m")
	# put the cursor at some position
	sys.stdout.write(f"\033[{i - 52};{i - 52}H")
	# print out my line
	sys.stdout.write(my_line)
# turn the text back to normal
sys.stdout.write("\033[0m")
sys.stdin.tell()