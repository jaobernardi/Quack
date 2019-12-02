# Quack Game Revisited

import pygame
import itertools
import threading
from random import randint
from time import sleep as wait
from win32api import GetSystemMetrics
from levelmanager import Levels



# Game Status Variable Track
global_status = {
	"process": {
		"run": True
	},
	"player": {
		"pos": [0, 0],
		"max_sprintspeed": 9,
		"max_normalspeed": 3,
		"max_speed": 5,
		"speed": 1,
		"speed_thread": None,
		"increase_per_step": 0.50,
		"walking": False,
		"sprite_lib": {
			"steady": pygame.transform.scale(pygame.image.load('assets/char/char_steady.png'), (37, 46)), # Sprite parado
			"moving": {
					"thread": None,
					"iter": itertools.cycle(
					[pygame.transform.scale(pygame.image.load('assets/char/char_walk_phase1.png'), (37, 46)),
					pygame.transform.scale(pygame.image.load('assets/char/char_walk_phase2.png'), (37, 46))]),
					"actual": None
				},
			"flying": pygame.transform.scale(pygame.image.load('assets/char/char_flying.png'), (37, 46))
		},
		"orientation": 0 #0 = Leste, 1 = Oeste
	},
	"gamestate": {
		"is_paused": False,
		"menu_state": 0,
		"is_playing": False,
		"id": Levels.get_all()[0]["Map"]()
	},
	"settings": {
		"display": {
			"size": [1024, 640],
			"fps": 60,
			"fullscreen": False
		},
		"gameplay": {
			"difficulty": 0
		}
	}
}


# Função para checkar os eventos de input
def KeyWork():		
	keys = pygame.key.get_pressed()
	if keys[pygame.K_F11]:
		global_status["settings"]["display"]["fullscreen"] = not global_status["settings"]["display"]["fullscreen"]
		if global_status["settings"]["display"]["fullscreen"]:
			window = pygame.display.set_mode((GetSystemMetrics(0), GetSystemMetrics(1)), pygame.FULLSCREEN)
			global_status["settings"]["display"]["size"] = [GetSystemMetrics(0), GetSystemMetrics(1)]
		else:
			global_status["settings"]["display"]["size"] = [1024, 640]
			window = pygame.display.set_mode((global_status["settings"]["display"]["size"][0], global_status["settings"]["display"]["size"][1]), pygame.RESIZABLE)
	if global_status["player"]["walking"] and not (keys[pygame.K_RIGHT] or keys[pygame.K_d]):
		global_status["player"]["walking"] = False
	if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
		global_status["player"]["max_speed"] = global_status["player"]["max_sprintspeed"]
	if keys[pygame.K_LEFT] or keys[pygame.K_a]:
		global_status["player"]["pos"][0] -= global_status["player"]["speed"]
		global_status["player"]["orientation"] = 1
		global_status["player"]["walking"] = True
	if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
		global_status["player"]["pos"][0] += global_status["player"]["speed"]
		global_status["player"]["orientation"] = 0
		global_status["player"]["walking"] = True

	if global_status["player"]["max_speed"] != global_status["player"]["max_normalspeed"] and not (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]):
		global_status["player"]["max_speed"] = global_status["player"]["max_normalspeed"]


# Função para entender a fase do jogo e chamar as respectivas funções
def DisplayRender():
	# Limpa a tela
	window.fill((0, 0, 0))
	# Verifica o status do Jogo
	DrawScene()
	if global_status["gamestate"]["is_paused"]:
		MenuDraw()
	CharacterDraw()
	

def DrawScene():
	level = global_status["gamestate"]["id"]
	line = len(level)
	y = 64
	x = 0
	for block in level[line-1][:64]:	
		if block[0] == 1:
			window.blit(Levels.get_block(1),(x, global_status["settings"]["display"]["size"][1]-y))
			#pygame.draw.rect(window, (randint(244,255), randint(244,255), randint(244,255)), pygame.Rect((x, global_status["settings"]["display"]["size"][1]-y), (y, y)))
		x += 64

def CharacterDraw():
	# Define o sprite
	if global_status["player"]["walking"]:
		_sprite = global_status["player"]["sprite_lib"]["moving"]["actual"]
	else:
		_sprite = global_status["player"]["sprite_lib"]["steady"]
	# Checa a Orientação.
	if global_status["player"]["orientation"] == 0:
		# Aplica as mudanças necessárias 
		_sprite = pygame.transform.flip(
		_sprite,
		180,
		0
		)
	
	# Renderiza o player
	window.blit(_sprite,
				(global_status["player"]["pos"][0], global_status["player"]["pos"][1]))


				
def Sprite_Thread():
	while global_status["process"]["run"]:
		global_status["player"]["sprite_lib"]["moving"]["actual"] = next(global_status["player"]["sprite_lib"]["moving"]["iter"])
		wait(0.5/int(global_status["player"]["speed"]))
		#print(0.5/int(global_status["player"]["speed"]))
		#print("new sprite")
#

def Speed_Thread():
	while global_status["process"]["run"]:
		if global_status["player"]["walking"]:
			if global_status["player"]["speed"] < global_status["player"]["max_speed"]:
				wait(0.03)
				global_status["player"]["speed"] += global_status["player"]["increase_per_step"]
		elif global_status["player"]["speed"] != 1:
			global_status["player"]["speed"] = 1
		

def MenuDraw():
	pass
	
def Quit():
	while True:    
		pygame.event.pump()
		event=pygame.event.wait()
		if event.type==pygame.QUIT:
			global_status["process"]["run"] = False
			print("Force Quit. (Code 0)")
			exit(-1)
			
	

def MainLoop():
	clock = pygame.time.Clock()
	while global_status["process"]["run"]:
		clock.tick(65)
		
		resize_event = pygame.event.get(pygame.VIDEORESIZE)
		if resize_event:
			#global_status["settings"]["display"]["size"] = [resize_event[0].w, resize_event[0].h]
			#window = pygame.display.set_mode((resize_event[0].w, resize_event[0].h), pygame.RESIZABLE)
			pass
		KeyWork()
		DisplayRender()
		pygame.display.update()

		

pygame.init()
window = pygame.display.set_mode((1024, 640), pygame.RESIZABLE)
pygame.display.set_caption("Quack!")
global_status["gamestate"]["is_playing"] = True
global_status["gamestate"]["is_paused"] = not global_status["gamestate"]["is_playing"]
global_status["player"]["speed_thread"] = threading.Thread(target=Speed_Thread, daemon=True)
global_status["player"]["sprite_lib"]["moving"]["thread"] = threading.Thread(target=Sprite_Thread, daemon=True)
global_status["player"]["sprite_lib"]["moving"]["thread"].start()
global_status["player"]["speed_thread"].start()
threading.Thread(target=Quit, daemon=True).start()
try:
	MainLoop()
except KeyboardInterrupt:
	global_status["process"]["run"] = False
	print("Force Quit. (Code 0)")
	exit(-1)
