# 文件位置：basecode\ProjectChronos\src\entities\element.py
class Element:
    def __init__(self, x, y, element_type):
        self.x = x
        self.y = y
        self.type = element_type
        # 添加ECS组件支持
        self.components = {
            'position': (x, y),
            'element': self,
            'renderable': {  # 渲染组件
                'symbol': self._get_symbol(),
                'color': self._get_color()
            }
        }

    def _get_symbol(self):
        # 根据元素类型返回对应的符号
        symbol_map = {
            'fire': '🔥',
            'water': '~',
            'vegetation': '♣︎',
            'stalagmite': '_spike_'  # 新增石笋符号
        }
        return symbol_map.get(self.type, '?')  # 使用 get 方法避免 KeyError

    def _get_color(self):
        # 根据元素类型返回对应的颜色
        color_map = {
            'fire': (255, 69, 0),
            'water': (0, 123, 255),
            'vegetation': (34, 139, 34),
            'stalagmite': (169, 169, 169)  # 新增石笋颜色
        }
        return color_map.get(self.type, (255, 255, 255))  # 使用 get 方法避免 KeyError
