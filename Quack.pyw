import itertools
import threading
from builtins import *
from math import floor
from time import sleep

import pygame

plataforms = [i for i in range(512)]
plataforms2 = [i + 512 for i in range(512)]
map_elements = {"plataforms": plataforms}
for i in plataforms:  # X            Y
    plataforms[i] = [plataforms[i], 500]
lan = 0
for i in plataforms2:  # X            Y
    plataforms.append([plataforms2[lan], 401])
    lan += 1
win = pygame.display.set_mode((1024, 600))

character = {
    "steady": pygame.transform.flip(pygame.transform.scale(pygame.image.load('assets/char/char_steady.png'), (37, 46)),
                                    180, 0),
    "steady_leste": pygame.transform.flip(
        pygame.transform.scale(pygame.image.load('assets/char/char_steady.png'), (37, 46)), 0, 0),
    "steady_oeste": pygame.transform.flip(
        pygame.transform.scale(pygame.image.load('assets/char/char_steady.png'), (37, 46)), 180, 0),
    "pos": {"x": 0, "y": 0}, "dimensions": {"length": 37, "height": 47.5},
    "def": {"speed": {"normal": 5, "boost": 4}},
    "state": {"gravity": True, "isJumping": False, "JumpCount": 10, "doubleJumpuble": False}, "cache": {},
    "sprints": {"list": [pygame.transform.scale(pygame.image.load('assets/char/char_walk_phase1.png'), (37, 46)),
                         pygame.transform.scale(pygame.image.load('assets/char/char_walk_phase2.png'), (37, 46))],
                "current": None},
}
global_status = {
    "paused": False,
    "running": True,
}
threads = {"sos": [], "running": []}


class Threads:
    def sos(self):
        thread = threading.Thread(target=self)
        thread.setName('SOS Thread')
        threads['sos'].append(thread)

    def sosstart(self=None):
        for thread in threads['sos']:
            thread.start()


# Gravity Check Function
def gravity_check(dist=None):
    if not character["state"]["gravity"]:
        return False
    for y_base in [i for i in range(600) if i > character["pos"]["y"] + character["dimensions"]["height"]]:
        # print([character["pos"]["x"], y_base])
        if [character["pos"]["x"], y_base] in plataforms:
            distance = [i for i in plataforms if i == [character["pos"]["x"], y_base]][0][1] - (
                    character["pos"]["y"] + character["dimensions"]["height"])
            if (distance > 0 and distance < 1):
                distance = 1
            if dist:
                return floor(distance)
            return True
    return False


# Character Movement Function
def character_jump():
    character["state"]["gravity"] = False
    character["state"]["isJumping"] = True
    if character["state"]["JumpCount"] >= 0:
        character["pos"]["y"] -= floor((character["state"]["JumpCount"] ** 2) * 0.3)
        character["state"]["JumpCount"] -= 1
    else:
        character["state"]["gravity"] = True
        character["state"]["isJumping"] = False
        character["state"]["JumpCount"] = character["cache"]["JumpCount"]


def character_move():
    keys = pygame.key.get_pressed()
    # Variables
    _vel = character["def"]["speed"]["normal"]

    # Clear Last Position
    gravity = gravity_check()

    # Gravity
    if gravity:
        dist = gravity_check(True)
        #        if gravity_check(True) > _vel + 2 + character["def"]["speed"]["boost"]:
        if _vel + character["def"]["speed"]["boost"] > dist:

            character["pos"]["y"] += dist
        else:
            character["pos"]["y"] += (_vel ** 2) * 0.5
    elif character["state"]["isJumping"]:
        character_jump()
    # Key Movements
    _walked = False
    if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
        _vel += character["def"]["speed"]["boost"]
    if ((keys[pygame.K_UP] or keys[pygame.K_SPACE]) and (character["pos"]["y"] - _vel > 0)):
        _walked = True
        if ((character["state"]["doubleJumpuble"] or character["state"]["gravity"]) and not gravity):
            #
            character["cache"]["JumpCount"] = character["state"]["JumpCount"]
            character_jump()
        # character["pos"]["y"] -= _vel
    if ((keys[pygame.K_DOWN] or keys[pygame.K_RCTRL]) and (
            character["pos"]["y"] + _vel + character["dimensions"]["height"] < 600)):
        character["pos"]["y"] += _vel
        _walked = True
    if ((keys[pygame.K_LEFT] or keys[pygame.K_s]) and (character["pos"]["x"] - _vel > 0)):
        _walked = True
        character["pos"]["x"] -= _vel
    if ((keys[pygame.K_RIGHT] or keys[pygame.K_w]) and (
            character["pos"]["x"] + _vel + character["dimensions"]["length"] < 1024)):
        character["pos"]["x"] += _vel
        _walked = True
    if not _walked:
        win.blit(character['steady'], (character["pos"]["x"], character["pos"]["y"]))
    else:
        win.blit(character["sprints"]['current'], (character["pos"]["x"], character["pos"]["y"]))


# noinspection PyMethodParameters
class menus:
    def pause():
        pygame.draw.rect(win, (190, 190, 190, 1), (0, 0, 60, 60))

    def unpause():
        pygame.draw.rect(win, (0, 0, 0), (0, 0, 60, 60))
        pygame.display.update()


def main_loop():
    threading.Thread(target=coiso).start()
    threading.Thread(target=coiso2).start()
    clock = pygame.time.Clock()
    while global_status["running"]:
        clock.tick(50)
        if pygame.event.get(pygame.QUIT):
            global_status["running"] = False
        win.fill((0, 0, 0))
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            global_status["paused"] = not (global_status["paused"])
            if not global_status["paused"]:
                menus.unpause()
            sleep(0.2)
        if not global_status["paused"]:
            character_move()
            for I in plataforms:
                pygame.draw.rect(win, (255, 0, 0), (I[0], I[1], 1, 1))
                pygame.draw.rect(win, (255, 0, 0), (I[0], I[1] + 1, 1, 1))
                pygame.draw.rect(win, (255, 0, 0), (I[0], I[1] + 2, 1, 1))
        else:
            menus.pause()
        pygame.display.update()
    pygame.quit()


def coiso():
    while True:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_s] or keys[pygame.K_LEFT]:
            character["steady"] = character["steady_leste"]
        elif keys[pygame.K_w] or keys[pygame.K_RIGHT]:
            character["steady"] = character["steady_oeste"]
        sleep(0.01)


def coiso2():
    _count = itertools.cycle(character["sprints"]["list"])
    while True:
        keys = pygame.key.get_pressed()
        if not keys[pygame.K_LSHIFT] or not keys[pygame.K_RSHIFT]:
            sleep(0.05)
        sleep(0.05)
        if character["steady"] != character["steady_leste"]:
            character["sprints"]["current"] = pygame.transform.flip(next(_count), 180, 0)
        else:
            character["sprints"]["current"] = next(_count)


pygame.init()
pygame.display.set_caption("Quack!")
pygame.display.toggle_fullscreen()

main_loop()
