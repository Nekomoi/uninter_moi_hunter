import pygame
from code.Const import WIN_WIDTH, WIN_HEIGHT, MENU_OPTION
from code.Level import Level
from code.Menu import Menu
from code.Score import Score


class Game:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode(size=(WIN_WIDTH, WIN_HEIGHT))
        pygame.display.set_caption('Uninter Moi Hunter - Moises Viegas (RU: 5471809)')

    def run(self):
        levels = ['Level1', 'Level2', 'Level3', 'Level4']

        while True:
            score = Score(self.window)
            menu = Menu(self.window)
            menu_return = menu.run()

            if menu_return in [MENU_OPTION[0], MENU_OPTION[1]]:
                player_score = [0, 0]
                current_level_idx = 0

                while current_level_idx < len(levels):
                    saved_score = list(player_score)
                    level = Level(self.window, levels[current_level_idx], menu_return, player_score)
                    level_result = level.run(player_score)

                    if level_result == 'MENU':
                        break
                    elif level_result is True:
                        current_level_idx += 1
                    else:
                        player_score = list(saved_score)
                else:
                    score.save(menu_return, player_score)

            elif menu_return == MENU_OPTION[2]:
                score.show()

            elif menu_return == MENU_OPTION[3]:
                pygame.quit()
                quit()