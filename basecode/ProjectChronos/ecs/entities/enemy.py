class Enemy:
    def __init__(self, x, y, difficulty=1):
        self.x = x
        self.y = y
        self.difficulty = difficulty
        self.health = 100  # 假设敌人初始生命值为100

    def take_damage(self, damage):
        """默认的伤害处理方法"""
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            self.die()

    def die(self):
        """敌人死亡处理方法"""
        print("Enemy died")


# 添加 QuantumPhantom 类
class QuantumPhantom(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.phase_state = 0  # 0=实体, 1=虚化
        self.phase_timer = 0

    def update(self, dt):
        # 相位切换
        self.phase_timer += dt
        if self.phase_timer > 3000:  # 每3秒切换
            self.phase_state = 1 - self.phase_state
            self.phase_timer = 0

    def take_damage(self, damage):
        if self.phase_state == 1:
            return  # 虚化状态免疫伤害
        super().take_damage(damage)