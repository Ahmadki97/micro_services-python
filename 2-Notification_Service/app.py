from server import elasticConnect, startQueues, startServer 
from logHandler import logger
import asyncio
import threading


def main():
    http_server_thread = threading.Thread(target=startServer)
    elastic_connect_thread = threading.Thread(target=elasticConnect)
    rabbit_queues_thread = threading.Thread(target=startQueues)
    http_server_thread.start()
    elastic_connect_thread.start()
    rabbit_queues_thread.start()

    

if __name__ == '__main__':
    main()