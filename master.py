## master.py
# This is the logic part of the whole project, it should intelligently arrange all the
# subroutines and classes.

import car
from shelf import Shelf

class Master:
	def __init__(self):
		## CONSTANTS

		self.all_item_dict = {
		1: 'red_block',
		2: 'green_block',
		3: 'blue_block',
		4: 'shuangwaiwai',
		5: 'yangleduo',
		6: 'wahaha',
		7: 'beer',
		8: 'red_bull',
		9: 'le_hu',
		10: 'tennis_ball'
		11: 'magic_cube'
		12: 'deluxe_milk'
		}

		self.car = car.Car()
		

		self.shelves = dict()
		for key in ['A', 'B', 'C', 'D']:
			slef.shelves[key] = Shelf()

	def main_loop(self):
		# car.move(1, 4) and turn around
		self.car.move(self.photo_spots['A'], (0, -1))
		# take a photo of the shelf D(to be proved viable)
		# for convenience, the car should stop when it turns round

		# take photo and map it to an array
		self.empty_shelf_array['D'] = car.take_photo('A')


		for shelf in self.shelf_list:
			while not self.shelves['A'].is_target_empty():
			# move around E and try to find the item for shelf D(tennis_ball, magic_cube, deluxe_milk)
		# put it to the right place
		# 
			pass

		move(4, 1)

		




if __name__ == '__main__':
	master = Master()
	master.main_loop()
