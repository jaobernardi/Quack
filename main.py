#Quack Game Revisited

import pygame
import threading
import time
from random import randint
import itertools

#Game Status Variable Track
global_status = {
	"process": {
		"run": True
		},
	"player": {
		"pos": [0, 0],
		"sprite_cache": {}
	},
	"gamestate": {
		"is_paused": False,
		"menu_state": 0,
		"is_playing": False,
		"play_phase": {
			"id": -1,
			"name": "DEBUG_PHASE"
		}
	},
	"settings": {
		"display": {
			"size": [1024, 640],
			"fps": 60
		},
		"gameplay": {
			"difficulty": 0
		}
	}
}
#Função para checkar os eventos de input
def EventChecking():
	if pygame.event.get(pygame.QUIT):
		global_status["process"]["run"] = False
		print("Force Quit. (Code 0)")
		exit(-1)
#Função para entender a fase do jogo e chamar as respectivas funções
def DisplayRender():
	window.fill((0, 0, 0))
	if global_status["gamestate"]["is_paused"]:
		MenuDraw()
def MenuDraw():
	
def MainLoop():
	clock = pygame.time.Clock()
	while global_status["process"]["run"]:
		clock.tick(65)
		EventChecking()
		DisplayRender()
		pygame.display.update()
pygame.init()
window = pygame.display.set_mode((1024, 640))
global_status["gamestate"]["is_playing"] = False
global_status["gamestate"]["is_paused"] = not global_status["gamestate"]["is_playing"]
MainLoop()