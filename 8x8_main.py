from __builtins__ import *

while get_pos_x() != 0:
    move(East)
while get_pos_y() != 0:
    move(North)

while True:
    pumpkin_id = None
    max_petals = 0
    best_x = None
    best_y = None
    for y in range (12):
        for x in range (12):
            x_pos = get_pos_x()
            y_pos = get_pos_y()
            ground_type = get_ground_type()
            cell_type = (x_pos + y_pos) % 2

            if x_pos == 4 and y_pos == 0:
                pumpkin_id = measure()

            if x_pos == 7 and y_pos == 3:
                second_pumpkin_id = measure()
                if second_pumpkin_id != None and second_pumpkin_id == pumpkin_id:
                    harvest()

            if x_pos in [0, 1, 2, 3, 8, 9, 10, 11]:
                if can_harvest():
                    harvest()

            if x_pos == 0:
                if ground_type == Grounds.Soil:
                    till()

            elif x_pos in [1, 2]:
                if ground_type == Grounds.Soil:
                    till()
                if cell_type == 0:
                    plant(Entities.Tree)
                else:
                    plant(Entities.Bush)

            elif x_pos == 3:
                if ground_type != Grounds.Soil:
                    till()
                plant(Entities.Carrot)

            elif x_pos in [4, 5, 6, 7]:
                if ground_type != Grounds.Soil:
                    till()
                if y_pos in [0, 1, 2, 3]:
                    plant(Entities.Pumpkin)
                else:
                    petals = measure()
                    if petals != None and petals > max_petals:
                        max_petals = petals
                        best_x = x_pos
                        best_y = y_pos
                    plant(Entities.Sunflower)

            move(East)
        move(North)
    if best_x != None and best_y != None:
        while get_pos_x() != best_x:
            move(East)
        while get_pos_y() != best_y:
            move(North)

        if can_harvest():
            harvest()