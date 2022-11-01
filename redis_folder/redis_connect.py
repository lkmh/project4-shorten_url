import redis
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


redis_host = os.environ.get('redis_host')
redis_pass = os.environ.get('redis_password')
redis_port = os.environ.get('redis_port')


redis_connection = redis.Redis(host=redis_host, port=redis_port, password=redis_pass)