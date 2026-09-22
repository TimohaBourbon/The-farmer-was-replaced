from __builtins__ import *

clear()

change_hat(Hats.Dinosaur_Hat)

while True:
    if can_move(North):
        move(North)
    else:
        break