from itertools import combinations
class grass_block:
    def __init__(self):
        self.height = 64
        self.length = 64
        self.plataform = True
        self.plataforms = list(combinations(range(64), 2))
        self.assets = 'assets/objects/grass_block.png'

    def __str__(self):
        return f"<grass_block object height={self.height}, length={self.length}, plataform={self.plataform}, plataform_places={self.plataforms}>"
