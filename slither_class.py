from base_class import *
import math
from tkinter import *

class slither_part(base):
	def __init__(self, options):
		super().__init__(options)
		self.color=options.color
		self.speed=0
		self.angle=0

	def give_speed(self, speed):
		self.speed=speed

	def update(self):
		self.x+=self.speed*math.cos(self.angle)
		self.y+=self.speed*math.sin(self.angle)

	def visible(self,other):
		super().visible(other)

	def draw(self, canvas):
		self.update()
		if()
