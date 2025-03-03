# movement.py
from ecs.systems.base import System
from ..components.components import Movable, Position


class MovementSystem(System):
    def update(self, dt: float):
        entities = self.em.get_entities_with(Position, Movable)

        for entity in entities:
            pos = self.em.get_component(entity, Position)
            mov = self.em.get_component(entity, Movable)

            # 更新位置
            pos.x += int(mov.dx * mov.speed * dt)
            pos.y += int(mov.dy * mov.speed * dt)
