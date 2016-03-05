# Load, render and simulate structured layouts of LED boards

import yaml

from OpenGL.GL import *
from board import Board

class Layout(object):

	def __init__(self, name):
		self.name = name

		with file("layouts/%s.yaml" % name) as config_file:
			self.config = yaml.load(config_file)

		# Set up boards
		self.boards = {}
		for board in self.config['boards']:
			self.boards[board['id']] = Board(board['type'], board['id'])

	def render(self):
		for board in self.config['boards']:
			glPushMatrix()
			glTranslatef(board['translate']['x'], board['translate']['y'], board['translate']['z'])
			glRotatef(board['rotate']['r'], 0, 0, 1)
			glRotatef(board['rotate']['p'], 1, 0, 0)
			glRotatef(board['rotate']['y'], 0, 1, 0)
			self.boards[board['id']].render()
			glPopMatrix()
