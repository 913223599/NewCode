import pygame

from ecs.components.combat import EnemyTag
from ecs.components.components import Position


class PlayerInfoWindow:
    def __init__(self, screen, position, size):
        self.screen = screen
        self.position = position
        self.size = size
        self.info_screen = pygame.Surface(size)
        pygame.display.set_caption("Player Info")

    def update(self, game_state):
        self.info_screen.fill((255, 255, 255))  # 填充背景色
        font = pygame.font.Font(None, 24)
        player_x = game_state['player_x']
        player_y = game_state['player_y']
        player_speed = game_state['player'].move_speed
        player_status = game_state['player'].status

        # 创建文本表面
        text_x = font.render(f"Player X: {player_x}", True, (0, 0, 0))
        text_y = font.render(f"Player Y: {player_y}", True, (0, 0, 0))
        text_speed = font.render(f"Player Speed: {player_speed}", True, (0, 0, 0))

        # 获取敌人坐标信息
        entity_manager = game_state['entity_manager']
        enemies = entity_manager.get_entities_with(Position, EnemyTag)  # 确保返回值非空
        if not enemies:
            print("Warning: No enemies found in the entity manager.")
            enemy_positions = []
        else:
            enemy_positions = [(entity_manager.get_component(entity, Position).x, entity_manager.get_component(entity, Position).y) for entity in enemies]
        enemy_info = ', '.join([f"Enemy {i+1}: ({x}, {y})" for i, (x, y) in enumerate(enemy_positions)])

        text_enemies = font.render(f"Enemies: {enemy_info}", True, (0, 0, 0))

        # 绘制文本
        self.info_screen.blit(text_x, (10, 10))
        self.info_screen.blit(text_y, (10, 40))
        self.info_screen.blit(text_speed, (10, 70))
        self.info_screen.blit(text_enemies, (10, 100))

    def draw(self):
        self.screen.blit(self.info_screen, self.position)