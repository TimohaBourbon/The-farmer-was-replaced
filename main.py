from __builtins__ import *

while True:
	for y in range(6):
		for x in range(6):
			if can_harvest():
				harvest()

			#if get_pos_x() == 0 or get_pos_x() == 3:
				#pass
				
			if get_pos_x() == 0 or get_pos_x() == 1:
				if get_ground_type() == Grounds.Soil:
					till()
				plant(Entities.Bush)
			
			elif get_pos_x() == 2 or get_pos_x() == 3 or get_pos_x() == 4 or get_pos_x() == 5:
				if get_ground_type() != Grounds.Soil:
					till()
				plant(Entities.Carrot)
				
			move(East)
		move(North)