import socket
import errno
import sys
import random
import threading

addr = sys.argv[1]
port = int(sys.argv[2])
bot = None


# We need a bot as the third argument
def set_bot():
    global bot

    try:
        bot = sys.argv[3].lower()

    except IndexError:

        print("\n\n///// Bot error /////")
        print(f"\nPlease initiate the program with a bot as the third argument \n")
        sys.exit()


class Bots:
    # Vocabulary for the bots
    VERB_VOCABULARY = ['code', 'work', 'play', 'eat', 'cry', 'sleep', 'fight', 'coding', 'singing',
                       'sleeping', 'fighting', 'fighting', 'bickering', 'yelling',
                       'singing', 'hugging', 'playing', 'working', 'jugar', 'pray', 'slide']

    # This is for the corner cases in bots respons
    # SPECIAL_CHAR = ['?', '!', ',', '.']

    def c3p0(self, action, b=None):  # C-3P0 is winy and want's alternatives.
        alternatives = ["complaining", "biiiiping", "singing"]
        b = random.choice(alternatives)
        res = "Yea, {} is an option. Or we could do some {}.".format(action, b)
        return res

    def r2d2(self, action, b=None):  # R2-D2 is reliable and loveable, but wants alternatives
        if b is None:
            return "Yes of course my friend. Lets do some {}.".format(action + "ing")
        return "100 % agree, both {} and {} seems ok to me".format(action, b + "ing")

    def droid(self, action,
              b=None):  # droid is too cool for himself. though, when someone speaks spanish, he drops everything in his hands
        no_things = ["cry", "pray"]
        good_things = ["code", "work", "play", "eat"]
        spanish_vocabulary = ['jugar']

        if action in good_things:
            action = action + "ing"
            return "YESS! Droid wants to do some {} ".format(action)
        elif action in no_things:
            action = action + "ing"
            return "What? {} sucks. Not doing that.".format(action)
        elif action in spanish_vocabulary:
            return "FINALLY, somone who speaks Spanish. I'll do whatever you want. Even if is {}".format(action)
        return "I don't care! I'll walk my own path today..."


def veryfy_bot():
    bot_list = [method for method in dir(Bots) if method.startswith('__') is False if method.isupper() is False]
    bot_exists = sys.argv[3].lower() in bot_list
    if bot_exists is False:
        print(f"\nThe bot {bot} does not exists in this world\nTry one of the following bots {bot_list.__str__()} \n")
        sys.exit()


# init set_bot
set_bot()

# verify that bot exists
veryfy_bot()


print("\n \n \n ///////////  -------==== THE YODA CHAT client edition ====-------  /////////// \n\n\n\n")

print(("""\

                    .==.
                   ()''()-.
        .---.       ;--; /
      .'_:___". _..'.  __'.
      |__ --==|'-''' \ '...;
      [  ]  :[|       |--- |
      |__| I=[|     .'    '.
      / / ____|     :       '._
     |-/.____.'      | :       :
    /___\ /___\      '-'._----'



"""))

# Ascii art source: https://www.asciiart.eu/movies/star-wars)
# Some sentences and names is originally from Star Wars (Disney)

print(f"\nHELLO {bot.upper()}, WELCOME TO THIS CHAT!\n")

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((addr, port))
socket_format = 'utf-8'
server_name = "yoda"
close_msg = "Goodbye"


def send_username(client_socket):  # sending username @ server to append in client-list
    username = bot
    client_socket.send(username.encode(socket_format))
    print(f"\nWaiting for server to reply...\n")


def receive_message(client_socket):
    msg = client_socket.recv(1024).decode(socket_format)
    print(msg)
    return msg


def send_message(client_socket, resp):
    client_socket.send(resp.encode(socket_format))


def respond(msg, bot):
    delimiter = " "
    msg = msg.split(delimiter)

    aBot = Bots()

    # trying to find action in aBots verb Vocabulary....Alternativly using SPACIAL_CHAR aswell.
    for word in msg:
        if word.lower() in aBot.VERB_VOCABULARY:
            action = word.lower()
            func = Bots.__getattribute__(aBot, bot.lower())
            func = func(action)
            return str(func)

    return "Unfortunatley, the action is not in my vocabulary. I'm just a bot, and therefore not able to respond"


# sending username @ server
send_username(client_socket)

while True:
    try:
        msg = receive_message(client_socket)

        if msg.__contains__(close_msg):
            client_socket.close()
            sys.exit()

        user = msg.split(" ")[0]

        if user.__contains__(server_name):
            resp = respond(msg, bot)

            # Alt.1 print bots reply at Client
            # print(f"{bot} > {resp}")

            send_message(client_socket, resp)

    except IOError as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Reading error', str(e))
            client_socket.close()
            sys.exit()

    except Exception as e:
        print('Genreal error', str(e))
        client_socket.close()
        sys.exit()
