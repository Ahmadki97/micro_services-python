import http.server
from consume import startConsumeAuthMail, startConsumeOrderMail
from elastic import checkConnection
from parameters import elasticsearch_url, SERVER_PORT
import os 
from logHandler import client, logger
import threading
import logging




def elasticConnect():
    print("Hello from elasticConnect()")
    checkConnection(client)

def startQueues():

    print("Hello from startQueues()")
    authmail_thread = threading.Thread(target=startConsumeAuthMail)
    ordermail_thread = threading.Thread(target=startConsumeOrderMail)
    authmail_thread.start()
    ordermail_thread.start()


def startServer():
    print("Hello from startServer()")
    try:
        server = http.server.HTTPServer(('localhost', SERVER_PORT), http.server.SimpleHTTPRequestHandler)
        logger.info(f"Worker with process id of {os.getpid()} on notification server has started")
        print((f"Worker with process id of {os.getpid()} on notification server has started"))
        server.serve_forever()
    except Exception as error:
        logger.error("NotificationService start_server() method:", error)
        logging.error("NotificationService start_server() method:", error)
