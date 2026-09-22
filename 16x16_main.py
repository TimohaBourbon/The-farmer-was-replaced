from __builtins__ import *

WORLD_SIZE = 16


#------------Movement------------------------------------------------------------------------
def move_to(target_x, target_y):
    current_x = get_pos_x()

    east_distance = (target_x - current_x) % WORLD_SIZE
    west_distance = (current_x - target_x) % WORLD_SIZE

    if east_distance <= west_distance:
        for i in range(east_distance):
            move(East)
    else:
        for i in range(west_distance):
            move(West)


    current_y = get_pos_y()

    north_distance = (target_y - current_y) % WORLD_SIZE
    south_distance = (current_y - target_y) % WORLD_SIZE

    if north_distance <= south_distance:
        for i in range(north_distance):
            move(North)
    else:
        for i in range(south_distance):
            move(South)


#------------Pumpkin_Drone-------------------------------------------------------------------
def pumpkin_worker():

    while True:
        move_to(0, 0)

        pumpkin_id = measure()

        for y in range(6):
            for x in range(6):
                move_to(x, y)

                if x == 5 and y == 5:
                    if pumpkin_id != None and measure() == pumpkin_id:
                        harvest()

                if get_ground_type() != Grounds.Soil:
                    till()

                plant(Entities.Pumpkin)


#------------Sunflower_Drone-----------------------------------------------------------------
def sunflower_worker():

    while True:
        max_petals = 0
        best_x = None
        best_y = None

        for y in range(6):
            for x in range(6, 8):
                move_to(x, y)

                if get_ground_type() != Grounds.Soil:
                    till()

                petals = measure()

                if petals != None and petals > max_petals:
                    max_petals = petals
                    best_x = x
                    best_y = y

                plant(Entities.Sunflower)

        if best_x != None and best_y != None:
            move_to(best_x, best_y)

            if can_harvest():
                harvest()


#------------Cactus_Drone--------------------------------------------------------------------
def cactus_worker():

    while True:
        cactus_ready = True
        cactus_swapped = False
        cactus_complete = True

        for y in range(8):
            for x in range(8, 16):
                move_to(x, y)

                if get_ground_type() != Grounds.Soil:
                    till()

                plant(Entities.Cactus)

                cactus_size = measure()

                if cactus_size == None:
                    cactus_complete = False


                if x < 15:
                    neighbour_size = measure(East)

                    if cactus_size != None and neighbour_size != None:
                        if cactus_size > neighbour_size:
                            swap(East)
                            cactus_swapped = True
                    else:
                        cactus_complete = False


                cactus_size = measure()

                if cactus_size == None:
                    cactus_complete = False


                if y < 7:
                    neighbour_size = measure(North)

                    if cactus_size != None and neighbour_size != None:
                        if cactus_size > neighbour_size:
                            swap(North)
                            cactus_swapped = True
                    else:
                        cactus_complete = False


                if not can_harvest():
                    cactus_ready = False


        if not cactus_swapped and cactus_complete and cactus_ready:
            move_to(8, 0)
            harvest()


#------------Polyculture_Drone---------------------------------------------------------------
def polyculture_worker():

    while True:

        for y in range(6, 16):

            if y < 8:
                row_width = 8
            else:
                row_width = 16


            for x in range(row_width):
                move_to(x, y)

                x_pos = get_pos_x()
                y_pos = get_pos_y()

                cell_type = (x_pos + y_pos) % 2
                ground_type = get_ground_type()

                current_plant_x = x_pos
                current_plant_y = y_pos


                #------------Companion--------------------------------------------------------
                if can_harvest():

                    companion = get_companion()

                    if companion == None:
                        harvest()

                    else:
                        plant_type, (x_target, y_target) = companion


                        # Don't touch Pumpkin / Sunflower / Cactus zones
                        if y_target <= 5 or (y_target in [6, 7] and x_target >= 8):
                            pass

                        else:
                            move_to(x_target, y_target)

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


                        move_to(current_plant_x, current_plant_y)

                        harvest()


                #------------Base_Polyculture_Layout-----------------------------------------
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


                #------------Fertilizer------------------------------------------------------
                if get_entity_type() != None:
                    if not can_harvest():
                        if num_items(Items.Fertilizer) > 0:
                            use_item(Items.Fertilizer)


#------------Start---------------------------------------------------------------------------
move_to(0, 0)

if max_drones() >= 4:

    spawn_drone(pumpkin_worker)
    spawn_drone(sunflower_worker)
    spawn_drone(cactus_worker)
    polyculture_worker()

else:
    quick_print("At least 4 drones are required.")