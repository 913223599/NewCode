# Project Chronos 设计纲要
> "每一次死亡都是对世界法则的重新定义"

## 一、核心元规则
### 1.1 时间锚点系统
- **死亡重置**：玩家死亡时触发 `WorldLine.reset(保留参数=[记忆碎片,元素熵值])`
- **蝴蝶效应**：微小选择改变未来分支概率权重（使用马尔可夫链模型）

### 1.2 元素守恒定律
``` python
class WorldState:
    def __init__(self):
        self.elements = { # 元素浓度实时影响世界
            'fire': 0.0, # 影响：技能强度/环境温度
            'entropy': 0.0, # 影响：随机事件触发率
            'chaos': 0.0 # 超过阈值触发维度崩塌 }
```

## 二、核心系统交互图
``` mermaid
graph TD
    A[玩家行为] --> B{元素释放}
    B -->|火+油| C[爆炸反应]
    B -->|电+水| D[传导麻痹]
    C --> E[改变地形状态]
    D --> F[触发敌人异常状态]
    E --> G[环境熵值增加]
    F --> H[AI学习应对策略]
    G --> I[混沌事件触发]
    H --> J[生成玩家镜像]

```

## 三、关键技术实现备忘
### 3.1 武器变形系统
- **组件池**：`Weapon = Base(类型) + Modifier(元素) + Mechanism(特殊效果)`
- **实时重构算法**：

``` python
def reforge_weapon(parts):
    # 输入示例：['flamethrower_nozzle', 'cryo_core']
    compatibility_matrix = load_json('weapon_compatibility.json')
    valid_combos = check_compatibility(parts, compatibility_matrix)
    return random.choice(valid_combos) if valid_combos else None
```
### 3.2 因果律道具系统
| 道具ID            | 效果        | 副作用          |
|-----------------|-----------|--------------|
| #chronos_anchor | 创建时间锚点    | 世界线变动率+15%   |
| #observer_lens  | 预渲染未来5秒画面 | 后续30秒内遭遇量子幽灵 |

### 3.3 动态难度曲线
``` python
def calculate_difficulty(player):
    """ 基于玩家历史表现的动态难度 """
    aggression = player.kills_per_minute
    survival = player.avg_survival_time
    return (aggression * 0.7 + survival * 0.3) * chaos_factor
```

## 四、待解决问题（TODO）
1. [ ] **元素过载悖论**：当四元素同时满浓度时的稳定状态模拟
2. [ ] **克莱因瓶走廊**：非欧几何空间的路径寻优算法优化
3. [ ] **AI镜像生成**：使用轻量化LSTM模拟玩家行为模式（需测试性能消耗）

## 五、美术资源需求表
| 资源类型             | 规格要求          | 元数据标记     |
|:-----------------|---------------|-----------|
| #character_sheet | 32x32px 含8方向帧 | 必须包含元素染色区 |
| #tileset         | 支持16层叠加的PNG序列 | 需标注可交互属性  |
| #effect_glitch   | 至少包含10种故障艺术变体 | 按熵值强度分级   |

## 六、叙事触发逻辑

``` python
class StoryManager:
    def __init__(self):
        self.fragments = { # 记忆碎片触发条件
            'fragment_01': lambda w: w.elements['chaos'] > 0.3,
            'fragment_02': lambda w: w.player.death_count >= 5
        }
    def check_triggers(self, world_state):
        return [k for k, v in self.fragments.items() if v(world_state)]
```

## 七、跨周目继承协议
``` json
{
    "persistent_data": {
        "memory_fragments": "加密存储",
        "material_evolution": {
            "unused_items": {
                "healing_potion":
                {"count": 3, "evolution_stage": 2}
            }
        },
        "ai_learning_data":
        "差分存储（仅记录行为模式变化）"
    }
}
```

**校验码**：`CHRONOS_v0.1.3_8B4E2A`  
**警告**：本文档包含时间悖论诱发内容，阅读时请确保所在世界线的休谟指数≥1.2