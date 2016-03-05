import pygame
import os
 
import OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *

textures = {}

class Renderer(object):

	@staticmethod
	def load_image(image):
		global textures

		# If the texture is not loaded, load it into the cache
		if image not in textures:

		    textureSurface = pygame.image.load(image)
		 
		    textureData = pygame.image.tostring(textureSurface, "RGBA", 1)
		 
		    width = textureSurface.get_width()
		    height = textureSurface.get_height()
		 
		    texture = glGenTextures(1)
		    glBindTexture(GL_TEXTURE_2D, texture)
		    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
		    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
		    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA,
		        GL_UNSIGNED_BYTE, textureData)
		    textures[image] = {'texture': texture, 'width': width, 'height': height}
	 
	    # Return cached texture
		return textures[image]['texture'], textures[image]['width'], textures[image]['height']


	@staticmethod
	def textured_quad(texture, w=1.0, h=1.0):
		glEnable(GL_TEXTURE_2D)
		glBindTexture(GL_TEXTURE_2D, texture)
		glColor3f(1.0, 1.0, 1.0)

		glBegin(GL_QUADS)
		glTexCoord2f(0,0)
		glVertex3f(-w/2,-h/2,0)
		glTexCoord2f(0,1)
		glVertex3f(-w/2,h/2,0)
		glTexCoord2f(1,1)
		glVertex3f(w/2,h/2,0)
		glTexCoord2f(1,0)
		glVertex3f(w/2,-h/2,0)
		glEnd()

	@staticmethod
	def quad(color, w=1.0, h=1.0):
		glDisable(GL_TEXTURE_2D)

		glBegin(GL_QUADS)
		glColor3f(color['r'], color['g'], color['b'])
		glVertex3f(-w/2,-h/2,0)
		glVertex3f(-w/2,h/2,0)
		glVertex3f(w/2,h/2,0)
		glVertex3f(w/2,-h/2,0)
		glEnd()


	@staticmethod
	def camera(pitch, yaw, scale):
		glLoadIdentity()
		gluPerspective(45, 1, 0.05, 200)

		glTranslatef(0,0,-100)
		glRotatef(pitch, 1.0, 0.0, 0.0)
		glRotatef(yaw, 0.0, 1.0, 0.0)
		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
		glEnable(GL_DEPTH_TEST)

		glScalef(scale, scale, scale)