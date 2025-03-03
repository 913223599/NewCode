class Player:
    def __init__(self, x, y, move_speed=1):
        # 初始化玩家的位置和移动速度
        self.x = x
        self.y = y
        self.move_speed = move_speed
        self.status = {}  # 用于存储玩家状态（例如是否湿透、是否烧伤）

    def move(self, dx, dy, game_map):
        """网格化移动"""
        new_x = self.x + dx * self.move_speed
        new_y = self.y + dy * self.move_speed

        # 确保新坐标在地图范围内
        if new_x < 0 or new_x >= len(game_map[0]) or new_y < 0 or new_y >= len(game_map):
            print(f"Cannot move to ({new_x}, {new_y}) due to out of bounds")
            return False

        # 使用 get_tile 方法检查目标位置是否可通行
        tile = self.get_tile(game_map, new_x, new_y)
        if tile == '.':
            self.x = new_x
            self.y = new_y
            print(f"Player moved to ({self.x}, {self.y})")
            return True
        elif tile == '~':  # 水元素
            self.status['wet'] = True
            print("Player is now wet!")
            self.x = new_x
            self.y = new_y
            return True
        elif tile == '🔥':  # 火元素
            if self.status.get('wet'):
                print("Steam created from fire and water!")
            else:
                self.status['burned'] = True
                print("Player is now burned!")
            self.x = new_x
            self.y = new_y
            return True
        else:
            reason = "wall" if tile == '#' else "vegetation" if tile == '♣' else tile
            print(f"Cannot move to ({new_x}, {new_y}) due to {reason}")
            return False

    def get_tile(self, game_map, x, y):
        """ 获取指定位置的地图瓦片 """
        if 0 <= x < len(game_map[0]) and 0 <= y < len(game_map):
            return game_map[y][x]
        return None