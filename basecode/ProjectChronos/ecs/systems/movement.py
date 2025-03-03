# movement.py
from ecs.systems.base import System
from ..components.components import Movable, Position
from ..entities.enemy import Enemy


class MovementSystem(System):
    def update(self, dt: float):
        entities = self.em.get_entities_with(Position, Movable)

        for entity in entities:
            pos = self.em.get_component(entity, Position)
            mov = self.em.get_component(entity, Movable)

            # 更新位置
            pos.x += int(mov.dx * mov.speed * dt)
            pos.y += int(mov.dy * mov.speed * dt)

            # 检查是否为敌人并触发相关逻辑
            enemy = self.em.get_component(entity, Enemy)
            if enemy and hasattr(enemy, 'on_move'):
                enemy.on_move()

