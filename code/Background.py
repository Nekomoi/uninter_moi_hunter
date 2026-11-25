import pygame
from code.Const import WIN_WIDTH, WIN_HEIGHT
from code.Entity import Entity
from code.Utils import resource_path


class Background(Entity):
    def __init__(self, name: str, position: tuple, speed: int = 0):
        super().__init__(name, position)
        self.speed = speed
        raw = pygame.image.load(resource_path(f'assets/{name}.png')).convert_alpha()
        self.surf = pygame.transform.scale(raw, (WIN_WIDTH, WIN_HEIGHT))
        self.rect = self.surf.get_rect(topleft=position)

    def move(self):
        # Cenário estático: não se move
        pass