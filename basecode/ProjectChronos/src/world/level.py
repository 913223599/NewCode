import random

from perlin_noise import PerlinNoise

from .bsp_tree import BSPNode  # 修改为正确的相对导入路径

TERRAIN_FEATURES = {
    'cave': ['~', '♣', '', 'S'],
    'dungeon': ['', '', '', ''],
    'forest': ['♣', '', '', ''],
    'grassland': ['.', '.', '', ''],
    'desert': ['.', '', '', ''],
    'swamp': ['.', '~', '', '']
}


class LevelGenerator:
    MIN_DIMENSION = 10  # 假设已经定义了最小尺寸常量
    DEFAULT_BIOME = 'cave'  # 假设已经定义了默认生态类型常量
    MAX_RETRIES = 15  # 设置最大重试次数为15

    def generate_map(cls, width: int = 120, height: int = 60, biome: str = 'cave', view_width: int = 40,
                     view_height: int = 20) -> list:
        """支持不同生态的地图生成"""
        # 参数有效性验证
        if not (isinstance(width, int) and isinstance(height, int) and isinstance(view_width, int) and isinstance(
                view_height, int)):
            raise ValueError("Width, height, view_width, and view_height must be integers")
        if width < cls.MIN_DIMENSION or height < cls.MIN_DIMENSION or view_width < cls.MIN_DIMENSION or view_height < cls.MIN_DIMENSION:
            raise ValueError(f"Minimum dimension size is {cls.MIN_DIMENSION}")

        # 构建生成方法映射表
        biome_handlers = {
            'cave': cls._generate_caves,
            'dungeon': cls._generate_dungeon,
            'forest': cls._generate_forest,
            'grassland': cls._generate_grassland,
            'desert': cls._generate_desert,
            'swamp': cls._generate_swamp
        }

        # 选择生成方法并处理未知生态类型
        generate_method = biome_handlers.get(biome)
        if not generate_method:
            generate_method = cls._generate_caves
            # 添加未知生态类型警告
            import warnings
            warnings.warn(f"Unknown biome type: {biome}, using default: {cls.DEFAULT_BIOME}")

        # 循环重试机制替代递归
        retry_count = 0
        while retry_count < cls.MAX_RETRIES:
            try:
                map_data = generate_method(width, height)
                map_data = cls.add_special_features(map_data, biome)

                if cls.validate_map(map_data):
                    return map_data

                retry_count += 1
            except Exception as e:
                raise RuntimeError(f"Map generation failed: {str(e)}") from e

        raise RuntimeError(f"Failed to generate valid map after {cls.MAX_RETRIES} attempts")

    @classmethod
    def _generate_caves(cls, width, height):
        """ 使用醉汉走路生成洞穴并优化 """
        # 类常量定义
        drunkard_steps = 10000  # 增加醉汉走路步数
        room_spawn_min = 15  # 最小房间数量
        room_spawn_max = 25  # 最大房间数量
        room_spawn_chance = 0.6  # 增加房间生成概率
        cellular_iterations = 15  # 增加元胞自动机迭代次数
        directions = [(-1, -1), (-1, 0), (-1, 1),
                      (0, -1), (0, 1),
                      (1, -1), (1, 0), (1, 1)]  # 8方向移动

        map_data = [['#' for _ in range(width)] for _ in range(height)]
        x, y = (width // 2, height // 2)  # 使用元组存储坐标

        # 醉汉走路阶段
        for _ in range(drunkard_steps):
            dx, dy = random.choice(directions)
            x = max(1, min(width - 2, x + dx))
            y = max(1, min(height - 2, y + dy))
            map_data[y][x] = '.'

        # 元胞自动机平滑阶段
        for _ in range(cellular_iterations):
            new_map_data = [['#' for _ in range(width)] for _ in range(height)]
            for y in range(1, height - 1):
                for x in range(1, width - 1):
                    neighbors = sum(map_data[ny][nx] == '.' for nx, ny in [(x + dx, y + dy) for dx, dy in directions])
                    if map_data[y][x] == '.' and neighbors >= 5:
                        new_map_data[y][x] = '.'
                    elif map_data[y][x] == '#' and neighbors >= 4:
                        new_map_data[y][x] = '.'
        map_data = new_map_data

        # 房间生成阶段
        room_count = random.randint(room_spawn_min, room_spawn_max)
        rooms = []
        for _ in range(room_count):
            room_width = random.randint(3, 8)
            room_height = random.randint(3, 8)
            room_x = random.randint(1, width - room_width - 1)
            room_y = random.randint(1, height - room_height - 1)
            for ry in range(room_y, room_y + room_height):
                for rx in range(room_x, room_x + room_width):
                    map_data[ry][rx] = '.'
            rooms.append((room_x, room_y, room_width, room_height))

        # 连接房间
        for i in range(len(rooms) - 1):
            room1 = rooms[i]
            room2 = rooms[i + 1]
            # 创建走廊连接两个房间
            x1, y1, w1, h1 = room1
            x2, y2, w2, h2 = room2
            # 选择房间中心点
            center1_x = x1 + w1 // 2
            center1_y = y1 + h1 // 2
            center2_x = x2 + w2 // 2
            center2_y = y2 + h2 // 2
            # 创建水平走廊
            for x in range(min(center1_x, center2_x), max(center1_x, center2_x) + 1):
                map_data[center1_y][x] = '.'
            # 创建垂直走廊
            for y in range(min(center1_y, center2_y), max(center1_y, center2_y) + 1):
                map_data[y][center2_x] = '.'

        print(f"Generated cave map with {room_count} rooms")
        return map_data

    @classmethod
    def _generate_dungeon(cls, width, height):
        """ BSP树生成地牢 """
        root_node = BSPNode(0, 0, width, height)
        root_node.split_recursive()

        map_data = [['#' for _ in range(width)] for _ in range(height)]
        rooms = []
        for node in root_node.get_leaves():
            room = node.create_room()
            rooms.append(room)
            for y in range(room.y1, room.y2):
                for x in range(room.x1, room.x2):
                    map_data[y][x] = '.'

        # 连接房间
        for i in range(len(rooms) - 1):
            room1 = rooms[i]
            room2 = rooms[i + 1]
            corridor = root_node.create_corridor(room1, room2)  # 确保使用正确的节点创建走廊
            for y in range(corridor.y1, corridor.y2):
                for x in range(corridor.x1, corridor.x2):
                    map_data[y][x] = '.'

        print("Generated dungeon map")
        return map_data

    @classmethod
    def _generate_forest(cls, width, height):
        """ 使用 Perlin noise 生成森林地形 """
        map_data = [['#' for _ in range(width)] for _ in range(height)]
        noise_gen = PerlinNoise(octaves=6, seed=random.randint(0, 100))
        scale = 10.0
        for y in range(height):
            for x in range(width):
                n = noise_gen([x / scale, y / scale])
                if n > 0.3:
                    map_data[y][x] = '.'
                if n > 0.5:
                    map_data[y][x] = '♣︎'
        print("Generated forest map")
        return map_data

    @classmethod
    def _generate_grassland(cls, width, height):
        """ 生成草原地形 """
        map_data = [['#' for _ in range(width)] for _ in range(height)]
        for y in range(height):
            for x in range(width):
                if random.random() < 0.8:
                    map_data[y][x] = '.'
        print("Generated grassland map")
        return map_data

    @classmethod
    def _generate_desert(cls, width, height):
        """ 生成沙漠地形 """
        map_data = [['#' for _ in range(width)] for _ in range(height)]
        for y in range(height):
            for x in range(width):
                if random.random() < 0.7:
                    map_data[y][x] = '.'
                elif random.random() < 0.1:
                    map_data[y][x] = '~'  # 沙漠中的水源
        print("Generated desert map")
        return map_data

    @classmethod
    def _generate_swamp(cls, width, height):
        """ 生成沼泽地形 """
        map_data = [['#' for _ in range(width)] for _ in range(height)]
        for y in range(height):
            for x in range(width):
                if random.random() < 0.6:
                    map_data[y][x] = '.'
                elif random.random() < 0.2:
                    map_data[y][x] = '~'  # 沼泽中的水域
        print("Generated swamp map")
        return map_data

    @classmethod
    def add_special_features(cls, map_data, biome):
        """ 添加生态特征要素 """
        features = [f for f in TERRAIN_FEATURES.get(biome, []) if f]  # 过滤空字符串
        if not features:
            return map_data

        height = len(map_data)
        width = len(map_data[0]) if height > 0 else 0

        for _ in range(len(map_data) * len(map_data[0]) // 20):
            x = random.randint(1, width - 2)
            y = random.randint(1, height - 2)
            if map_data[y][x] == '.':
                map_data[y][x] = random.choice(features)

        print(f"Added {len(features)} types of features to {biome} map")
        return map_data

    @classmethod
    def validate_map(cls, map_data):
        """ 使用洪水填充算法验证地图连通性 """
        start = (1, 1)
        visited = set()
        queue = [start]

        # 修改判断条件：仅允许 '.' 地块作为可通行区域
        while queue:
            x, y = queue.pop(0)
            if (x, y) in visited:
                continue
            visited.add((x, y))

            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < len(map_data[0]) and 0 <= ny < len(map_data):
                    # 修改判断条件：map_data[ny][nx] == '.' 代替 != '#'
                    if map_data[ny][nx] == '.' and (nx, ny) not in visited:
                        queue.append((nx, ny))

        accessible = len(visited)
        total = sum(row.count('.') for row in map_data)

        # 添加空地图保护
        if total == 0:
            print("Error: No valid floor tiles generated")
            return False

        validity = accessible / total > 0.7
        print(
            f"Validation: {accessible}/{total} ({accessible / total * 100:.1f}%) {'Valid' if validity else 'Invalid'}")
        return validity
