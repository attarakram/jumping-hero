from csv import reader
from os import walk
import pygame

def import_folder(path):
	surface_list = []

	for _, __, image_files in walk(path):
		for image in image_files:
			full_path = path + '/' + image
			image_surf = pygame.image.load(full_path).convert_alpha()
			surface_list.append(image_surf)

	return surface_list

def import_csv_layout(path):
	terrain_map = []
	with open(path) as map:
		level = reader(map, delimiter = ',')
		for row in level:
			terrain_map.append(list(row))
		return terrain_map

def import_graphics(tilesize_x, tilesize_y, path):
	surface = pygame.image.load(path).convert_alpha()
	tile_num_x = int(surface.get_size()[0] /  tilesize_x)
	tile_num_y = int(surface.get_size()[1] / tilesize_y)

	graphics = []
	for row in range(tile_num_y):
		for col in range(tile_num_x):
			x = col * tilesize_x
			y = row * tilesize_y
			new_surf = pygame.Surface((tilesize_x, tilesize_y),flags = pygame.SRCALPHA)
			new_surf.blit(surface,(0,0),pygame.Rect(x, y, tilesize_x, tilesize_y))
			graphics.append(new_surf)

	return graphics