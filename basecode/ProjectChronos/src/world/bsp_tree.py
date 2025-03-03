# bsp_tree.py
import random

class Room:
    def __init__(self, x, y, w, h):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h
        self.center = (x + w // 2, y + h // 2)

class BSPNode:
    def __init__(self, x, y, width, height, min_size=6):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.min_size = min_size
        self.left = None
        self.right = None
        self.sibling = None
        self.room = None

    def split_recursive(self, depth=5):
        if depth <= 0 or (self.width < self.min_size*2 and self.height < self.min_size*2):
            return

        # 随机选择分割方向
        split_horizontal = random.choice([True, False])
        if self.width / self.height > 1.25:
            split_horizontal = False
        elif self.height / self.width > 1.25:
            split_horizontal = True

        if split_horizontal:
            split = random.randint(self.min_size, self.height - self.min_size)
            self.left = BSPNode(self.x, self.y, self.width, split, self.min_size)
            self.right = BSPNode(self.x, self.y + split, self.width, self.height - split, self.min_size)
        else:
            split = random.randint(self.min_size, self.width - self.min_size)
            self.left = BSPNode(self.x, self.y, split, self.height, self.min_size)
            self.right = BSPNode(self.x + split, self.y, self.width - split, self.height, self.min_size)

        if self.left and self.right:
            self.left.sibling = self.right
            self.right.sibling = self.left
            self.left.split_recursive(depth-1)
            self.right.split_recursive(depth-1)

    def get_leaves(self):
        if self.left or self.right:
            return self.left.get_leaves() + self.right.get_leaves()
        return [self]

    def create_room(self):
        # 在叶节点内随机生成房间
        room_w = random.randint(self.min_size, self.width - 2)
        room_h = random.randint(self.min_size, self.height - 2)
        x = self.x + random.randint(1, self.width - room_w - 1)
        y = self.y + random.randint(1, self.height - room_h - 1)
        self.room = Room(x, y, room_w, room_h)
        return self.room

    def create_corridor(self, other):
        # 连接两个兄弟节点的中心点
        x1, y1 = self.room.center
        x2, y2 = other.room.center
        return Room(min(x1, x2), min(y1, y2), abs(x1 - x2) + 1, abs(y1 - y2) + 1)