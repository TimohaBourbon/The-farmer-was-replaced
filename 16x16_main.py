from __builtins__ import *

#------------Start_from_0---------------------------------------------------------------------
while get_pos_x() != 0:
    move(East)

while get_pos_y() != 0:
    move(North)

#------------Cycle----------------------------------------------------------------------------
while True:
    cactus_ready = True
    cactus_swapped = False
    cactus_complete = True
    max_petals = 0
    best_x = None
    best_y = None
    pumpkin_id = None
    plant_type = None
    x_target = None
    y_target = None

    for y in range(16):
        for x in range(16):
            x_pos = get_pos_x()
            y_pos = get_pos_y()
            cell_type = (x_pos + y_pos) % 2
            ground_type = get_ground_type()

            #------------Pumpkin--------------------------------------------------------------
            if x_pos == 0 and y_pos == 0:
                pumpkin_id = measure()

            if x_pos == 5 and y_pos == 5:
                if pumpkin_id != None and measure() == pumpkin_id:
                    harvest()

            if x_pos <= 5 and y_pos <= 5:
                if ground_type != Grounds.Soil:
                    till()

                plant(Entities.Pumpkin)

            #------------Sunflower------------------------------------------------------------
            elif x_pos in [6, 7] and y_pos <= 5:

                if ground_type != Grounds.Soil:
                    till()
                petals = measure()

                if petals != None and petals > max_petals:
                    max_petals = petals
                    best_x = x_pos
                    best_y = y_pos
                plant(Entities.Sunflower)

            #------------Cactus---------------------------------------------------------------
            elif x_pos >= 8 and y_pos <= 7:

                if ground_type != Grounds.Soil:
                    till()

                plant(Entities.Cactus)
                cactus_size = measure()
                if cactus_size == None:
                    cactus_complete = False
                if x_pos < 15:
                    move(East)
                    neighbour_size = measure()
                    move(West)
                    if cactus_size != None and neighbour_size != None:
                        if cactus_size > neighbour_size:
                            swap(East)
                            cactus_swapped = True
                    else:
                        cactus_complete = False
                cactus_size = measure()
                if cactus_size == None:
                    cactus_complete = False
                if y_pos < 7:
                    move(North)
                    neighbour_size = measure()
                    move(South)
                    if cactus_size != None and neighbour_size != None:
                        if cactus_size > neighbour_size:
                            swap(North)
                            cactus_swapped = True
                    else:
                        cactus_complete = False

                if not can_harvest():
                    cactus_ready = False

            #------------Polyculture----------------------------------------------------------
            else:
                current_plant_x = get_pos_x()
                current_plant_y = get_pos_y()

                if can_harvest():
                    companion = get_companion()

                    if companion == None:
                        harvest()

                    else:
                        plant_type, (x_target, y_target) = companion

                        if y_target <= 5 or (y_target in [6, 7] and x_target >= 8):
                            pass

                        else:
                            while get_pos_x() != x_target:
                                move(East)

                            while get_pos_y() != y_target:
                                move(North)

                            target_entity = get_entity_type()

                            if target_entity == plant_type:
                                pass

                            else:
                                if target_entity != None:
                                    harvest()

                                if plant_type == Entities.Carrot:
                                    if get_ground_type() != Grounds.Soil:
                                        till()

                                else:
                                    if get_ground_type() == Grounds.Soil:
                                        till()

                                plant(plant_type)

                        while get_pos_x() != current_plant_x:
                            move(East)

                        while get_pos_y() != current_plant_y:
                            move(North)

                        harvest()

                #------------Base_polyculture_layout------------------------------------------
                if cell_type == 0:
                    if x_pos % 4 == 0:
                        if ground_type == Grounds.Soil:
                            till()

                    elif x_pos % 4 == 1:
                        if ground_type == Grounds.Soil:
                            till()

                        plant(Entities.Tree)

                    elif x_pos % 4 == 2:
                        if ground_type != Grounds.Soil:
                            till()

                        plant(Entities.Carrot)

                    elif x_pos % 4 == 3:
                        if ground_type == Grounds.Soil:
                            till()

                        plant(Entities.Bush)

                else:
                    if x_pos % 4 == 0:
                        if ground_type != Grounds.Soil:
                            till()

                        plant(Entities.Carrot)

                    elif x_pos % 4 == 1:
                        if ground_type == Grounds.Soil:
                            till()

                        plant(Entities.Bush)

                    elif x_pos % 4 == 2:
                        if ground_type == Grounds.Soil:
                            till()

                    elif x_pos % 4 == 3:
                        if ground_type == Grounds.Soil:
                            till()

                        plant(Entities.Tree)

            move(East)

        move(North)

    #------------------------Sunflower_harvest------------------------------------------------
    if best_x != None and best_y != None:
        while get_pos_x() != best_x:
            move(East)
        while get_pos_y() != best_y:
            move(North)

        if can_harvest():
            harvest()

    #------------------------Cactus_harvest---------------------------------------------------
    if not cactus_swapped and cactus_complete and cactus_ready:
        while get_pos_x() != 8:
            move(East)
        while get_pos_y() != 0:
            move(North)
        harvest()

    while get_pos_x() != 0:
        move(East)

    while get_pos_y() != 0:
        move(North)
