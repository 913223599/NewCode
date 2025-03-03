from .base import System
from ..components.components import ElementState, Position, Health

class ElementSystem(System):
    def __init__(self, entity_manager, element_engine):
        super().__init__(entity_manager)
        self.element_engine = element_engine

    def update(self, dt: float):
        # 获取所有携带元素状态的实体
        entities = self.em.get_entities_with(ElementState, Position)

        for entity in entities:
            elem = self.em.get_component(entity, ElementState)
            pos = self.em.get_component(entity, Position)
            health = self.em.get_component(entity, Health)

            if elem.effect_duration > 0:
                elem.effect_duration -= dt
                # 应用元素持续效果
                if health:
                    health.current -= 2  # 示例伤害
