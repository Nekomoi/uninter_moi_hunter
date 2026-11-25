import pygame

# Dimensões da janela
WIN_WIDTH = 960
WIN_HEIGHT = 540

# Margens verticais livres
MIN_Y = 65
MAX_Y = WIN_HEIGHT - 12

# Cores RGB
C_PURPLE = (210, 120, 255)
C_CRIMSON = (255, 70, 90)
C_YELLOW = (255, 230, 100)
C_WHITE = (255, 255, 255)
C_BLACK = (0, 0, 0)
C_CYAN = (90, 240, 255)
C_GOLD = (255, 200, 60)

# Opções do Menu (sem modo competitivo)
MENU_OPTION = (
    '1 JOGADOR',
    '2 JOGADORES (CO-OP)',
    'SCORE',
    'SAIR',
)

# Eventos customizados
EVENT_ENEMY = pygame.USEREVENT + 1
EVENT_TIMEOUT = pygame.USEREVENT + 2

# Camadas de fundo por fase (cenário estático: velocidade 0)
LEVEL_BG_LAYERS = {
    'Level1': [
        ('Level1_4', 0),
        ('Level1_5', 0),
        ('Level1_3', 0),
        ('Level1_2', 0),
        ('Level1_1', 0),
    ],
    'Level2': [
        ('Level2_6', 0),
        ('Level2_5', 0),
        ('Level2_4', 0),
        ('Level2_3', 0),
        ('Level2_2', 0),
        ('Level2_1', 0),
    ],
    'Level3': [
        ('Level3_4', 0),
        ('Level3_5', 0),
        ('Level3_2', 0),
        ('Level3_3', 0),
        ('Level3_1', 0),
    ],
    'Level4': [
        ('Level4_4', 0),
        ('Level4_5', 0),
        ('Level4_3', 0),
        ('Level4_2', 0),
        ('Level4_1', 0),
    ],
}

# Quantidade exata de frames horizontais de cada sprite sheet
SPRITE_FRAMES = {
    'Player1_Idle': 8,
    'Player1_Walk': 8,
    'Player1_Run': 8,
    'Player1_Jump': 10,
    'Player1_Attack_3': 7,
    'Player1_Hurt': 2,
    'Player1_Dead': 10,
    'Player1_Fire_1': 14,
    'Player1_Fire_2': 11,
    'Player2_Idle': 6,
    'Player2_Walk': 8,
    'Player2_Run': 8,
    'Player2_Jump': 15,
    'Player2_Attack_2': 6,
    'Player2_Hurt': 3,
    'Player2_Dead': 6,
    'Enemy1_Idle': 7,
    'Enemy1_Walk': 12,
    'Enemy1_Attack': 8,
    'Enemy1_Hurt': 4,
    'Enemy1_Dead': 4,
    'Enemy1_Charge': 8,
    'Enemy2_Idle': 7,
    'Enemy2_Walk': 12,
    'Enemy2_Attack': 4,
    'Enemy2_Hurt': 4,
    'Enemy2_Dead': 4,
    'Enemy2_Charge': 10,
}

# Velocidades
ENTITY_SPEED = {
    'Player1': 4,
    'Player2': 4,
    'Player1Shot': 10,
    'Player2Shot': 10,
    'Enemy1': 2,
    'Enemy2': 3,
    'Enemy1Shot': 6,
    'Enemy2Shot': 7,
}

# Pontos de vida padrão (jogadores com 300; inimigos morrem rápido)
ENTITY_HEALTH = {
    'Player1': 300,
    'Player2': 300,
    'Player1Shot': 1,
    'Player2Shot': 1,
    'Enemy1': 25,
    'Enemy2': 40,
    'Enemy1Shot': 1,
    'Enemy2Shot': 1,
}

# Dano por impacto
ENTITY_DAMAGE = {
    'Player1': 15,
    'Player2': 15,
    'Player1Shot': 25,
    'Player2Shot': 25,
    'Enemy1': 15,
    'Enemy2': 20,
    'Enemy1Shot': 15,
    'Enemy2Shot': 20,
}

# Pontuação por inimigo derrotado
ENTITY_SCORE = {
    'Player1': 0,
    'Player2': 0,
    'Player1Shot': 0,
    'Player2Shot': 0,
    'Enemy1': 100,
    'Enemy2': 150,
    'Enemy1Shot': 0,
    'Enemy2Shot': 0,
}

# Cadência de disparo (frames)
ENTITY_SHOT_DELAY = {
    'Player1': 14,
    'Player2': 14,
    'Enemy1': 110,
    'Enemy2': 130,
}

# Controles
PLAYER_KEY_UP = {'Player1': pygame.K_UP, 'Player2': pygame.K_w}
PLAYER_KEY_DOWN = {'Player1': pygame.K_DOWN, 'Player2': pygame.K_s}
PLAYER_KEY_LEFT = {'Player1': pygame.K_LEFT, 'Player2': pygame.K_a}
PLAYER_KEY_RIGHT = {'Player1': pygame.K_RIGHT, 'Player2': pygame.K_d}
PLAYER_KEY_JUMP = {'Player1': pygame.K_RSHIFT, 'Player2': pygame.K_q}
PLAYER_KEY_SHOOT = {'Player1': pygame.K_SPACE, 'Player2': pygame.K_LCTRL}

# Regras da fase: 1 minuto (60.000 ms) OU matar 30 inimigos
SPAWN_TIME = 1500
TIMEOUT_STEP = 100
TIMEOUT_LEVEL = 60000
KILLS_TO_WIN = 30

# Posições da tela de Score
SCORE_POS = {
    'Title': (WIN_WIDTH / 2, 65),
    'EnterName': (WIN_WIDTH / 2, 130),
    'Label': (WIN_WIDTH / 2, 165),
    'Name': (WIN_WIDTH / 2, 200),
    0: (WIN_WIDTH / 2, 200),
    1: (WIN_WIDTH / 2, 230),
    2: (WIN_WIDTH / 2, 260),
    3: (WIN_WIDTH / 2, 290),
    4: (WIN_WIDTH / 2, 320),
    5: (WIN_WIDTH / 2, 350),
    6: (WIN_WIDTH / 2, 380),
    7: (WIN_WIDTH / 2, 410),
    8: (WIN_WIDTH / 2, 440),
    9: (WIN_WIDTH / 2, 470),
}