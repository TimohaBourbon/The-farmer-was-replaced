from __builtins__ import *

while True:
	for y in range(8):
		for x in range(8):
			x_pos = get_pos_x()
			ground_type = get_ground_type()
			entity_to_plant = None
			if can_harvest():
				harvest()

			if x_pos in [0, 1]:
				if ground_type == Grounds.Soil:
					till()
			
			elif x_pos in [2, 3]:
				entity_to_plant = Entities.Bush
				if ground_type == Grounds.Soil:
					till()

			elif x_pos in [4, 5]:
				entity_to_plant = Entities.Carrot
				if ground_type != Grounds.Soil:
					till()

			elif x_pos in [6, 7]:
				entity_to_plant = Entities.Pumpkin
				if ground_type != Grounds.Soil:
					till()

			if entity_to_plant != None:
				plant(entity_to_plant)
				
			move(East)
		move(North)