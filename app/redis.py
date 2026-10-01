from .settings import settings
import redis

if not settings.redis_url:
    raise ValueError("REDIS_URL is not in the .env or incorrect")

redis_client = redis.Redis.from_url(settings.redis_url, decode_responses=True)

if __name__ == "__main__":
    try:
        redis_client.set("test_ping", "pong")
        result = redis_client.get("test_ping")
        print(f"Redis connection is successful: {result}")
    except Exception as e:
        print(f"Error occured while connecting redis: {e}")