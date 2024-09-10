from Helper_api.logHandler import logger
from Redis_Api.gateway_cach import GateWayCach
import socketio
import os 

chat_io = socketio.Client(logger=True)
gig_io = socketio.Client(logger=True)
order_io = socketio.Client()
sio = socketio.Server(logger=True)
gateway_cashe = GateWayCach()

# connect, disconnect, message. json are reserved events in socketio
        


@gig_io.on(event='getLoggedInUsers')
def getLoggedInUsers():
        response = gateway_cashe.getLoggedInUsersFromCash('loggedInUsers')
        gig_io.emit('online', response)

    
@gig_io.on(event='loggedInUsers')
def logInUsers(username):
    response = gateway_cashe.saveLoggedInUserToCash('LoggedInUsers', username)
    gig_io.emit('online', response)


@gig_io.on(event='removeLoggedInUser')
def removeLoggedInUser(username):
    response = gateway_cashe.removeLoggedOutUserFromCash(key=username)
    gig_io.emit('online', response)


@gig_io.on(event='category')
def category(category, username):
    response = gateway_cashe.saveUserSelectedCategory(key=f"selectedCategories{username}", value=category)
    gig_io.emit('online', response)

################################################# Chat Service Socket ########################################################################

@chat_io.on('connect')
def chatIoConenct():
    logger.info('Chat Service Socket Connected.')

@chat_io.on('disconnect')
def chatIoDisconnect():
    logger.error(f"Chat Service Disconected")

@chat_io.on('message received')
def recieveMessage(message):
    print(f"chat socketio Recieved message, {message}")
    sio.emit(event='message recieved', data=message)



@chat_io.on('message updated')
def updateMessage(message):
     print(f"chat socketio Received message {message}")
     sio.emit(event='message updated', data=message)



####################################################################################

@order_io.on('connect')
def orderIoConnect():
     logger.info(f"Order Service Socket IO Connected.")


@order_io.on('disconnect')
def orderIoDisconnect():
     logger.info(f"Order Service Socket IO Disconnected")
     