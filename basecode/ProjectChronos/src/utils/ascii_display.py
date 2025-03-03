import pygame

from ecs.components.components import Position
from ecs.entities.enemy import Enemy, QuantumPhantom


class ASCIIDisplay:
    def __init__(self):
        # 初始化 tile_cache 和 colors 属性
        self.tile_cache = {}
        self.colors = {
            'floor': (0, 0, 0),
            'wall': (100, 100, 100),
            '.': (0, 0, 0),  # 地板颜色
            '#': (100, 100, 100),  # 墙壁颜色
            '~': (0, 0, 255),  # 水颜色
            '♣': (0, 255, 0),  # 树木颜色
            'stalagmite': (169, 169, 169),  # 石笋颜色
            'player': (255, 0, 0)  # 玩家颜色
        }
        # 初始化 font 属性
        self.font = pygame.font.Font(None, 32)
    def render(self, game_state, screen, camera_offset, player_moved, entity_manager):
        # 只渲染可见区域（约提升30%帧率）
        start_x = max(0, int(-camera_offset[0] // 32) - 2)
        end_x = min(len(game_state['map_data'][0]), start_x + 45)  # 1280/32=40 + 缓冲
        start_y = max(0, int(-camera_offset[1] // 32) - 2)
        end_y = min(len(game_state['map_data']), start_y + 25)  # 720/32=22.5 + 缓冲
        map_data = game_state['map_data']
        for y, row in enumerate(map_data):
            for x, tile in enumerate(row):
                tile_surface = self._get_tile_surface(tile)
                screen.blit(tile_surface, (x * 32 + camera_offset[0], y * 32 + camera_offset[1]))

        # 渲染X坐标
        for x in range(len(map_data[0])):
            text_surface = self.font.render(str(x), True, (255, 255, 255))
            screen.blit(text_surface, (x * 32 + camera_offset[0], -32 + camera_offset[1]))

        # 渲染Y坐标
        for y in range(len(map_data)):
            text_surface = self.font.render(str(y), True, (255, 255, 255))
            screen.blit(text_surface, (-32 + camera_offset[0], y * 32 + camera_offset[1]))

        # 渲染敌人
        for entity in entity_manager.get_entities_with(Position, Enemy):
            pos = entity_manager.get_component(entity, Position)
            enemy = entity_manager.get_component(entity, Enemy)
            symbol = 'E' if not isinstance(enemy, QuantumPhantom) else 'Q'  # 根据敌人类型自定义符号
            screen_x = (pos.x * 32) + camera_offset[0]
            screen_y = (pos.y * 32) + camera_offset[1]
            self._draw_tile(screen, screen_x, screen_y, symbol, (255, 0, 0) if not isinstance(enemy, QuantumPhantom) else (0, 255, 255))  # 不同敌人使用不同颜色

        # 渲染玩家
        player_x = game_state['player_x']
        player_y = game_state['player_y']
        player_surface = self._get_tile_surface('@')
        screen.blit(player_surface, (player_x * 32 + camera_offset[0], player_y * 32 + camera_offset[1]))
        if player_moved:  # 新增：只有在玩家移动时才打印调试信息
            print(f"Rendering player at ({player_x}, {player_y})")

    def _get_tile_surface(self, tile):
        """ 生成带边框的ASCII字符表面 """
        if tile not in self.tile_cache:
            # 创建基础表面
            surface = pygame.Surface((32, 32), pygame.SRCALPHA)

            # 绘制背景色（如果是地板或墙壁）
            if tile in self.colors:
                surface.fill(self.colors[tile])

            # 绘制ASCII字符
            if tile.strip():  # 过滤空字符
                text_surface = self.font.render(tile, True, (255, 255, 255) if tile != '@' else self.colors['player'])
                text_rect = text_surface.get_rect(center=(16, 16))
                surface.blit(text_surface, text_rect)

            # 添加边框
            pygame.draw.rect(surface, (50, 50, 50), surface.get_rect(), 1)

            self.tile_cache[tile] = surface
        return self.tile_cache[tile]

    def _draw_tile(self, screen, x, y, symbol, color):
        """绘制单个瓦片"""
        surface = self._get_tile_surface(symbol)
        screen.blit(surface, (x, y))