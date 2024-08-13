import redis
from django.conf import settings

TOKEN_EXPIRY_TIME = getattr(settings, 'TOKEN_EXPIRY_TIME', 60 * 30)

# Redis 클라이언트 인스턴스 가져오기
def get_redis_connection():
    redis_url = settings.CACHES['default']['LOCATION']
    return redis.StrictRedis.from_url(redis_url)

# Redis 클라이언트 인스턴스 생성
redis_client = get_redis_connection()

def add_token_to_blacklist(token):
    redis_client.sadd('blacklisted', token)
    redis_client.expire('blacklisted', TOKEN_EXPIRY_TIME)

def is_token_blacklisted(token):
    return redis_client.sismember('blacklisted', token)