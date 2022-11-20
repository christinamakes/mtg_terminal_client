import zmq
import pyfiglet
import time
import os


def intro():
    hello_text = pyfiglet.figlet_format("Magic the Gathering")
    print(hello_text)
    print("****** Welcome to the Magic the Gathering Card Tool ******")
    print(
        "** From here you can search Magic cards and I will give you their information!"
    )
    print("** To search by name type 'name' or search by power type 'power'.")
    print("** Or type 'random' for a random card!\n")


def main_driver():
    bye_text = pyfiglet.figlet_format("See you later!")
    start_input = input(":")
    if start_input == "random":
        card_name = magic_rng_card()
        print(card_name)
        main_driver()
    if start_input == "exit":
        print(bye_text)
        exit
    else:
        print("I'm sorry I didn't recognize that command")
        time.sleep(1)
        main_driver()


def magic_rng_card():

    context = zmq.Context()

    #  Socket to talk to server
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")

    print("Getting your random card…")
    socket.send_string("Generating random card name...")

    #  Get the reply.
    message = socket.recv()
    return message.decode("utf-8")


intro()
main_driver()
# card_name = magic_rng_card()
# print(card_name)
