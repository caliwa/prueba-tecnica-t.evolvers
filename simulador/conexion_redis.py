from redis_om import get_redis_connection

#Conexión a DB Redis https://redis.io/
redis = get_redis_connection(
    host="redis-11940.c256.us-east-1-2.ec2.cloud.redislabs.com",
    port=11940,
    password="WJYgldne1Ummc8xYubF8j91BjzN1Z7uN",
    decode_responses=True
)