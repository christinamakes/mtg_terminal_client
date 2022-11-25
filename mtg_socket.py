import time
import zmq
import requests

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

while True:
    #  Wait for next request from client
    message = socket.recv()
    print(message.decode("utf-8"))
    response = requests.get("https://api.scryfall.com/cards/random?q=set:khm")

    result = response.json()
    card_name = result["name"]
    print(card_name)

    #  Send reply back to client
    socket.send_string(card_name)
