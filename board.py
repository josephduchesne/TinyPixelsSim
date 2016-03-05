# Load, render and simulate boards

import yaml

from renderer import Renderer
from OpenGL.GL import *
import colorsys

class Board(object):

	def __init__(self, name, id):
		self.id = id
		self.name = name

		with file("boards/%s.yaml" % name) as config_file:
			self.config = yaml.load(config_file)

		# Load textures
		self.front = Renderer.load_image("boards/"+self.config['front'])[0]
		self.back = Renderer.load_image("boards/"+self.config['back'])[0]



	def update(self, time_offset):
		self.colors = {}
		for i, led in enumerate(self.config['leds']):
			percent = ( i*1.0/len(self.config['leds']) - time_offset/4.0 ) % 1.0
			rgb = colorsys.hsv_to_rgb(percent, 1.0, 1.0)
			self.colors[led['id']] = {"r": rgb[0], "g": rgb[1], "b": rgb[2]}

	def render(self):

		# Render front
		glPushMatrix()
		glTranslatef(0,0, self.config['size']['thickness']/2.0)
		Renderer.textured_quad(self.front, self.config['size']['width'], self.config['size']['height'])
		glPopMatrix()

		# Render back
		glPushMatrix()
		glTranslatef(0,0, -self.config['size']['thickness']/2.0)
		glRotatef( 180.0, 0.0, 1.0, 0.0) # 180 degree spin around the vertical axis
		Renderer.textured_quad(self.back, self.config['size']['width'], self.config['size']['height'])
		glPopMatrix()

		# Render top
		glPushMatrix()
		glTranslatef(0, self.config['size']['height']/2.0, 0.0)
		glRotatef( 90.0, 1.0, 0.0, 0.0) # 90 degree spin around the horizontal axis
		Renderer.quad(self.config['color'], self.config['size']['width'], self.config['size']['thickness'])
		glPopMatrix()

		# Render bottom
		glPushMatrix()
		glTranslatef(0, -self.config['size']['height']/2.0, 0.0)
		glRotatef( 90.0, 1.0, 0.0, 0.0) # 90 degree spin around the horizontal axis
		Renderer.quad(self.config['color'], self.config['size']['width'], self.config['size']['thickness'])
		glPopMatrix()

		# Render left
		glPushMatrix()
		glTranslatef(-self.config['size']['width']/2., 0, 0)
		glRotatef( 90.0, 0.0, 1.0, 0.0) # 90 degree spin around the vertical axis
		Renderer.quad(self.config['color'], self.config['size']['thickness'], self.config['size']['height'])
		glPopMatrix()

		# Render right
		glPushMatrix()
		glTranslatef(self.config['size']['width']/2., 0, 0)
		glRotatef( 90.0, 0.0, 1.0, 0.0) # 90 degree spin around the vertical axis
		Renderer.quad(self.config['color'], self.config['size']['thickness'], self.config['size']['height'])
		glPopMatrix()

		# Render LEDs
		for led in self.config['leds']:
			self.render_led(led, self.colors[led['id']])

	def render_led(self, led, color):

		# as a very basic quad for now!
		glPushMatrix()
		glTranslatef(led['x'], led['y'], self.config['size']['thickness']/2.0 + 0.1)  # 0.1mm in front of front face
		Renderer.quad(color, led['w'], led['h'])
		glPopMatrix()