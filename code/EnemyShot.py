from code.Const import ENTITY_SPEED
from code.Entity import Entity
from code.Utils import load_frames


class EnemyShot(Entity):
    def __init__(self, name: str, position: tuple, sheet_name: str, direction: int = -1):
        super().__init__(name, position)
        self.direction = -1 if direction <= 0 else 1
        flip_x = self.direction < 0
        self.frames = load_frames(sheet_name, flip_x=flip_x, scale=0.7)
        self.frame_idx = 0.0
        self.surf = self.frames[0]
        self.rect = self.surf.get_rect(center=position)

    def move(self):
        self.rect.centerx += ENTITY_SPEED[self.name] * self.direction
        self.frame_idx = (self.frame_idx + 0.4) % len(self.frames)
        self.surf = self.frames[int(self.frame_idx)]