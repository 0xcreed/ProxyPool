import redis
from proxypool.error import PoolEmptyError
from proxypool.setting import HOST, PORT


class RedisClient(object):
    def __init__(self, host=HOST, port=PORT):
        self._db = redis.Redis(host, port)

    def get(self, count=1):
        """
        get proxies from redis
        """
        proxies = self._db.lrange("proxies", 0, count - 1)
        self._db.ltrim("proxies", count, -1)
        print(proxies)
        return proxies

    def put(self, proxy):
        """
        add proxy to right top
        """
        self._db.rpush("proxies", proxy)

    def put_many(self, proxies):
        """
        put many proxies to right
        """
        for proxy in proxies:
            self.put(proxy)

    def pop(self):
        """
        get proxy from right.
        """
        try:
            return self._db.rpop("proxies").decode('utf-8')
        except:
            raise PoolEmptyError

    @property
    def queue_len(self):
        """
        get length from queue.
        """
        return self._db.llen("proxies")

    def flush(self):
        """
        flush db
        """
        self._db.flushall()


if __name__ == '__main__':
    conn = RedisClient()
    print(conn.pop())
