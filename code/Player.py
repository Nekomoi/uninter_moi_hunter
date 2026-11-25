import pygame
from code.Const import (
    ENTITY_SPEED, WIN_WIDTH, MIN_Y, MAX_Y,
    PLAYER_KEY_UP, PLAYER_KEY_DOWN, PLAYER_KEY_LEFT, PLAYER_KEY_RIGHT,
    PLAYER_KEY_JUMP, PLAYER_KEY_SHOOT, ENTITY_SHOT_DELAY
)
from code.Entity import Entity
from code.PlayerShot import PlayerShot
from code.Utils import load_frames


class Player(Entity):
    def __init__(self, name: str, position: tuple):
        super().__init__(name, position)
        self.facing = 1
        self.animations_right = self.__load_all_animations(flip_x=False)
        self.animations_left = self.__load_all_animations(flip_x=True)
        self.state = 'Idle'
        self.frame_idx = 0.0
        self.surf = self.animations_right['Idle'][0]

        self.ground_y = max(MIN_Y, min(MAX_Y, position[1]))
        self.z_offset = 0.0
        self.z_velocity = 0.0
        self.is_jumping = False

        self.rect = self.surf.get_rect(midbottom=(position[0], int(self.ground_y)))
        self.hitbox = pygame.Rect(0, 0, 22, 38)
        self.hitbox.midbottom = self.rect.midbottom

        self.shot_delay = 0
        self.attack_timer = 0
        self.hurt_timer = 0
        self.dead_timer = 0
        self.invuln_timer = 0
        self.is_dying = False
        self.death_finished = False

    def __load_all_animations(self, flip_x: bool) -> dict:
        if self.name == 'Player1':
            return {
                'Idle': load_frames('Player1_Idle', flip_x=flip_x, scale=0.75),
                'Walk': load_frames('Player1_Walk', flip_x=flip_x, scale=0.75),
                'Run': load_frames('Player1_Run', flip_x=flip_x, scale=0.75),
                'Jump': load_frames('Player1_Jump', flip_x=flip_x, scale=0.75),
                'Attack': load_frames('Player1_Attack_3', flip_x=flip_x, scale=0.75),
                'Hurt': load_frames('Player1_Hurt', flip_x=flip_x, scale=0.75),
                'Dead': load_frames('Player1_Dead', flip_x=flip_x, scale=0.75),
            }
        else:
            return {
                'Idle': load_frames('Player2_Idle', flip_x=flip_x, scale=0.75),
                'Walk': load_frames('Player2_Walk', flip_x=flip_x, scale=0.75),
                'Run': load_frames('Player2_Run', flip_x=flip_x, scale=0.75),
                'Jump': load_frames('Player2_Jump', flip_x=flip_x, scale=0.75),
                'Attack': load_frames('Player2_Attack_2', flip_x=flip_x, scale=0.75),
                'Hurt': load_frames('Player2_Hurt', flip_x=flip_x, scale=0.75),
                'Dead': load_frames('Player2_Dead', flip_x=flip_x, scale=0.75),
            }

    def __current_frames(self, state: str) -> list[pygame.Surface]:
        anim_dict = self.animations_right if self.facing == 1 else self.animations_left
        return anim_dict[state]

    def take_hit(self, damage: int):
        if self.invuln_timer > 0 or self.is_dying:
            return
        self.health -= damage
        self.invuln_timer = 35
        if self.health <= 0:
            self.health = 0
            self.is_dying = True
            self.state = 'Dead'
            self.frame_idx = 0.0
            self.dead_timer = 35
        else:
            self.hurt_timer = 12
            self.state = 'Hurt'
            self.frame_idx = 0.0

    def move(self):
        if self.invuln_timer > 0:
            self.invuln_timer -= 1

        if self.is_dying:
            frames = self.__current_frames('Dead')
            if self.frame_idx < len(frames) - 1:
                self.frame_idx += 0.25
            self.surf = frames[int(self.frame_idx)]
            self.dead_timer -= 1
            if self.dead_timer <= 0:
                self.death_finished = True
            return

        pressed_key = pygame.key.get_pressed()
        moving = False
        speed = ENTITY_SPEED[self.name]

        if pressed_key[PLAYER_KEY_LEFT[self.name]] and self.hitbox.left > 15:
            self.rect.x -= speed
            self.facing = -1
            moving = True
        if pressed_key[PLAYER_KEY_RIGHT[self.name]] and self.hitbox.right < WIN_WIDTH - 15:
            self.rect.x += speed
            self.facing = 1
            moving = True

        if pressed_key[PLAYER_KEY_UP[self.name]] and self.ground_y > MIN_Y:
            self.ground_y -= speed
            moving = True
        if pressed_key[PLAYER_KEY_DOWN[self.name]] and self.ground_y < MAX_Y:
            self.ground_y += speed
            moving = True

        jump_pressed = pressed_key[PLAYER_KEY_JUMP[self.name]] or (
            self.name == 'Player1' and pressed_key[pygame.K_z]
        )
        if jump_pressed and not self.is_jumping:
            self.is_jumping = True
            self.z_velocity = 12.5

        if self.is_jumping:
            self.z_offset += self.z_velocity
            self.z_velocity -= 0.65
            if self.z_offset <= 0:
                self.z_offset = 0
                self.z_velocity = 0
                self.is_jumping = False

        self.rect.bottom = int(self.ground_y - self.z_offset)
        self.hitbox.midbottom = self.rect.midbottom

        if self.hurt_timer > 0:
            self.hurt_timer -= 1
            new_state = 'Hurt'
        elif self.attack_timer > 0:
            self.attack_timer -= 1
            new_state = 'Attack'
        elif self.is_jumping:
            new_state = 'Jump'
        elif moving:
            new_state = 'Run'
        else:
            new_state = 'Idle'

        if new_state != self.state:
            self.state = new_state
            self.frame_idx = 0.0

        frames = self.__current_frames(self.state)
        anim_speed = 0.28 if self.state in ('Attack', 'Run') else 0.16
        self.frame_idx = (self.frame_idx + anim_speed) % len(frames)
        self.surf = frames[int(self.frame_idx)]

    def shoot(self):
        if self.is_dying:
            return None
        if self.shot_delay > 0:
            self.shot_delay -= 1
            return None

        pressed_key = pygame.key.get_pressed()
        shoot_pressed = (
            pressed_key[PLAYER_KEY_SHOOT[self.name]]
            or (self.name == 'Player1' and (pressed_key[pygame.K_x] or pressed_key[pygame.K_RCTRL]))
            or (self.name == 'Player2' and pressed_key[pygame.K_f])
        )
        if shoot_pressed:
            self.shot_delay = ENTITY_SHOT_DELAY[self.name]
            self.attack_timer = 14
            self.state = 'Attack'
            self.frame_idx = 0.0
            shot_sheet = 'Player1_Fire_2' if self.name == 'Player1' else 'Player1_Fire_1'
            spawn_x = self.hitbox.right + 10 if self.facing == 1 else self.hitbox.left - 10
            return PlayerShot(
                name=f'{self.name}Shot',
                position=(spawn_x, self.hitbox.centery - 4),
                sheet_name=shot_sheet,
                direction=self.facing
            )
        return None