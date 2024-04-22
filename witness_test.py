import sys
import os
# from pynput import keyboard

CLEAR = "\033[2J"
ORIGIN = "\033[H"


def move_cursor_right():
	sys.stdout.write("\033[1C")


# def on_press(key: keyboard.Key):
# 	if key == keyboard.Key.right:
# 		move_cursor_right()
#
#
# listener = keyboard.Listener(
# 	on_press=on_press
# )

sys.stdout.write(CLEAR + ORIGIN)

# █▓▒░ comment ░▒▓█

sys.stdout.write("░░░░░░░░░░░░░░░░░░░░░░░░░░░░")
sys.stdout.flush()

while True:
	print(os.read(0, 1))

# listener.start()
# while True:
# 	pass
