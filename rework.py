import pygame

character = {
    "pos": {
        "x": 0,
        "y": 0,
    },
    "dimensions": {
        "height": 50,
        "length": 50,
    },
    "sprites": {
        "images": [pygame.image.load('assets/char/char_walk_phase1.png'),
                   pygame.image.load('assets/char/char_walk_phase2.png')],
        "current": pygame.image.load('assets/char/char_walk_phase1.png'),
    }
}
global_status = {
    ""
}
