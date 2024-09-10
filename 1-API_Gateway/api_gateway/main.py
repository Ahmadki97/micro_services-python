from server import gateWayServer
from Redis_Api.connection import redis_connection


server = gateWayServer()
server.start()
redis_connection.redisConnect()