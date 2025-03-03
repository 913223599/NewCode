class AIComponent:
    """ AI组件 """
    behavior: str = "default"  # 默认行为
    target: str = None  # 目标实体ID

class Movable:
    def __init__(self, speed: float = 5.0):
        self.speed = speed

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
    def __init__(self, Health: float = 100):
        self.Health = Health
        self.current = Health
        self.max = Health

class ElementState:
    """ 元素状态组件 """
    active_element: str = None
    effect_duration: float = 0.0

class Combat:
    """ 战斗属性组件 """
    attack: int = 10
    defense: int = 5
