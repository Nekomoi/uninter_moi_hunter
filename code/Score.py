from datetime import datetime
import sys
import pygame
from pygame import Surface, KEYDOWN, K_RETURN, K_BACKSPACE, K_ESCAPE
from code.Const import WIN_WIDTH, WIN_HEIGHT, C_YELLOW, SCORE_POS, MENU_OPTION, C_WHITE, C_GOLD
from code.DBProxy import DBProxy
from code.Utils import draw_text_outline, resource_path, data_path


class Score:
    def __init__(self, window: Surface):
        self.window = window
        raw = pygame.image.load(resource_path('assets/ScoreBG.png')).convert_alpha()
        self.surf = pygame.transform.scale(raw, (WIN_WIDTH, WIN_HEIGHT))
        self.rect = self.surf.get_rect(topleft=(0, 0))

    def save(self, game_mode: str, player_score: list[int]):
        pygame.mixer_music.load(resource_path('assets/Score_song.mp3'))
        pygame.mixer_music.set_volume(0.4)
        pygame.mixer_music.play(-1)
        db_proxy = DBProxy(data_path('DBUninterMoiHunter'))
        name = ''

        while True:
            self.window.blit(source=self.surf, dest=self.rect)
            draw_text_outline(self.window, 'VITORIA! CASTELO CONQUISTADO!', 36, C_YELLOW, SCORE_POS['Title'], outline_width=3)

            if game_mode == MENU_OPTION[0]:
                score = player_score[0]
                text = 'Digite as 4 letras do Jogador 1 e aperte ENTER:'
            else:
                score = player_score[0] + player_score[1]
                text = 'Digite as 4 letras da Equipe Co-op e aperte ENTER:'

            draw_text_outline(self.window, text, 20, C_WHITE, SCORE_POS['EnterName'])
            draw_text_outline(self.window, f'Pontuacao Final: {score}', 22, C_GOLD, SCORE_POS['Label'])

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_RETURN and len(name) == 4:
                        db_proxy.save({'name': name, 'score': int(score), 'date': get_formatted_date()})
                        db_proxy.close()
                        self.show()
                        return
                    elif event.key == K_BACKSPACE:
                        name = name[:-1]
                    else:
                        if len(name) < 4 and event.unicode.isalnum():
                            name += event.unicode.upper()

            draw_text_outline(self.window, name if name else '____', 32, C_GOLD, SCORE_POS['Name'])
            pygame.display.flip()

    def show(self):
        pygame.mixer_music.load(resource_path('assets/Score_song.mp3'))
        pygame.mixer_music.set_volume(0.4)
        pygame.mixer_music.play(-1)

        db_proxy = DBProxy(data_path('DBUninterMoiHunter'))
        list_score = db_proxy.retrieve_top10()
        db_proxy.close()

        while True:
            self.window.blit(source=self.surf, dest=self.rect)
            draw_text_outline(self.window, 'TOP 10 RECORDES', 40, C_YELLOW, SCORE_POS['Title'], outline_width=3)
            draw_text_outline(self.window, 'NOME      PONTOS          DATA      ', 20, C_GOLD, SCORE_POS['Label'])

            for index, player_score in enumerate(list_score):
                _, name, score, date = player_score
                draw_text_outline(
                    self.window,
                    f'{name}      {score:05d}      {date}',
                    19,
                    C_WHITE,
                    SCORE_POS[index]
                )

            draw_text_outline(
                self.window,
                'Pressione ENTER ou ESC para voltar ao Menu',
                16,
                C_GOLD,
                (WIN_WIDTH / 2, WIN_HEIGHT - 25)
            )

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key in (K_ESCAPE, K_RETURN):
                        return
            pygame.display.flip()


def get_formatted_date():
    current_datetime = datetime.now()
    current_time = current_datetime.strftime('%H:%M')
    current_date = current_datetime.strftime('%d/%m/%y')
    return f'{current_time} - {current_date}'