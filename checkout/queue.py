from rq import Queue, Retry

from redis import Redis

redis = Redis(
    host="redis",
    port=6379,
)

queue = Queue(connection=redis)
