class ElementSystem:
    ELEMENT_REACTIONS = {
        ('fire', 'water'): 'steam',
        ('fire', 'grass'): 'ash',
        ('water', 'electric'): 'charged_water',
    }

    def apply_element_effect(self, element: str, target_tile: str) -> str:
        """应用元素效果并返回新的瓦片状态"""
        reaction_key = (element, target_tile)
        if reaction_key in self.ELEMENT_REACTIONS:
            return self.ELEMENT_REACTIONS[reaction_key]
        return target_tile

    def _process_reactions(self, game_map, x, y, element):
        """递归处理元素反应链"""
        current_tile = game_map[y][x]
        new_tile = self.apply_element_effect(element, current_tile)
        if new_tile != current_tile:
            game_map[y][x] = new_tile
            # 检查周围瓦片是否有连锁反应
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < len(game_map[0]) and 0 <= ny < len(game_map):
                    self._process_reactions(game_map, nx, ny, element)

    def trigger_element(self, game_map, x, y, element):
        """触发指定位置的元素效果"""
        self._process_reactions(game_map, x, y, element)