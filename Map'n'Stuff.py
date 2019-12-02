# Quack Scene Addon

import pygame

class Scene:
	class map(object):
		def __init__(self):
			pass
	def add(name):
		def decorator(function):
			pass
		return decorator
lol = 0
for _ in range(1024*200):
    if _ == lol + 32:
        lol += 32
    x[_] = lol
lol = 0
for _ in range(840):
    if _ == lol + 32:
        lol += 32
    y[_] = lol
	
def main_loop():
	pygame.init()

	clock = pygame.time.Clock()
	window = pygame.display.set_mode((1024, 640))
	img = pygame.transform.scale(pygame.image.load('assets/object/grass_block.png'), (64, 64))
	type="grass_block"
	while True:
		clock.tick(60)
		window.fill((0, 0, 0))
		window.blit(img, (x[pygame.mouse.get_pos()[0]], y[pygame.mouse.get_pos()[1]]))
		pygame.display.update()
		keys = pygame.key.get_pressed()
		if keys[pygame.K_1]: img,type = pygame.transform.scale(pygame.image.load('assets/object/grass_block.png'), (64, 64)), "grass_block"
		if keys[pygame.K_2]: img,type = pygame.transform.scale(pygame.image.load('assets/object/flag_lgbt.png'), (512, 512)), "flag"
		if keys[pygame.K_3]: img,type = pygame.transform.scale(pygame.image.load('assets/object/foliage_1.png'), (81, 81)), "foliage_1"
		if keys[pygame.K_4]: img,type = pygame.transform.scale(pygame.image.load('assets/object/foliage_2.png'), (88, 88)), "foliage_2"
main_loop()