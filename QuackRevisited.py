# Quack Game Revisited

import pygame
import itertools

# Game Status Variable Track
global_status = {
    "process": {
        "run": True
    },
    "player": {
        "pos": [0, 0],
        "speed": 5,
        "sprite_lib": {
            "steady": pygame.transform.scale(pygame.image.load('assets/char/char_steady.png'), (37, 46)),
            "moving": itertools.cycle(
                [pygame.transform.scale(pygame.image.load('assets/char/char_walk_phase1.png'), (37, 46)),
                 pygame.transform.scale(pygame.image.load('assets/char/char_walk_phase2.png'), (37, 46))]),
            "flying": pygame.transform.scale(pygame.image.load('assets/char/char_flying.png'), (37, 46))
        },
        "orientation": 0 #0 = Leste, 1 = Oeste
    },
    "gamestate": {
        "is_paused": False,
        "menu_state": 0,
        "is_playing": False,
        "play_phase": {
            "id": 0,
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


# Função para checkar os eventos de input
def EventChecking():
    keys = pygame.key.get_pressed()
    if pygame.event.get(pygame.QUIT):
        global_status["process"]["run"] = False
        print("Force Quit. (Code 0)")
        exit(-1)
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        global_status["player"]["pos"][0] -= global_status["player"]["speed"]
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        global_status["player"]["pos"][0] += global_status["player"]["speed"]


# Função para entender a fase do jogo e chamar as respectivas funções
def DisplayRender():
    window.fill((0, 0, 0))
    if global_status["gamestate"]["is_paused"]:
        MenuDraw()
    else:
        CharacterDraw()


def CharacterDraw():
    window.blit(global_status["player"]["sprite_lib"]["steady"],
                (global_status["player"]["pos"][0], global_status["player"]["pos"][1]))


def MenuDraw():
    pass


def MainLoop():
    clock = pygame.time.Clock()
    while global_status["process"]["run"]:
        clock.tick(65)
        EventChecking()
        DisplayRender()
        pygame.display.update()


pygame.init()
window = pygame.display.set_mode((1024, 640))
global_status["gamestate"]["is_playing"] = True
global_status["gamestate"]["is_paused"] = not global_status["gamestate"]["is_playing"]
MainLoop()
