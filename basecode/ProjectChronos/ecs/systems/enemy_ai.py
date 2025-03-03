from ecs.components.combat import EnemyTag
from ecs.components.components import Position, Movable


class EnemyAISystem:
    def update(self, dt, entity_manager):
        for entity in entity_manager.get_entities_with(EnemyTag):
            pos = entity_manager.get_component(entity, Position)
            movable = entity_manager.get_component(entity, Movable)
            # 实现敌人AI逻辑...
