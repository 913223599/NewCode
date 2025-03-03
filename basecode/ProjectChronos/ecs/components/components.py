class AIComponent:
    """ AI组件 """
    behavior: str = "default"  # 默认行为
    target: str = None  # 目标实体ID

class Movable:
    """ 可移动组件 """
    speed: float = 5.0  # 格子/秒

class Position:
    """ 实体位置组件 """
    def __init__(self, x: int = 0, y: int = 0):
        self.x = x
        self.y = y

class Renderable:
    """ 可渲染组件 """
    symbol: str = '?'
    color: tuple = (255, 255, 255)

class Health:
    """ 生命值组件 """
    current: int = 100
    max: int = 100

class ElementState:
    """ 元素状态组件 """
    active_element: str = None
    effect_duration: float = 0.0

class Combat:
    """ 战斗属性组件 """
    attack: int = 10
    defense: int = 5
