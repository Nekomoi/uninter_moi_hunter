import random
from code.Background import Background
from code.Const import WIN_WIDTH, MIN_Y, MAX_Y, LEVEL_BG_LAYERS
from code.Enemy import Enemy
from code.Player import Player


class EntityFactory:

    @staticmethod
    def get_entity(entity_name: str):
        if entity_name in LEVEL_BG_LAYERS:
            list_bg = []
            for layer_name, speed in LEVEL_BG_LAYERS[entity_name]:
                list_bg.append(Background(layer_name, (0, 0), speed))
            return list_bg

        match entity_name:
            case 'Player1':
                return Player('Player1', (WIN_WIDTH // 2 - 80, (MIN_Y + MAX_Y) // 2))
            case 'Player2':
                return Player('Player2', (WIN_WIDTH // 2 + 80, (MIN_Y + MAX_Y) // 2))
            case 'Enemy1' | 'Enemy2':
                spawn_y = random.randint(MIN_Y + 20, MAX_Y)
                # Escolhe aleatoriamente entre vir da direita (-1) ou da esquerda (1)
                direction = random.choice((-1, 1))
                spawn_x = WIN_WIDTH + 30 if direction == -1 else -30
                return Enemy(entity_name, (spawn_x, spawn_y), direction=direction)
        return None