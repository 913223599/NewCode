# ai.py
from ecs.components.components import Position, Movable
from ecs.components.components import AIComponent
from ecs.systems.base import System

class AISystem(System):
    def update(self, player_pos):
        entities = self.em.get_entities_with(AIComponent, Position)

        for entity in entities:
            ai = self.em.get_component(entity, AIComponent)
            pos = self.em.get_component(entity, Position)

            # A*路径finding优化
            path = self._find_path((pos.x, pos.y), player_pos)
            if len(path) > 1:
                next_x, next_y = path[1]
                mov = self.em.get_component(entity, Movable)
                mov.dx = (next_x - pos.x) / mov.speed
                mov.dy = (next_y - pos.y) / mov.speed