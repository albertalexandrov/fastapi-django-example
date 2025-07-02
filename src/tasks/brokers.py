from faststream.redis import RedisBroker

from settings import settings

redis_broker = RedisBroker(f"redis://{settings.redis_broker.host}:{settings.redis_broker.port}")
