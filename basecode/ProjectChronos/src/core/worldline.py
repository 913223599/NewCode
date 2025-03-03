import pickle
import zlib

import pygame


class WorldLine:
    def __init__(self, max_snapshots=5):
        self.snapshots = []
        self.max_snapshots = max_snapshots

    def capture(self, game_state):
        """ 压缩保存游戏状态 """
        compressed = zlib.compress(pickle.dumps(game_state))
        if len(self.snapshots) >= self.max_snapshots:
            self.snapshots.pop(0)
        self.snapshots.append(compressed)

    def restore(self, index=-1):
        """ 加载指定时间锚点 """
        if not self.snapshots:
            raise ValueError("No snapshots available")
        return pickle.loads(zlib.decompress(self.snapshots[index]))

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
        self.chaos_factor *= 1.15
