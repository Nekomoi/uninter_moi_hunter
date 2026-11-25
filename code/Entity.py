from abc import ABC, abstractmethod
import pygame
from code.Const import ENTITY_HEALTH, ENTITY_DAMAGE, ENTITY_SCORE


class Entity(ABC):
    def __init__(self, name: str, position: tuple):
        self.name = name
        self.surf: pygame.Surface = pygame.Surface((1, 1), pygame.SRCALPHA)
        self.rect: pygame.Rect = self.surf.get_rect(topleft=position)
        self.health = ENTITY_HEALTH.get(self.name, 1)
        self.damage = ENTITY_DAMAGE.get(self.name, 0)
        self.score = ENTITY_SCORE.get(self.name, 0)
        self.last_dmg = 'None'

    @abstractmethod
    def move(self):
        pass