import random
import pygame
from pygame import Surface
from code.Const import (
    C_WHITE, WIN_HEIGHT, WIN_WIDTH, MENU_OPTION,
    EVENT_ENEMY, SPAWN_TIME, C_CYAN, C_CRIMSON, C_YELLOW, C_GOLD,
    EVENT_TIMEOUT, TIMEOUT_STEP, TIMEOUT_LEVEL, KILLS_TO_WIN
)
from code.Background import Background
from code.Enemy import Enemy
from code.Entity import Entity
from code.EntityFactory import EntityFactory
from code.EntityMediator import EntityMediator
from code.Player import Player
from code.Utils import draw_text_outline


class Level:
    def __init__(self, window: Surface, name: str, game_mode: str, player_score: list[int]):
        self.timeout = TIMEOUT_LEVEL
        self.kills = 0
        self.window = window
        self.name = name
        self.game_mode = game_mode
        self.entity_list: list[Entity] = []
        self.entity_list.extend(EntityFactory.get_entity(self.name))

        player1 = EntityFactory.get_entity('Player1')
        player1.score = player_score[0]
        self.entity_list.append(player1)

        if game_mode == MENU_OPTION[1]:
            player2 = EntityFactory.get_entity('Player2')
            player2.score = player_score[1]
            self.entity_list.append(player2)

        pygame.time.set_timer(EVENT_ENEMY, SPAWN_TIME)
        pygame.time.set_timer(EVENT_TIMEOUT, TIMEOUT_STEP)

    def run(self, player_score: list[int]) -> bool:
        pygame.mixer_music.load(f'./assets/{self.name}_backgroundsong.mp3')
        pygame.mixer_music.set_volume(0.35)
        pygame.mixer_music.play(-1)
        clock = pygame.time.Clock()

        while True:
            clock.tick(60)

            bg_entities = [e for e in self.entity_list if isinstance(e, Background)]
            actors = [e for e in self.entity_list if not isinstance(e, Background)]
            actors.sort(key=lambda e: e.rect.bottom)

            for ent in bg_entities + actors:
                if isinstance(ent, Player) and ent.invuln_timer > 0 and (ent.invuln_timer // 4) % 2 == 0:
                    pass
                else:
                    self.window.blit(source=ent.surf, dest=ent.rect)

                ent.move()

                if isinstance(ent, (Player, Enemy)):
                    shoot = ent.shoot()
                    if shoot is not None:
                        self.entity_list.append(shoot)

            draw_text_outline(
                self.window,
                f'{self.name} | Tempo: {self.timeout / 1000:.1f}s | Abates: {self.kills}/{KILLS_TO_WIN}',
                18, C_WHITE, (16, 12), center=False
            )

            for ent in actors:
                if ent.name == 'Player1':
                    draw_text_outline(
                        self.window,
                        f'P1 (Kitsune) - HP: {ent.health} | Pontos: {ent.score}',
                        17, C_GOLD, (16, 38), center=False
                    )
                elif ent.name == 'Player2':
                    draw_text_outline(
                        self.window,
                        f'P2 (Tengu) - HP: {ent.health} | Pontos: {ent.score}',
                        17, C_CYAN, (16, 62), center=False
                    )

            draw_text_outline(
                self.window,
                f'FPS: {clock.get_fps():.0f}',
                14, C_WHITE, (16, WIN_HEIGHT - 26), center=False
            )

            pygame.display.flip()

            EntityMediator.verify_collision(entity_list=self.entity_list)
            self.kills += EntityMediator.verify_health(entity_list=self.entity_list)

            found_player = False
            for ent in self.entity_list:
                if isinstance(ent, Player):
                    found_player = True
                    if ent.name == 'Player1':
                        player_score[0] = ent.score
                    elif ent.name == 'Player2':
                        player_score[1] = ent.score

            if not found_player:
                self.show_end_message('VOCE MORREU! Reiniciando estagio...', C_CRIMSON)
                return False

            if self.kills >= KILLS_TO_WIN:
                self.show_end_message(f'{self.name} CONCLUIDA! (30 Abates)', C_YELLOW)
                return True

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == EVENT_ENEMY:
                    choice = random.choice(('Enemy1', 'Enemy2'))
                    self.entity_list.append(EntityFactory.get_entity(choice))
                if event.type == EVENT_TIMEOUT:
                    self.timeout -= TIMEOUT_STEP
                    if self.timeout <= 0:
                        self.show_end_message(f'{self.name} CONCLUIDA! (Tempo Esgotado)', C_YELLOW)
                        return True

    def show_end_message(self, message: str, color: tuple):
        draw_text_outline(
            self.window,
            message,
            30,
            color,
            (WIN_WIDTH / 2, WIN_HEIGHT / 2),
            center=True,
            outline_width=3
        )
        pygame.display.flip()
        pygame.time.delay(2200)