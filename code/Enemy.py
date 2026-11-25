import pygame
from code.Const import ENTITY_SPEED, ENTITY_SHOT_DELAY, MIN_Y, MAX_Y
from code.EnemyShot import EnemyShot
from code.Entity import Entity
from code.Utils import load_frames


class Enemy(Entity):
    def __init__(self, name: str, position: tuple, direction: int = -1):
        super().__init__(name, position)
        self.direction = -1 if direction <= 0 else 1
        flip_x = self.direction < 0
        self.animations = self.__load_all_animations(flip_x=flip_x)
        self.state = 'Walk'
        self.frame_idx = 0.0
        self.surf = self.animations['Walk'][0]

        ground_y = max(MIN_Y, min(MAX_Y, position[1]))
        self.rect = self.surf.get_rect(midbottom=(position[0], ground_y))
        self.hitbox = pygame.Rect(0, 0, 22, 38)
        self.hitbox.midbottom = self.rect.midbottom

        self.shot_delay = ENTITY_SHOT_DELAY[self.name] // 2
        self.attack_timer = 0
        self.hurt_timer = 0
        self.dead_timer = 0
        self.is_dying = False

    def __load_all_animations(self, flip_x: bool) -> dict:
        return {
            'Idle': load_frames(f'{self.name}_Idle', flip_x=flip_x, scale=0.75),
            'Walk': load_frames(f'{self.name}_Walk', flip_x=flip_x, scale=0.75),
            'Attack': load_frames(f'{self.name}_Attack', flip_x=flip_x, scale=0.75),
            'Hurt': load_frames(f'{self.name}_Hurt', flip_x=flip_x, scale=0.75),
            'Dead': load_frames(f'{self.name}_Dead', flip_x=flip_x, scale=0.75),
        }

    def take_hit(self, damage: int, attacker_name: str):
        if self.is_dying:
            return
        self.health -= damage
        self.last_dmg = attacker_name
        if self.health <= 0:
            self.health = 0
            self.is_dying = True
            self.state = 'Dead'
            self.frame_idx = 0.0
            self.dead_timer = 14
        else:
            self.hurt_timer = 8
            self.state = 'Hurt'
            self.frame_idx = 0.0

    def move(self):
        if self.is_dying:
            frames = self.animations['Dead']
            if self.frame_idx < len(frames) - 1:
                self.frame_idx += 0.35
            self.surf = frames[int(self.frame_idx)]
            self.dead_timer -= 1
            return

        if self.hurt_timer > 0:
            self.hurt_timer -= 1
            new_state = 'Hurt'
        elif self.attack_timer > 0:
            self.attack_timer -= 1
            new_state = 'Attack'
        else:
            self.rect.x += ENTITY_SPEED[self.name] * self.direction
            new_state = 'Walk'

        self.hitbox.midbottom = self.rect.midbottom

        if new_state != self.state:
            self.state = new_state
            self.frame_idx = 0.0

        frames = self.animations[self.state]
        self.frame_idx = (self.frame_idx + 0.2) % len(frames)
        self.surf = frames[int(self.frame_idx)]

    def shoot(self):
        if self.is_dying:
            return None
        self.shot_delay -= 1
        if self.shot_delay <= 0:
            self.shot_delay = ENTITY_SHOT_DELAY[self.name]
            self.attack_timer = 16
            spawn_x = self.hitbox.left - 8 if self.direction == -1 else self.hitbox.right + 8
            return EnemyShot(
                name=f'{self.name}Shot',
                position=(spawn_x, self.hitbox.centery - 2),
                sheet_name=f'{self.name}_Charge',
                direction=self.direction
            )
        return None