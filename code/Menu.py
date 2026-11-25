import sys
import pygame
from pygame import Surface
from code.Const import WIN_WIDTH, WIN_HEIGHT, C_PURPLE, MENU_OPTION, C_WHITE, C_YELLOW, C_CYAN, C_GOLD
from code.Utils import draw_text_outline, resource_path


class Menu:
    def __init__(self, window: Surface):
        self.window = window
        raw = pygame.image.load(resource_path('assets/Menu.png')).convert_alpha()
        self.surf = pygame.transform.scale(raw, (WIN_WIDTH, WIN_HEIGHT))
        self.rect = self.surf.get_rect(topleft=(0, 0))

    def run(self):
        menu_option = 0
        pygame.mixer_music.load(resource_path('assets/Menu_song.mp3'))
        pygame.mixer_music.set_volume(0.4)
        pygame.mixer_music.play(-1)

        while True:
            self.window.blit(source=self.surf, dest=self.rect)

            draw_text_outline(self.window, 'Aluno: Moises Viegas', 16, C_GOLD, (16, 14), center=False)
            draw_text_outline(self.window, 'RU: 5471809', 16, C_GOLD, (16, 36), center=False)

            draw_text_outline(self.window, 'UNINTER', 52, C_PURPLE, (WIN_WIDTH / 2, 92), outline_width=3)
            draw_text_outline(self.window, 'MOI HUNTER', 52, C_PURPLE, (WIN_WIDTH / 2, 145), outline_width=3)

            for i in range(len(MENU_OPTION)):
                if i == menu_option:
                    draw_text_outline(self.window, f'> {MENU_OPTION[i]} <', 26, C_YELLOW, (WIN_WIDTH / 2, 230 + 36 * i))
                else:
                    draw_text_outline(self.window, MENU_OPTION[i], 24, C_WHITE, (WIN_WIDTH / 2, 230 + 36 * i))

            draw_text_outline(
                self.window,
                'P1 (Kitsune): Setas (Mover) | R-Shift ou Z (Pular) | Espaco ou X (Atirar)',
                15, C_CYAN, (WIN_WIDTH / 2, WIN_HEIGHT - 48)
            )
            draw_text_outline(
                self.window,
                'P2 (Tengu): W/A/S/D (Mover) | Q (Pular) | L-CTRL ou F (Atirar) | Menu: Setas + Enter',
                15, C_CYAN, (WIN_WIDTH / 2, WIN_HEIGHT - 24)
            )

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        menu_option = (menu_option + 1) % len(MENU_OPTION)
                    elif event.key == pygame.K_UP:
                        menu_option = (menu_option - 1) % len(MENU_OPTION)
                    elif event.key == pygame.K_RETURN:
                        return MENU_OPTION[menu_option]