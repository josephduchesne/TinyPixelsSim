import pygame, OpenGL
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

from layout import Layout
from renderer import Renderer

pygame.init()
pygame.display.set_mode((1000,1000), DOUBLEBUF|OPENGL)

layouts = ['grid_4', 'cube_6', 't_6']
layout_offset = 0

def load_layout(offset, layouts):
	layout = Layout(layouts[layout_offset % len(layouts)])
	scale = layout.config['scale']
	return layout, scale
layout, scale = load_layout(layout_offset, layouts)

pitch = yaw = 0.0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == MOUSEBUTTONDOWN:
        	if event.button == 4:
        		scale *= 1.2
        		print scale
        	elif event.button == 5:
        		scale /= 1.2
        		print scale
        if event.type == pygame.KEYUP:
        	if event.key == pygame.K_RIGHT:
        		layout_offset += 1
        		layout, scale = load_layout(layout_offset, layouts)
        	if event.key == pygame.K_LEFT:
        		layout_offset -= 1
        		layout, scale = load_layout(layout_offset, layouts)

    if pygame.mouse.get_pressed()[0]:
    	dx, dy = pygame.mouse.get_rel()
    	pitch += dy/4.0
    	yaw += dx/4.0
    else:
    	pygame.mouse.get_rel()

    Renderer.camera(pitch, yaw, scale)

    layout.render()

    pygame.display.flip()
    pygame.time.wait(50)