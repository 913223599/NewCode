class System:
    """ 系统基类 """
    def __init__(self, entity_manager):
        self.em = entity_manager

    def update(self, dt: float):
        """ 每帧更新逻辑 """
        raise NotImplementedError
