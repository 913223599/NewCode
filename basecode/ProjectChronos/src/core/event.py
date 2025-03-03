class EventBus:
    _subscriptions = {}

    @classmethod
    def subscribe(cls, event_type, callback):
        if event_type not in cls._subscriptions:
            cls._subscriptions[event_type] = []
        cls._subscriptions[event_type].append(callback)

    @classmethod
    def publish(cls, event_type, **data):
        for callback in cls._subscriptions.get(event_type, []):
            callback(**data)

# 定义标准事件类型
EVENT_PLAYER_MOVED = 'player_moved'
EVENT_ELEMENT_REACTION = 'element_reaction'
