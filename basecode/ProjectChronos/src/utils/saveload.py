# src/utils/saveload.py
import datetime
import pickle


class GameSaveManager:
    SAVE_SLOTS = 5
    SAVE_DIR = "saves"

    def save_game(self, game_state, slot):
        """二进制压缩存档格式"""
        save_data = {
            'player': (game_state.player.x, game_state.player.y),
            'map': self._compress_map(game_state.current_level),
            'timestamp': datetime.now().isoformat(),
            'checksum': self._generate_checksum(game_state)
        }

        with open(f"{self.SAVE_DIR}/save_{slot}.dat", 'wb') as f:
            pickle.dump(save_data, f, protocol=pickle.HIGHEST_PROTOCOL)

    def _compress_map(self, map_data):
        """RLE地图压缩算法"""
        compressed = []
        current = map_data[0][0]
        count = 1
        for row in map_data:
            for tile in row:
                if tile == current:
                    count +=1
                else:
                    compressed.append((current, count))
                    current = tile
                    count = 1
        return compressed
