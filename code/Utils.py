import os
import sys
import pygame
from pygame import Surface
from code.Const import SPRITE_FRAMES, C_BLACK


def get_base_dir() -> str:
    if getattr(sys, 'frozen', False):
        return getattr(sys, '_MEIPASS', os.path.dirname(sys.executable))
    return os.path.abspath('.')


def resource_path(relative_path: str) -> str:
    return os.path.join(get_base_dir(), relative_path.lstrip('./').lstrip('/'))


def data_path(filename: str) -> str:
    if getattr(sys, 'frozen', False):
        base = os.path.dirname(sys.executable)
    else:
        base = os.path.abspath('.')
    return os.path.join(base, filename)


def load_frames(sheet_name: str, flip_x: bool = False, scale: float = 1.6) -> list[Surface]:
    sheet = pygame.image.load(resource_path(f'assets/{sheet_name}.png')).convert_alpha()
    num_frames = SPRITE_FRAMES.get(sheet_name, 1)
    sheet_w, sheet_h = sheet.get_size()
    frame_w = sheet_w // num_frames
    frames = []

    for i in range(num_frames):
        sub = sheet.subsurface(pygame.Rect(i * frame_w, 0, frame_w, sheet_h))
        if scale != 1.0:
            sub = pygame.transform.scale(sub, (int(frame_w * scale), int(sheet_h * scale)))
        if flip_x:
            sub = pygame.transform.flip(sub, True, False)
        frames.append(sub)
    return frames


def draw_text_outline(
    window: Surface,
    text: str,
    size: int,
    color: tuple,
    pos: tuple,
    center: bool = True,
    outline_color: tuple = C_BLACK,
    outline_width: int = 2
):
    font = pygame.font.SysFont('Lucida Sans Typewriter', size, bold=True)
    base_surf = font.render(text, True, color).convert_alpha()
    outline_surf = font.render(text, True, outline_color).convert_alpha()

    if center:
        rect = base_surf.get_rect(center=pos)
    else:
        rect = base_surf.get_rect(topleft=pos)

    for dx in range(-outline_width, outline_width + 1):
        for dy in range(-outline_width, outline_width + 1):
            if dx != 0 or dy != 0:
                window.blit(outline_surf, (rect.x + dx, rect.y + dy))

    window.blit(base_surf, rect)