from typing import Set
from uuid import uuid4

class EntityManager:
    def __init__(self):
        self._entities = {}
        self._components = {}

    def add_entity(self, *components) -> str:
        """ 创建实体并附加组件 """
        entity_id = str(uuid4())
        self._entities[entity_id] = set()

        for comp in components:
            self.add_component(entity_id, comp)

        return entity_id

    def add_component(self, entity_id: str, component):
        """ 为实体添加组件（带类型检查）"""
        if not hasattr(component, '__class__'):
            raise TypeError("Components must be class instances")

        comp_type = type(component)
        if comp_type not in self._components:
            self._components[comp_type] = {}

        self._components[comp_type][entity_id] = component
        self._entities[entity_id].add(comp_type)


    def get_component(self, entity_id: str, component_type):
        """ 获取实体特定组件 """
        return self._components.get(component_type, {}).get(entity_id, None)
    def get_entities_with_any(self, *component_types) -> Set[str]:
        """ 获取包含任意指定组件的实体 """
        entities = set()
        for comp_type in component_types:
            entities.update(self._components.get(comp_type, {}).keys())
        return entities

    def get_entities_with(self, *component_types) -> Set[str]:
        """ 查询拥有指定组件的实体集合 """
        valid_entities = set(self._entities.keys())

        for comp_type in component_types:
            entities_with = set(self._components.get(comp_type, {}).keys())
            valid_entities.intersection_update(entities_with)

        return valid_entities