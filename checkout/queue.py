from rq import Queue, Retry  # NOQA

from redis import Redis

redis = Redis(
    host="redis",
    port=6379,
)

queue = Queue(connection=redis)
