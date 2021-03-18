import random
import socket
import sys
import select
import threading
import time

addr = 'localhost'
port = int(sys.argv[1])

# alt is to use sys.argv[3].lower() set the bot and verify it like the client side
bot = "yoda"

VERB_VOCABULARY = ['work', 'play', 'eat', 'cry', 'sleep', 'fight', 'pray', 'slide']
WISDOM_VOCABULARY = ['code']
SPANISH_VOCABULARY = ['jugar']
DAILY_MOOD = ['happy', 'wise', 'nonchalant', 'spanish']
GREEET = ['Hello', 'Hola', 'Olleh', 'Listen' ]


def GREETINGS(mood):
    action = random.choice(VERB_VOCABULARY)
    wisdom_action = random.choice(WISDOM_VOCABULARY)
    spanish_action = random.choice(SPANISH_VOCABULARY)
    if mood == "happy":
        return "Come! My dear friends, do you guys want to {} with me?".format(action)
    elif mood == "wise":
        return "Would you like to {} with me? Do or do not. There is no try.".format(wisdom_action)
    elif mood == "nonchalant":
        return "i'm to cool for you robots, but anyway do you robots wanna {} today?".format(action)
    return "Por favor chicos, vamonos a {} hoy!".format(spanish_action)


def yoda(self, b=None):
    mood = random.choice(DAILY_MOOD)
    greet = random.choice(GREEET)
    message = f"{greet} robots. i'm feeling {mood} now. "
    return message + GREETINGS(mood)


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Let us reconnect
server_socket.bind((addr, port))
server_socket.listen()

utf_format = 'utf-8'
USERNAME_LENGHT = 10
chatRoomSize = 3
sockets_list = [server_socket]
clients = {}
signature = (("""\n\n\n
                    ____
                 _.' :  `._
             .-.'`.  ;   .'`.-.
    __      / : ___\ ;  /___ ; \      __
  ,'_ ""--.:__;".-.";: :".-.":__;.--"" _`,
  :' `.t""--.. '<@.`;_  ',@>` ..--""j.' `;
       `:-.._J '-.-'L__ `-- ' L_..-;'
         "-.__ ;  .-"  "-.  : __.-"
             L ' /.------.\ ' J
              "-.   "--"   .-"
             __.l"-:_JL_;-";.__
          .-j/'.;  ;  / .'\¨-.
        .' /:`. "-.:     .-" .';  `.
     .-"  / ;  "-. "-..-" .-"  :    "-.
  .+"-.  : :      "-.__.-"      ;-._   |
  ; \  `.; ;                    : : "+. ;
  :  ;   ; ;                    : ;  : \:
 : `."-; ;  ;                  :  ;   ,/;
  ;    -: ;  :                ;  : .-"'  :
  :\     \  : ;             : \.-"      :
   ;`.    \  ; :            ;.'_..--  / ;
   :  "-.  "-:  ;          :/."      .'  :
     \       .-`.\        /t-""  ":-+.   :
      `.  .-"    `l    __/ /`. :  ; ; \  ;
        \   .-" .-"-.-"  .' .'j \  /   ;/
         \ / .-"   /.     .'.' ;_:'    ;
          :-""-.`./-.'     /    `.___.'
                \ `t  ._  /
                 "-.t-._"
"""))

# Ascii art source: https://www.asciiart.eu/movies/star-wars)
# Some sentences and names is originally from Star Wars (Disney)

print("\n \n \n ///////////  -------==== THE YODA CHAT server edition ====-------  /////////// \n\n\n\n")


def accept_sockets():
    while len(sockets_list) <= chatRoomSize:
        client_socket, client_address = server_socket.accept()
        sockets_list.append(client_socket)
        user = get_username(client_socket)

        if user is False:
            continue

        clients[client_socket] = user
        print(f"\n:::::::: {user} just rolled into the room ::::::::   \nSOCKET INFO: {client_address[0]}:{client_address[1]} \n")


def disconnected_socket(thisSocket):
    message= f"\n\n\nUnfortunately, {clients[thisSocket]} just logged out. Closing connection."
    print(message)
    sockets_list.remove(thisSocket)
    del clients[thisSocket]
    broadcast_message(user, message, False)
    close_server()


def message_format(user, message):
    return f"\n{user} > {message}"


def broadcast_message(user, message, welcomeMessage):  # THIS SOCKET

    if welcomeMessage is True and user == "yoda":
        message = globals()[user.lower()](user)
        message = str(message)
        print(f"\n<<<<<<<< SERVER SENDS MESSAGE >>>>>>>>> {message_format(user, message)}  ")

    for socket in clients:
        # I´ve chose to print all the replies, including the sender (thisSocket)
        # if socket != thisSocket:
        socket.send(message_format(user, message).encode(utf_format))


def recceive_message(client_socket, user):
    time.sleep(3)
    message = client_socket.recv(1024).decode(utf_format)

    if not len(message):
        return False

    print(f"\n<<<<<<<< SERVER RECEIVES MESSAGE >>>>>>>>> {message_format(user, message)}")
    return message


def get_username(client_socket):
    msg = client_socket.recv(USERNAME_LENGHT).decode(utf_format)
    username = msg
    return username.__str__()


def close_server():
    message = "Before i go... Many of the truths that we cling to depend on our point of view....\n\n"
    message += signature.__str__()
    message += "\n\n\nGoodbye robots....\n\n\n"
    time.sleep(2)

    broadcast_message(bot, message, False)

    print("\n\n\n\n::::::::::::: SERVER IS CLOSING :::::::::::::\n\n\n")
    time.sleep(2)

    for closingSocket in sockets_list:
        sockets_list.remove(closingSocket)
        # del clients[closingSocket]

    server_socket.close()
    sys.exit()


def intro():
    print("\n\n\nBefore we start off.....")
    counterFromUser = input("choose number of chat rounds   :   ")
    while type(counterFromUser) is not int:
        try:
            counterFromUser = int(counterFromUser)
            break
        except ValueError as v:
            counterFromUser = input("Try again   :   ")

    return counterFromUser

counter = 1
i = intro()
time.sleep(1)
print("\n\n\nWELCOME//////////////////////////////////////////////////")
time.sleep(3)
print(signature)
time.sleep(3)
print("\n\n\nwaiting for the bots to join.....")
print("\n\n\n\n/////////////////////////////////////////////////\n\n\n\n")

while counter <= i:
    # while counter <= 3

    # alternative with select
    #all_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)

    for thisSocket in sockets_list:

        if thisSocket == server_socket:
            accept_sockets()

            print(f"\n\n\n ----==== CHAT ROUND NO: {counter} ===---\n\n")

            #alternative without thread
            #broadcast_message(bot, None, True)

            # alternative with threads
            thread_client = threading.Thread(target=broadcast_message, args=[bot, None, True])
            thread_client.start()

        else:
            user = clients[thisSocket]
            message = " "
            thisSocket.settimeout(8)
            try:
                message = recceive_message(thisSocket, user)
                if message is False:
                    disconnected_socket(thisSocket)
            except socket.timeout:
                disconnected_socket(thisSocket)



            #alternative without thread
            #broadcast_message(user, message, False)

            # alternative with threads
            thread_client = threading.Thread(target=broadcast_message, args=[user, message, False])
            thread_client.start()

    counter += 1
close_server()
