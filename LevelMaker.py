import itertools
import json
import threading

import pygame

pygame.init()
global_status = {
    "running": True,
    "paused": False,
}
threads = {
    "tostart": [],
    "started": [],
}
clock = pygame.time.Clock()


class Thread_Handler:
    def new_thread(self):
        threads['tostart'].append(threading.Thread(target=self))

    def start_threads(self=None):
        for thread in threads["tostart"]:
            thread.start()
        threads["tostart"] = []


y = {}
x = {}
lol = 0
for _ in range(1024):
    if _ == lol + 32:
        lol += 32
    x[_] = lol
lol = 0
for _ in range(640):
    if _ == lol + 32:
        lol += 32
    y[_] = lol


def ticko():
    while True:
        globals()['tick'] = int(input("tick_rate> "))


colors = [i for i in range(80) if i % 2 == 0]
id = 80
for i in range(80):
    id -= 1
    if id % 2 == 0:
        colors.append(id)
colors = itertools.cycle(colors)


def draw_limits():
    pow = 0

    color = next(colors)
    # print(color)
    for _ in range(32):
        pow += 32
        pygame.draw.line(window, (color, color, color), (pow, 0), (pow, 640))

    pow = 0
    for _ in range(20):
        pow += 32
        pygame.draw.line(window, (color, color, color), (0, pow), (1024, pow))

saved_blocks = []

def to_json():
    top = {"objects": []}
    for block in saved_blocks:
        top['objects'].append({"type": block[3], "location": [block[1],block[2]]})
    with open('dump.json', 'w') as f:
        f.write(json.dumps(top, sort_keys=True, indent=4))
        f.close()
def draw_blocks():
    if len(saved_blocks) == 0: return
    for block in saved_blocks:
        window.blit(block[0], (block[1], block[2]))
    to_json()

def main_loop():
    img = pygame.transform.scale(pygame.image.load('assets/object/grass_block.png'), (64, 64))
    type="grass_block"
    while global_status['running']:
        clock.tick(tick)
        # print('tick')
        window.fill((0, 0, 0))
        draw_limits()
        draw_blocks()
        # print(pygame.mouse.get_pos())
        window.blit(img, (x[pygame.mouse.get_pos()[0]], y[pygame.mouse.get_pos()[1]]))
        pygame.display.update()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_1]: img,type = pygame.transform.scale(pygame.image.load('assets/object/grass_block.png'), (64, 64)), "grass_block"
        if keys[pygame.K_2]: img,type = pygame.transform.scale(pygame.image.load('assets/object/flag_lgbt.png'), (512, 512)), "flag"
        if keys[pygame.K_3]: img,type = pygame.transform.scale(pygame.image.load('assets/object/foliage_1.png'), (81, 81)), "foliage_1"
        if keys[pygame.K_4]: img,type = pygame.transform.scale(pygame.image.load('assets/object/foliage_2.png'), (88, 88)), "foliage_2"
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                saved_blocks.append([img, x[pygame.mouse.get_pos()[0]], y[pygame.mouse.get_pos()[1]], type])
            # check if the event is the X button

            if event.type == pygame.QUIT:
                # if it is quit the game
                pygame.quit()
                exit(0)


def start():
    global window
    window = pygame.display.set_mode((1024, 640))
    global tick
    tick = 20
    threading.Thread(target=ticko).start()
    main_loop()


start()
