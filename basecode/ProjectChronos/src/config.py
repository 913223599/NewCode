# 窗口与网格配置
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
CELL_SIZE = 32

# 元素浓度阈值
ELEMENT_THRESHOLDS = {
    'fire': 0.8,
    'chaos': 0.75,
    'entropy': 0.9,
    'water': 0.6,  # 新增水元素
    'wind': 0.5,  # 新增风元素
    'earth': 0.4  # 新增土元素
}

# 武器组合兼容性文件路径
WEAPON_DATA_PATH = "assets/data/weapon_compatibility.json"