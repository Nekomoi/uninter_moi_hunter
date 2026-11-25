from code.Const import WIN_WIDTH
from code.Enemy import Enemy
from code.EnemyShot import EnemyShot
from code.Entity import Entity
from code.Player import Player
from code.PlayerShot import PlayerShot


class EntityMediator:

    @staticmethod
    def __verify_collision_window(ent: Entity):
        if isinstance(ent, Enemy):
            if ent.direction == -1 and ent.rect.right < -60:
                ent.health = 0
                ent.is_dying = True
                ent.dead_timer = 0
            elif ent.direction == 1 and ent.rect.left > WIN_WIDTH + 60:
                ent.health = 0
                ent.is_dying = True
                ent.dead_timer = 0
        elif isinstance(ent, PlayerShot):
            if ent.rect.right < 0 or ent.rect.left > WIN_WIDTH:
                ent.health = 0
        elif isinstance(ent, EnemyShot):
            if ent.rect.right < 0 or ent.rect.left > WIN_WIDTH:
                ent.health = 0

    @staticmethod
    def __get_box(ent: Entity):
        return getattr(ent, 'hitbox', ent.rect)

    @staticmethod
    def __verify_collision_entity(ent1: Entity, ent2: Entity):
        box1 = EntityMediator.__get_box(ent1)
        box2 = EntityMediator.__get_box(ent2)

        if not box1.colliderect(box2):
            return

        if isinstance(ent1, Enemy) and isinstance(ent2, PlayerShot) and not ent1.is_dying:
            ent1.take_hit(ent2.damage, ent2.name)
            ent2.health = 0
        elif isinstance(ent1, PlayerShot) and isinstance(ent2, Enemy) and not ent2.is_dying:
            ent2.take_hit(ent1.damage, ent1.name)
            ent1.health = 0

        elif isinstance(ent1, Player) and isinstance(ent2, EnemyShot):
            ent1.take_hit(ent2.damage)
            ent2.health = 0
        elif isinstance(ent1, EnemyShot) and isinstance(ent2, Player):
            ent2.take_hit(ent1.damage)
            ent1.health = 0

        elif isinstance(ent1, Player) and isinstance(ent2, Enemy) and not ent2.is_dying:
            ent1.take_hit(ent2.damage)
        elif isinstance(ent1, Enemy) and isinstance(ent2, Player) and not ent1.is_dying:
            ent2.take_hit(ent1.damage)

    @staticmethod
    def __give_score(enemy: Enemy, entity_list: list[Entity]):
        if enemy.last_dmg == 'Player1Shot':
            for ent in entity_list:
                if ent.name == 'Player1':
                    ent.score += enemy.score
        elif enemy.last_dmg == 'Player2Shot':
            for ent in entity_list:
                if ent.name == 'Player2':
                    ent.score += enemy.score

    @staticmethod
    def verify_collision(entity_list: list[Entity]):
        for i in range(len(entity_list)):
            entity1 = entity_list[i]
            EntityMediator.__verify_collision_window(entity1)
            for j in range(i + 1, len(entity_list)):
                entity2 = entity_list[j]
                EntityMediator.__verify_collision_entity(entity1, entity2)

    @staticmethod
    def verify_health(entity_list: list[Entity]) -> int:
        kills_in_frame = 0
        for ent in entity_list[:]:
            if isinstance(ent, Enemy):
                if ent.is_dying and ent.dead_timer <= 0:
                    if ent.last_dmg in ('Player1Shot', 'Player2Shot'):
                        EntityMediator.__give_score(ent, entity_list)
                        kills_in_frame += 1
                    entity_list.remove(ent)
            elif isinstance(ent, Player):
                if ent.death_finished:
                    entity_list.remove(ent)
            elif ent.health <= 0:
                entity_list.remove(ent)
        return kills_in_frame