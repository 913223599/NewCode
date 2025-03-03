import copy  # 新增导入 copy 模块
import itertools  # 新增导入 itertools 模块
import json  # 新增导入 json 模块
import random

import pygame  # 添加导入语句

from ecs.components.components import Movable, Position, Health
from ecs.components.combat import EnemyTag
from ecs.entities import Player
from ecs.entities.enemy import Enemy
from ecs.entity_manager import EntityManager  # 新增导入语句
from ..utils.ascii_display import ASCIIDisplay
from ..utils.player_info_window import PlayerInfoWindow  # 新增导入语句
from ..world.level import LevelGenerator


class WorldLine:
    def create_anchor(self, key):
        """创建时间锚点"""
        if not hasattr(self, 'player') or not hasattr(self, 'world_state'):
            raise AttributeError("Player or world state is not initialized.")
        if not hasattr(self, 'anchors'):
            self.anchors = {}
        self.anchors[key] = {
            'player_state': self.player.__dict__.copy(),
            'world_state': self._get_world_snapshot(),
            'timestamp': pygame.time.get_ticks()
        }
        self.chaos_factor *= 1.15  # 增加世界线变动

    def reset(self, anchor_key):
        """重置到指定锚点"""
        if anchor_key in self.anchors:
            anchor = self.anchors[anchor_key]
            # 保留记忆碎片和元素熵值
            preserved_chaos = self.world_state['chaos']
            # 恢复状态
            self.player.__dict__.update(anchor['player_state'])
            self._restore_world(anchor['world_state'])
            self.world_state['chaos'] = preserved_chaos * 1.2
            return True
        return False

    def _restore_world(self, snapshot):
        """恢复世界状态"""
        self.current_level = [row.copy() for row in snapshot['map']]
        self.entities = copy.deepcopy(snapshot['entities'])
        self.world_state['elements'] = snapshot['elements'].copy()


class ChronosGame(WorldLine):
    def __init__(self, use_player_info_window: bool = True):
        super().__init__()
        pygame.init()
        try:
            self.screen = pygame.display.set_mode((1280, 720))  # 创建显示表面
            if self.screen is None:
                raise RuntimeError("Failed to create screen surface")
        except pygame.error as e:
            raise RuntimeError(f"Failed to create screen surface: {e}")
        self.display = ASCIIDisplay()  # 添加显示系统初始化
        # 初始化游戏状态
        self.running = True
        self.current_level = LevelGenerator.generate_map(LevelGenerator, view_width=40, view_height=20)  # 使用 LevelGenerator 替换 cls
        self.world_state = {'chaos': 1.0, 'elements': {}}

        # 修改: 设置初始玩家位置在地板上
        self.player = self._find_spawn_position(self.current_level)

        # 新增：初始化 EntityManager 实例
        self.em = EntityManager()

        # 新增：创建敌人实例并添加到 EntityManager
        enemy_id = self.em.add_entity()  # 生成唯一实体ID
        # 修改: 获取敌人生成位置
        enemy_x, enemy_y = self._find_enemy_spawn_position(self.current_level)
        self.em.add_component(enemy_id, Position(enemy_x, enemy_y))
        self.em.add_component(enemy_id, Movable(speed=1.5))
        self.em.add_component(enemy_id, EnemyTag(difficulty=2))
        self.em.add_component(enemy_id, Health(150))  # 添加血量组件

        # 新增：创建玩家属性窗口实例
        self.use_player_info_window = use_player_info_window
        if self.use_player_info_window:
            self.info_window = PlayerInfoWindow(self.screen, (1000, 50), (300, 200))
        self.player_moved = False  # 新增：玩家是否移动的标志

        # 新增：初始化 anchors 属性
        self.anchors = {}

        # 新增：初始化 chaos_factor 属性
        self.chaos_factor = 1.0  # 初始混沌因子

    def _get_world_snapshot(self):
        """获取世界状态快照"""
        return {
            'map': [row.copy() for row in self.current_level],
            'entities': [],  # 当前未实现实体系统，留空
            'elements': self.world_state['elements'].copy()
        }

    def load_anchor(self):
        """加载最近的时间锚点"""
        if not hasattr(self, 'anchors') or 'last_anchor' not in self.anchors:
            print("Error: No valid time anchor found. Please create an anchor first.")
            print(f"Details: anchors={self.anchors if hasattr(self, 'anchors') else 'None'}")
            return False
        if self.reset('last_anchor'):
            print("Time anchor restored successfully.")
        else:
            print("Failed to restore time anchor.")
            print(f"Details: anchors={self.anchors if hasattr(self, 'anchors') else 'None'}")

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            # 新增：简化后的玩家控制逻辑
            if event.type == pygame.KEYDOWN:
                dx, dy = 0, 0
                if event.key == pygame.K_UP:
                    dx, dy = 0, -1
                elif event.key == pygame.K_DOWN:
                    dx, dy = 0, 1
                elif event.key == pygame.K_LEFT:
                    dx, dy = -1, 0
                elif event.key == pygame.K_RIGHT:
                    dx, dy = 1, 0
                
                # 调用玩家移动方法并设置移动标志
                if (dx, dy) != (0, 0):
                    self.player_moved = self.player.move(dx, dy, self.current_level)
                    # 创建时间锚点
                    self.create_anchor('last_anchor')

            # 实现时间回溯快捷键
            if event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:
                self.load_anchor()
            # 添加时间暂停快捷键
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self._toggle_time_pause()

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            self.handle_input()  # 处理输入
            self.screen.fill((0, 0, 0))  # 清空画面
            game_state = self._get_game_state()  # 获取当前游戏状态

            # 新增：动态更新镜头位置
            self._update_camera()

            # 修改: 将敌人的信息传递给 render 方法
            self.display.render(game_state, self.screen, (self.camera_x, self.camera_y), self.player_moved, self.em)  # 将 entity_manager 传递给 render 方法

            # 新增：更新玩家属性窗口
            if self.use_player_info_window:
                self.info_window.update(game_state)

            # 将 info_screen 绘制到主窗口
            if self.use_player_info_window:
                self.info_window.draw()

            # 重置玩家移动标志
            self.player_moved = False

            pygame.display.flip()
            clock.tick(60)

    def _get_game_state(self):
        """获取当前游戏状态"""
        return {
            'map_data': self.current_level,
            'player_x': int(self.player.x),
            'player_y': int(self.player.y),
            'player': self.player,  # 添加player对象引用
            'entity_manager': self.em  # 新增：将 entity_manager 添加到游戏状态
        }

    def _update_camera(self):
        """动态更新镜头位置，智能处理地图边界"""
        # 基础参数
        tile_size = 32
        screen_width, screen_height = 1280, 720
        screen_tiles_x = screen_width // tile_size  # 40 tiles
        screen_tiles_y = screen_height // tile_size  # 22 tiles

        # 计算地图实际像素尺寸
        map_pixel_width = len(self.current_level[0]) * tile_size
        map_pixel_height = len(self.current_level) * tile_size

        # 智能镜头跟随逻辑（基于瓦片坐标）
        def calculate_camera_tiles(player_tile, map_tiles, screen_tiles):
            """基于瓦片坐标的镜头计算"""
            if map_tiles <= screen_tiles:
                return 0  # 小地图居中显示
            else:
                # 动态跟随，确保玩家始终在屏幕中心区域
                return max(0, min(
                    player_tile - screen_tiles // 2,
                    map_tiles - screen_tiles
                ))

        # 计算基于瓦片的镜头偏移
        camera_tile_x = calculate_camera_tiles(
            self.player.x,
            len(self.current_level[0]),
            screen_tiles_x
        )
        camera_tile_y = calculate_camera_tiles(
            self.player.y,
            len(self.current_level),
            screen_tiles_y
        )

        # 转换为像素坐标（注意符号取反）
        self.camera_x = -camera_tile_x * tile_size
        self.camera_y = -camera_tile_y * tile_size

    def _toggle_time_pause(self):
        # 实现时间暂停逻辑
        pass

    def _find_spawn_position(self, level_map):
        """找到一个合适的玩家初始生成位置"""
        for y, row in enumerate(level_map):
            for x, tile in enumerate(row):
                if tile == '.':  # 地板位置
                    return Player(x, y)  # 返回玩家对象
        raise ValueError("No valid spawn position found in the map")

    def _find_enemy_spawn_position(self, level_map):
        """找到一个合适的敌人初始生成位置"""
        for y, row in enumerate(level_map):
            for x, tile in enumerate(row):
                if tile == '.':  # 地板位置
                    return x, y
        raise ValueError("No valid enemy spawn position found in the map")


class Weapon:
    def __init__(self, base, modifier, mechanism=None):
        self.base = base
        self.modifier = modifier
        self.mechanism = mechanism

    def __repr__(self):
        return f"Weapon(base={self.base}, modifier={self.modifier}, mechanism={self.mechanism})"

class WeaponForge:
    def __init__(self):
        self.load_compatibility_matrix()

    def load_compatibility_matrix(self):
        with open("weapon_compatibility.json", "r") as file:
            self.matrix = json.load(file)

    def generate_weapon(self, parts):
        valid_combos = []
        for perm in itertools.permutations(parts):
            if self._validate_combo(perm):
                valid_combos.append(perm)

        if valid_combos:
            chosen = random.choice(valid_combos)
            return Weapon(
                base=chosen[0],
                modifier=chosen[1],
                mechanism=chosen[2] if len(chosen) > 2 else None
            )
        return None

    def _validate_combo(self, parts):
        for i in range(len(parts)):
            current = parts[i]
            for other in parts[i+1:]:
                if other in self.matrix.get(current, {}).get('conflicts', []):
                    return False
        return True