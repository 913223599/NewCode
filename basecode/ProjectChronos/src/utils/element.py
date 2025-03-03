class ElementEngine:
    def __init__(self):
        # 初始化 reactions 属性（合并为单次字典定义）
        self.reactions = {
            'fire_water': {
                'result': 'steam',
                'effect': 'steam_cloud',
                'duration': 5,
                'damage': 2
            },
            'electric_fire': {
                'result': 'plasma',
                'effect': 'explosion',
                'duration': 3,
                'damage': 10
            },
            'earth_water': {
                'result': 'mud',
                'effect': 'slow',
                'duration': 8,
                'slow_amount': 0.7
            }
        }


    def apply_environment_effect(self, reaction, position, game_map):
        """ 扩展环境效果处理 """
        effect_type = reaction['effect']
        duration = reaction['duration']

        if effect_type == 'burning_ground':
            # 燃烧地面持续伤害
            game_map.set_tile_effect(
                position,
                effect={
                    'type': 'fire',
                    'damage': 5,
                    'duration': duration,
                    'graphic': '🔥'
                }
            )
        elif effect_type == 'conductive':
            # 导电区域连锁反应
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                x = position[0] + dx
                y = position[1] + dy
                if game_map.is_within_bounds(x, y):
                    game_map.set_tile_effect(
                        (x, y),
                        effect={
                            'type': 'electric',
                            'stun': True,
                            'duration': duration // 2,
                            'graphic': '⚡'
                        }
                    )
        elif effect_type == 'freezing':
            # 新增冰冻效果
            game_map.set_tile_effect(
                position,
                effect={
                    'type': 'ice',
                    'slow': 0.5,
                    'duration': duration,
                    'graphic': '❄️'
                }
            )
        elif effect_type == 'corrosive':
            # 新增腐蚀效果
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                x = position[0] + dx
                y = position[1] + dy
                if game_map.is_within_bounds(x, y):
                    game_map.set_tile_effect(
                        (x, y),
                        effect={
                            'type': 'acid',
                            'damage': 3,
                            'duration': duration,
                            'graphic': '☣️'
                        }
                    )
        # 新增蒸汽效果
        if effect_type == 'steam':
            game_map.set_tile_effect(
                position,
                effect={
                    'type': 'steam',
                    'obscure': True,
                    'duration': duration,
                    'graphic': '💨'
                }
            )
        # 新增磁力效果
        elif effect_type == 'magnetic':
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                x = position[0] + dx
                y = position[1] + dy
                if game_map.is_within_bounds(x, y):
                    game_map.set_tile_effect(
                        (x, y),
                        effect={
                            'type': 'magnetic',
                            'attract': True,
                            'duration': duration,
                            'graphic': '🧲'
                        }
                    )
        elif effect_type == 'steam_cloud':
            # 新增蒸汽云效果
            game_map.set_tile_effect(
                position,
                effect={
                    'type': 'steam',
                    'damage': reaction['damage'],
                    'duration': reaction['duration'],
                    'graphic': '💨',
                    'vision_block': True
                }
            )
        elif effect_type == 'explosion':
            # 新增爆炸效果
            for dx in range(-2, 3):
                for dy in range(-2, 3):
                    x = position[0] + dx
                    y = position[1] + dy
                    if game_map.is_within_bounds(x, y):
                        game_map.set_tile_effect(
                            (x, y),
                            effect={
                                'type': 'explosion',
                                'damage': reaction['damage'] // (abs(dx) + abs(dy) + 1),
                                'duration': reaction['duration'],
                                'graphic': '💥'
                            }
                        )
        elif effect_type == 'slow':
            # 新增减速效果
            game_map.set_tile_effect(
                position,
                effect={
                    'type': 'mud',
                    'slow': reaction['slow_amount'],
                    'duration': reaction['duration'],
                    'graphic': '坭'
                }
            )
    def check_reaction(self, element_a, element_b):
        key = tuple(sorted([element_a, element_b]))
        return self.REACTION_TABLE.get(key, None)

    def apply_reaction(self, reaction_data, target):
        """ 应用元素反应效果 """
        # 伤害计算
        target.take_damage(reaction_data['damage'])

        # 添加状态效果
        if reaction_data['effect']:
            target.add_status(
                effect=reaction_data['effect'],
                duration=reaction_data['duration']
            )

        # 环境改变（如地面燃烧）
        if reaction_data['effect'] == 'burning_ground':
            self.world.set_tile_effect(
                position=target.position,
                effect_type='fire',
                duration=reaction_data['duration']
            )
        """ 应用反应效果到目标 """
        # 示例实现
        target.health -= reaction_data['damage']
        print(f"{target.name} 受到 {reaction_data['damage']} 点 {reaction_data['effect']} 伤害")

