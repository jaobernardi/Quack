# Quack Game Revisited

import pygame
import itertools
import threading
from math import floor
from random import randint
from time import sleep as wait
from levelmanager import Levels
from win32api import GetSystemMetrics



# Game Status Variable Track
global_status = {
	"process": {
		"run": True
	},
	"player": {
		"tile": None,
		"offset": 0,
		"pos": [0, 0],
		"max_sprintspeed": 9,
		"max_normalspeed": 4.5,
		"max_speed": 5,
		"fall_speed": 0,
		"maxfall_speed": 6,
		"speed": 1,
		"speed_thread": None,
		"increase_per_step": 0.50,
		"walking": False,
		"falling": False,
		"sprite_lib": {
			"steady": pygame.transform.scale(pygame.image.load('assets/char/char_steady.png'), (37, 46)), # Sprite parado
			"flying": pygame.transform.scale(pygame.image.load('assets/char/char_flying.png'), (37, 46)), # Sprite Voando
			"moving": {
					"thread": None,
					"iter": itertools.cycle(
					[pygame.transform.scale(pygame.image.load('assets/char/char_walk_phase1.png'), (37, 46)),
					pygame.transform.scale(pygame.image.load('assets/char/char_walk_phase2.png'), (37, 46))]),
					"actual": None
				},
		},
		"orientation": 0 #0 = Leste, 1 = Oeste
	},
	"gamestate": {
		"is_paused": False,
		"menu_state": 0,
		"is_playing": False,
		"id": Levels.get_all()[0]["Map"]()
	},
	"physics": {
		"tiles": []	
	},
	"assets": {
		"grass_block": pygame.transform.scale(pygame.image.load('assets/object/grass_block.png'), (64, 64)),
		"grass_block2": pygame.transform.scale(pygame.image.load('assets/object/grass_block2.png'), (64, 64)),
		"dirt_block": pygame.transform.scale(pygame.image.load('assets/object/dirt_block.png'), (64, 64)),
		"foliage": pygame.transform.scale(pygame.image.load('assets/object/foliage_1.png'), (128, 128))
	},
	"settings": {
		"draw_bound": False,
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
	if keys[pygame.K_x]:
		global_status["settings"]["draw_bound"] = True
	else:
		global_status["settings"]["draw_bound"] = False
	if global_status["player"]["walking"] and not (keys[pygame.K_RIGHT] or keys[pygame.K_d]):
		global_status["player"]["walking"] = False
	if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
		global_status["player"]["max_speed"] = global_status["player"]["max_sprintspeed"]
	if keys[pygame.K_LEFT] or keys[pygame.K_a]:#global_status["player"]["offset"] += global_status["player"]["speed"]
		if global_status["player"]["pos"][0] < 100:			
			global_status["player"]["offset"] += global_status["player"]["speed"]
		else:
			global_status["player"]["pos"][0] -= global_status["player"]["speed"]
		global_status["player"]["orientation"] = 1
		global_status["player"]["walking"] = True
	if keys[pygame.K_RIGHT] or keys[pygame.K_d]:#global_status["player"]["offset"] -= global_status["player"]["speed"]
		if global_status["player"]["pos"][0] > global_status["settings"]["display"]["size"][0] - 100:
			
			global_status["player"]["offset"] -= global_status["player"]["speed"]
		else:
			global_status["player"]["pos"][0] += global_status["player"]["speed"]
		global_status["player"]["orientation"] = 0
		global_status["player"]["walking"] = True

	if global_status["player"]["max_speed"] != global_status["player"]["max_normalspeed"] and not (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]):
		global_status["player"]["max_speed"] = global_status["player"]["max_normalspeed"]


# Função para entender a fase do jogo e chamar as respectivas funções
def DisplayRender():
	# Limpa a tela
	window.fill((0, 0, 0))
	later_render = DrawScene()
	CharacterDraw()
	
	#-- Finalizar renderizção de objetos 
	for item in later_render:
		window.blit(item["Assets"], item["pos"])
	#--
	if global_status["gamestate"]["is_paused"]:
		MenuDraw()
	

def DrawScene():
	level = global_status["gamestate"]["id"]
	y = global_status["settings"]["display"]["size"][1]-110
	offset = global_status["player"]["offset"]
	window.fill((96,178,200))
	later_render = []
	global_status["physics"]["tiles"] = []
	for layer in level:
		x = offset
		for tile in layer:
			if not tile in ["0", "4", "2", "3"]:
				window.blit(global_status["assets"][Levels.get_block(tile)], (x, y+48))
				global_status["physics"]["tiles"].append(pygame.Rect(x,y+48,64,64))
			if tile in ["2", "3"]:
				window.blit(global_status["assets"][Levels.get_block(tile)], (x, y+48))
				global_status["physics"]["tiles"].append(pygame.Rect(x,y+56,64,58))
			if tile == "4":
				global_status["physics"]["tiles"].append(pygame.Rect(x,y,128,128))
				later_render.append({"Assets": global_status["assets"][Levels.get_block(tile)], "pos": (x, y)})
			x += 64
		y -= 64
	if global_status["settings"]["draw_bound"]:
		for rectum in global_status["physics"]["tiles"]:
			pygame.draw.rect(window, (255,0,0), rectum, 1)
	return later_render


def CollisionTest(objecto, tobetested):
	found = []
	for tile in tobetested:
		if objecto.colliderect(tile):
			return True
	

def CharPhysics():
	y = global_status["player"]["pos"][1]+global_status["player"]["fall_speed"]
	rd = floor((global_status["player"]["fall_speed"] ** 2) * 0.5)
	hrp = pygame.Rect(global_status["player"]["pos"][0],y,37, 46)
	if global_status["settings"]["draw_bound"]: pygame.draw.rect(window, (0,255,0), hrp, 1)
	collisions = CollisionTest(hrp, global_status["physics"]["tiles"])
	collisions2 = CollisionTest(global_status["player"]["tile"], global_status["physics"]["tiles"])
	if (collisions and not collisions2) or (collisions and collisions2):
		rd = 0	
		global_status["player"]["fall_speed"] = 0
		global_status["player"]["falling"] = False
	elif global_status["player"]["fall_speed"] < global_status["player"]["maxfall_speed"]:
		global_status["player"]["fall_speed"] += 0.3
		if rd > 1.5:
			global_status["player"]["falling"] = True
	global_status["player"]["pos"][1] += rd


def CharacterDraw():
	# Define o sprite
	if global_status["player"]["walking"] and not global_status["player"]["falling"]:
		_sprite = global_status["player"]["sprite_lib"]["moving"]["actual"]
	elif not global_status["player"]["falling"]:
		_sprite = global_status["player"]["sprite_lib"]["steady"]
	else:
		_sprite = global_status["player"]["sprite_lib"]["flying"]
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
	global_status["player"]["tile"] = (pygame.Rect(global_status["player"]["pos"][0],global_status["player"]["pos"][1],37, 46))
	if global_status["settings"]["draw_bound"]: pygame.draw.rect(window, (255,0,0), global_status["player"]["tile"], 1)
				
def Sprite_Thread():
	while global_status["process"]["run"]:
		global_status["player"]["sprite_lib"]["moving"]["actual"] = next(global_status["player"]["sprite_lib"]["moving"]["iter"])
		wait(0.8/int(global_status["player"]["speed"]))
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
		CharPhysics()
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