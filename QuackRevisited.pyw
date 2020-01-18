# Quack Game Revisited by Jão and Bianca
import pygame
import itertools
import threading
from os import listdir
from math import floor
from random import randint
from time import sleep as wait
from time import time
from assets.levels.levels import Levels
from win32api import GetSystemMetrics

# Variavél de Status do Jogo

global_status = { # Status do Jogo em si
	'process': {'run': True},
	'cache': {"pauseclick_span": 0},
	'player': { # Status do Jogador
		'tile': None, # Rect do Jogador
		'offset': 0, # Posição relativa do Jogador em relação ao mapa - Câmera
		'pos': [0, 0], # Posição do Jogador
		'max_sprintspeed': 9,
		'max_normalspeed': 4.5,
		'max_speed': 5,
		'fall_speed': 0,
		'maxfall_speed': 6,
		'speed': 1,
		'speed_thread': None,
		'increase_per_step': 0.50,
		'walking': False, # Estado de movimentação X
		'falling': False, # Estado de movimentação -Y
		'sprite_lib': { # Sprites do Jogador
					   'steady': pygame.transform.scale(pygame.image.load('assets/char/char_steady.png'
					   ), (37, 46)),
					   'flying': pygame.transform.scale(pygame.image.load('assets/char/char_flying.png'
					   ), (37, 46)), 'moving': {'thread': None,
					   'iter': itertools.cycle([pygame.transform.scale(pygame.image.load('assets/char/char_walk_phase1.png'
					   ), (37, 46)),
					   pygame.transform.scale(pygame.image.load('assets/char/char_walk_phase2.png'
					   ), (37, 46))]), 'actual': None}},
		'orientation': 0, # Orientação do Jogador ( Leste e Oeste )
		},
	'menu': {
		'id': 0,
		'offset': 0,
		'state': 0
		},
	'gamestate': { # Estado da gameplay
		'is_paused': False,
		'is_playing': False,
		},
	'level': {
			'background_offset': 0,
			'levels': Levels.get_all(),
			'actual': None
		},
	'physics': { # Objetos do Mapa
		'stiles': [],
		'sstiles': []},
	'assets': { # Texturas
		'mmback': pygame.image.load('assets/ui/mmback.png'),
		'opaticy': pygame.image.load('assets/ui/opacity.png'),
		'font': 'assets/fonts/VCR_OSD_MONO.ttf',
		'font2': 'assets/fonts/Coder\'s Crux.ttf',
		'grass_block': pygame.transform.scale(pygame.image.load('assets/object/grass_block.png'
				), (64, 64)),
		'grass_block2': pygame.transform.scale(pygame.image.load('assets/object/grass_block2.png'
				), (64, 64)),
		'dirt_block': pygame.transform.scale(pygame.image.load('assets/object/dirt_block.png'
				), (64, 64)),
		'tree': pygame.transform.scale(pygame.image.load('assets/object/tree.png'
				), (128, 256)),
		'foliage': pygame.transform.scale(pygame.image.load('assets/object/foliage_1.png'
				), (128, 128)),
		},
	'settings': {'draw_bound': False, 'display': {'size': [1024, 640],
				 'fps': 60, 'fullscreen': False},
				 'gameplay': {'difficulty': 0}},
	}
# Função de administração do input das teclas


def KeyWork():
	keys = pygame.key.get_pressed()
	if keys[pygame.K_F11]:
		ToggleFullscreen()
	if global_status["gamestate"]["is_playing"]:
		if keys[pygame.K_ESCAPE] and (time() - global_status["cache"]["pauseclick_span"]) > 0.2:
			global_status["gamestate"]["is_paused"] = not global_status["gamestate"]["is_paused"]
			global_status["menu"]["id"] = 1
			global_status["cache"]["pauseclick_span"] = time()
		if not global_status["gamestate"]["is_paused"]:
			if keys[pygame.K_x]:
				global_status["settings"]["draw_bound"] = True
			else:
				global_status["settings"]["draw_bound"] = False
			
			if global_status["player"]["walking"] and not (keys[pygame.K_RIGHT] or keys[pygame.K_d]):
				global_status["player"]["walking"] = False
			if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
				global_status["player"]["max_speed"] = global_status["player"]["max_sprintspeed"]
				
			if keys[pygame.K_LEFT] or keys[pygame.K_s]:#global_status["player"]["offset"] += global_status["player"]["speed"]
				if global_status["player"]["pos"][0] < 100:
					global_status["player"]["offset"] += global_status["player"]["speed"]
					global_status["level"]["background_offset"] += global_status["player"]["speed"]
				else:
					global_status["player"]["pos"][0] -= global_status["player"]["speed"]
				global_status["player"]["orientation"] = 1
				global_status["player"]["walking"] = True
				
			elif keys[pygame.K_RIGHT] or keys[pygame.K_w]:#global_status["player"]["offset"] -= global_status["player"]["speed"]
				if global_status["player"]["pos"][0] > global_status["settings"]["display"]["size"][0] - 100:

					global_status["player"]["offset"] -= global_status["player"]["speed"]
					global_status["level"]["background_offset"] -= global_status["player"]["speed"]
				else:
					global_status["player"]["pos"][0] += global_status["player"]["speed"]
				global_status["player"]["orientation"] = 0
				global_status["player"]["walking"] = True

			if global_status["player"]["max_speed"] != global_status["player"]["max_normalspeed"] and not (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]):
				global_status["player"]["max_speed"] = global_status["player"]["max_normalspeed"]


# Função da Renderização do Jogo

def DisplayRender():
	# Limpa a tela
	window.fill((0, 0, 0))
	if global_status['gamestate']['is_playing']:
		# Renderiza o Background
		BackgroundDraw()
		# Recebe objetos de renderização tardia e renderiza o cenário.
		later_render = DrawScene()
		# Renderiza o Jogador
		CharacterDraw()
		# Renderização dos objetos tardios
		for item in later_render:
			window.blit(item['Assets'], item['pos'])
		if global_status['gamestate']['is_paused']:
			MenuDraw()		
	# Menus
	else:
		MenuDraw()
		
# Função dos Menus (em breve)
def ToggleFullscreen():
	global_status["settings"]["display"]["fullscreen"] = not global_status["settings"]["display"]["fullscreen"]
	if global_status["settings"]["display"]["fullscreen"]:
		global_status["player"]["pos"][1] += GetSystemMetrics(1)-global_status["settings"]["display"]["size"][1]
		window = pygame.display.set_mode((GetSystemMetrics(0), GetSystemMetrics(1)), pygame.FULLSCREEN)
		global_status["settings"]["display"]["size"] = [GetSystemMetrics(0), GetSystemMetrics(1)]
	else:
		global_status["player"]["pos"][1] += 640-global_status["settings"]["display"]["size"][1]
		global_status["settings"]["display"]["size"] = [1024, 640]
		window = pygame.display.set_mode((global_status["settings"]["display"]["size"][0], global_status["settings"]["display"]["size"][1]), pygame.RESIZABLE)
	if "back" in global_status["assets"]: global_status["assets"]["back"] = pygame.transform.scale(global_status["assets"]["back"], global_status['settings']['display']['size']).convert()
	global_status["assets"]["mmback"] = pygame.transform.scale(global_status["assets"]["mmback"], global_status['settings']['display']['size']).convert()
	global_status['assets']['opacity'] = global_status['assets']['opacity'] = pygame.transform.scale(pygame.image.load('assets/ui/opacity.png'), global_status["settings"]["display"]["size"])
	
def MenuDraw():
	# Background
	if global_status['menu']['id'] == 0:
		offset = global_status['menu']['offset']
		screen_size = global_status['settings']['display']['size'][0]
		a = pygame.mouse.get_pos()
		mouse_rect = pygame.Rect(a[0]-5, a[1]-5, 10, 10)
		y = 0
		if offset < 0:
			y += offset
			if y < 0:
				window.blit(global_status['assets']['mmback'], (y+screen_size,0))
			if y*-1 > screen_size:
				global_status['menu']['offset'] = 0 
		window.blit(global_status['assets']['mmback'], (y,0))
		global_status['menu']['offset'] -= 0.5
		
		# Buttons
		largeText = pygame.font.Font(global_status['assets']['font'],115)
		buttonText = pygame.font.Font(global_status['assets']['font2'],40)
		smallText = pygame.font.Font(global_status['assets']['font2'],33)
		mediumText = pygame.font.Font(global_status['assets']['font2'],40)
		mediumText.set_bold(True)
		buttons = []
		if global_status['menu']['state'] == 0:
			
			title = largeText.render('Quack', True, (255, 222, 65))
			text_rect = title.get_rect(center=(screen_size/2, global_status['settings']['display']['size'][1]/4*0.5))
			
			button = buttonText.render('Play', False, (255, 255, 255))
			b_rect = button.get_rect(center=(screen_size/2, global_status['settings']['display']['size'][1]/4*1.75))
			buttons.append([button, b_rect, 0])
			button = buttonText.render('Settings', False, (255, 255, 255))
			b_rect = button.get_rect(center=(screen_size/2, global_status['settings']['display']['size'][1]/4*2.25))
			buttons.append([button, b_rect, 1])
			button = buttonText.render('Quit', False, (255, 255, 255))
			b_rect = button.get_rect(center=(screen_size/2, global_status['settings']['display']['size'][1]/4*2.75))
			buttons.append([button, b_rect, 4])
			button = smallText.render('Version 0.3 Alpha', False, (255, 255, 255))
			b_rect = button.get_rect(center=(120, global_status['settings']['display']['size'][1]-10))
			buttons.append([button, b_rect, -1])
			window.blit(title, text_rect)
		else:
			button = mediumText.render('Settings', False, (255, 255, 255))
			b_rect = button.get_rect(center=(screen_size/2, global_status['settings']['display']['size'][1]/4))
			buttons.append([button, b_rect, 1])
			button = buttonText.render('Fullscreen', False, (255, 255, 255))
			b_rect = button.get_rect(center=(screen_size/4*1.5, global_status['settings']['display']['size'][1]/4*1.25))
			buttons.append([button, b_rect, 1])
			if global_status["settings"]["display"]["fullscreen"]:
				button = buttonText.render('[On]', False, (255, 255, 255))
			else:
				button = buttonText.render('[Off]', False, (255, 255, 255))
			b_rect = button.get_rect(center=(screen_size/4*2.5, global_status['settings']['display']['size'][1]/4*1.25))
			buttons.append([button, b_rect, 2])
			button = buttonText.render('Back', False, (255, 255, 255))
			b_rect = button.get_rect(center=(screen_size/2, global_status['settings']['display']['size'][1]/4*2.5))
			buttons.append([button, b_rect, 3])
		# Draw Buttons
		for button in buttons:
			window.blit(button[0], button[1])
			if button[1].colliderect(mouse_rect): 
				ev = pygame.event.get()
				for event in ev:
					if event.type == pygame.MOUSEBUTTONUP or event.type == pygame.MOUSEBUTTONDOWN:
						if button[2] == 0:
							LevelLoad("Testing Level")
							global_status['gamestate']['is_playing'] = True
						elif button[2] == 1:
							global_status['menu']['state'] = 1
						elif button[2] == 2:
							ToggleFullscreen()
						elif button[2] == 3:
							global_status['menu']['state'] = 0
						elif button[2] == 4:
							global_status['process']['run'] = False
	elif global_status['menu']['id'] == 1:
		window.blit(global_status['assets']['opacity'], (0,0))
		# Buttons, Mouse and Size Points
		screen_size = global_status['settings']['display']['size'][0]
		a = pygame.mouse.get_pos()
		mouse_rect = pygame.Rect(a[0]-5, a[1]-5, 10, 10)
		buttons = []
		
		# Fonts
		largeText = pygame.font.Font(global_status['assets']['font2'],40)
		buttonText = pygame.font.Font(global_status['assets']['font2'],33)
		smallText = pygame.font.Font(global_status['assets']['font2'],33)
		mediumText = pygame.font.Font(global_status['assets']['font2'],40)
		mediumText.set_bold(True)
		
		# Title
		title = largeText.render('Paused', True, (255, 255, 255))
		text_rect = title.get_rect(center=(100, 50))
		window.blit(title, text_rect)
		
		# Buttons
		button = buttonText.render('Quit', False, (255, 255, 255))
		b_rect = button.get_rect(center=(100, global_status['settings']['display']['size'][1]/4*2.75))
		buttons.append([button, b_rect, 0])
		
		# Button Handle
		for button in buttons:
			window.blit(button[0], button[1])
			if button[1].colliderect(mouse_rect): 
				ev = pygame.event.get()
				for event in ev:
					if event.type == pygame.MOUSEBUTTONUP or event.type == pygame.MOUSEBUTTONDOWN:
						if button[2] == 0:
							global_status['gamestate']['is_playing'] = False
							global_status['gamestate']['is_paused'] = False
							global_status['menu']['id'] = 0
	#pygame.draw.rect(window, (255, 0, 0), mouse_rect, 1)
	#print(offset, y)
# Função para renderização do Background do nivél
def BackgroundDraw():
# sorry jão do futuro. nem eu sei como que eu cheguei nesse código...
	offset = global_status['level']['background_offset']
	screen_size = global_status['settings']['display']['size'][0]
	y = 0
	if offset < 0:
		y += offset	
		if y < 0:
			window.blit(global_status['assets']['back'], (y+screen_size,0))
		if y*-1 > screen_size:
			global_status['level']['background_offset'] = 0 
	if offset > 0:
		y += offset	
		window.blit(global_status['assets']['back'], ((screen_size-offset)*-1,0))
		if y >= screen_size:
			global_status['level']['background_offset'] = 0
	window.blit(global_status['assets']['back'], (y,0))

# Função de Renderização e Interpretação de Nivél
def DrawScene():
	# Atribuir o nivél (á ser reformulado.)
	level = global_status['level']['actual']
	# Pegar o canto inferior esquerdo
	y = global_status['settings']['display']['size'][1] - 110
	# Pegar o Offset da câmera
	offset = global_status['player']['offset']
	# Variavél para objetos de renderização tardia
	later_render = []
	# Limpar objetos do ultimo Frame
	global_status['physics']['stiles'] = []
	# Level é igual à linha horizontal formada por blocos.
	for layer in level:
		x = offset
		# Tile significa uma entidade (bloco, objeto) em um Level.
		for tile in layer:
			# Identificação e tratamento dos tipos de bloco
			if not tile in ['0', '4', '2', '3', '5']:
				window.blit(global_status['assets'
							][Levels.get_block(tile)], (x, y + 48))
				global_status['physics']['stiles'].append(pygame.Rect(x,
						y + 48, 64, 64))
			elif tile in ['2', '3']:
				window.blit(global_status['assets'
							][Levels.get_block(tile)], (x, y + 48))
				global_status['physics']['stiles'].append(pygame.Rect(x,
						y + 56, 64, 58))
			elif tile == '5':
				global_status['physics']['sstiles'].append(pygame.Rect(x,
						y - 128, 128, 256))
				window.blit(global_status['assets'][Levels.get_block(tile)], (x, y - 128))
			elif tile == '4':
				global_status['physics']['sstiles'].append(pygame.Rect(x,
						y, 128, 128))
				later_render.append({'Assets': global_status['assets'
									][Levels.get_block(tile)],
									'pos': (x, y)})
			x += 64
		y -= 64
	# Debug: Modo de visualização de limites dos blocos.
	if global_status['settings']['draw_bound']:
		for rectum in global_status['physics']['stiles']:
			pygame.draw.rect(window, (255, 0, 0), rectum, 1)
	return later_render

# Função de teste de colisão

def CollisionTest(objecto, tobetested):
	found = []
	for tile in tobetested:
		if objecto.colliderect(tile):
			return True
# Função de Física ( Gravidade apenas, por ora. )

def CharPhysics():
	if global_status["gamestate"]["is_playing"]:
		# Aceleração do Jogador em direção -Y.
		y = global_status["player"]["pos"][1]+global_status["player"]["fall_speed"]
		aceleration = floor(global_status['player']['fall_speed'] ** 2 * 0.50)
		# Limite da previsão.
		preview_bound = pygame.Rect(global_status['player']['pos'][0] + 10, y, 7, 46)
		# Debug: Modo de visualização de limites dos blocos.
		if global_status['settings']['draw_bound']:
			pygame.draw.rect(window, (0, 255, 0), preview_bound, 1)
		# Testes de colisão da Previsão entre o mundo e do Jogador atual entre o mundo.
		c_pb = CollisionTest(preview_bound, global_status['physics']['stiles'])
		c_np = CollisionTest(global_status['player']['tile'],global_status['physics']['stiles'])
		# Decisão sobre se é possivél uma queda.
		if c_pb and not c_np or c_pb and c_np:
			# Cancelamento e nulificação da queda
			aceleration = 0
			global_status['player']['fall_speed'] = 0
			global_status['player']['falling'] = False
		elif global_status['player']['fall_speed'] < global_status['player']['maxfall_speed']:
			# Aceleração da queda e efetivação da queda.
			global_status['player']['fall_speed'] += 0.3
			if aceleration > 1.5:
				global_status['player']['falling'] = True
		global_status['player']['pos'][1] += aceleration
# Função de Renderização do Jogador

def CharacterDraw():
	# Definição do Sprite correto.
	if global_status['player']['walking'] and not global_status['player'
			]['falling']:
		_sprite = global_status['player']['sprite_lib']['moving'
				]['actual']
	elif not global_status['player']['falling']:
		_sprite = global_status['player']['sprite_lib']['steady']
	else:
		_sprite = global_status['player']['sprite_lib']['flying']
	# Correção da Orientação.
	if global_status['player']['orientation'] == 0:
		_sprite = pygame.transform.flip(_sprite, 180, 0)
	# Renderiza o player
	window.blit(_sprite, (global_status['player']['pos'][0],
				global_status['player']['pos'][1]))
	global_status['player']['tile'] = pygame.Rect(global_status['player'
			]['pos'][0], global_status['player']['pos'][1], 37, 46)
	# Debug: Modo de visualização de limites dos blocos.
	if global_status['settings']['draw_bound']:
		pygame.draw.rect(window, (255, 0, 0), global_status['player'
						 ]['tile'], 1)

# Função do Processo de Sprite.

def Sprite_Thread():
	while global_status['process']['run']:
		# Atualizar o Sprite
		global_status['player']['sprite_lib']['moving']['actual'] = \
			next(global_status['player']['sprite_lib']['moving']['iter'
				 ])
		wait(0.8 / int(global_status['player']['speed']))

# Função do Processo de Velocidade.

def Speed_Thread():
	while global_status['process']['run']:
		#  Verifica o status de movimento X.
		if global_status['player']['walking']:
			# Verifica a possibilidade de alteração de Velocidade
			if global_status['player']['speed'] < global_status['player'
					]['max_speed']:
				wait(0.03)
				# Altera a Velocidade
				global_status['player']['speed'] += \
					global_status['player']['increase_per_step']
		elif global_status['player']['speed'] != 1:
			# Reseta a Velocidade para 1, em prol da manteneção dos cálculos futuros.
			global_status['player']['speed'] = 1


# Função de Saida.

def Quit():
	while True:
		pygame.event.pump()
		event = pygame.event.wait()
		if event.type == pygame.QUIT or not global_status['process']['run']:
			global_status['process']['run'] = False
			print('Force Quit. (Code 0)')
			exit(-1)


def LevelLoad(name):
	for level in global_status['level']['levels']:
		if level["Name"] == name:
			global_status['level']['actual'] = level["Map"]()
			files = listdir(level['Assets'])
			for file in files:
				if file.endswith(".png") or file.endswith(".jpg"):
					#print(file.split(".")[0])
					global_status["assets"][file.split(".")[0]] = pygame.transform.scale(pygame.image.load(f"{level['Assets']}/{file}"), global_status['settings']['display']['size']).convert()
# Função do Loop Principal

def MainLoop():
	clock = pygame.time.Clock()
	#print("[@] Loading Testing Level")
	#LevelLoad("Testing Level")
	while global_status['process']['run']:
		clock.tick(70)
		resize_event = pygame.event.get(pygame.VIDEORESIZE)
		if resize_event:
			global_status["player"]["pos"][1] += resize_event[0].h-global_status["settings"]["display"]["size"][1]
			global_status["settings"]["display"]["size"] = [resize_event[0].w, resize_event[0].h]
			window = pygame.display.set_mode((resize_event[0].w, resize_event[0].h), pygame.RESIZABLE)
			if "back" in global_status["assets"]: global_status["assets"]["back"] = pygame.transform.scale(global_status["assets"]["back"], global_status['settings']['display']['size']).convert()
			global_status["assets"]["mmback"] = pygame.transform.scale(global_status["assets"]["mmback"], global_status['settings']['display']['size']).convert()
			global_status['assets']['opacity'] = global_status['assets']['opacity'] = pygame.transform.scale(pygame.image.load('assets/ui/opacity.png'), global_status["settings"]["display"]["size"])
			pass
		# Chama as funções principais
		DisplayRender()
		KeyWork()
		if not global_status["gamestate"]["is_paused"]:
			CharPhysics()
		# Atualiza o Frame
		pygame.display.update()
pygame.init()
pygame.font.init()
icon = pygame.transform.scale(pygame.image.load('icon.png'), (32, 32))
pygame.display.set_icon(icon)
window = pygame.display.set_mode((1024, 640), pygame.RESIZABLE)
pygame.display.set_caption('Quack!')
global_status['player']['speed_thread'] = \
	threading.Thread(target=Speed_Thread, daemon=True)
global_status['player']['sprite_lib']['moving']['thread'] = \
	threading.Thread(target=Sprite_Thread, daemon=True)
global_status['player']['sprite_lib']['moving']['thread'].start()
global_status['player']['speed_thread'].start()
threading.Thread(target=Quit, daemon=True).start()
global_status["assets"]["mmback"] = pygame.transform.scale(global_status["assets"]["mmback"], global_status['settings']['display']['size']).convert()
global_status['assets']['opacity'] = global_status['assets']['opacity'] = pygame.transform.scale(pygame.image.load('assets/ui/opacity.png'), global_status["settings"]["display"]["size"])
try:
	MainLoop()
except KeyboardInterrupt:
	global_status['process']['run'] = False
	print('Force Quit. (Code 0)')
	exit(-1)
