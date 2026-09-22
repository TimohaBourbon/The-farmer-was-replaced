from __builtins__ import *

while True:
    clear()

    plant(Entities.Bush)

    maze_size = get_world_size() * num_unlocked(Unlocks.Mazes)

    use_item(Items.Weird_Substance, maze_size)

    direction = North

    while True:
        if get_entity_type() == Entities.Treasure:
            harvest()
            break

        if direction == North:
            right = East
            left = West
            back = South


        elif direction == West:
            right = North
            left = South
            back = East

        elif direction == South:
            right = West
            left = East
            back = North


        else:
            right = South
            left = North
            back = West

        if can_move(right):
            direction = right
            move(direction)

        elif can_move(direction):
            move(direction)

        elif can_move(left):
            direction = left
            move(direction)

        else:
            direction = back
            move(direction)
