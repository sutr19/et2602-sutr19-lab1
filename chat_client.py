import sys
import socket
import re
import select


# Try the input
try:
    ARGS = str(sys.argv[1]).split(':')
    IP = str(ARGS[0])
    PORT = int(ARGS[1])
    NICK = sys.argv[2]
except Exception as e:
    print("Usage: python chat_client.py server_ip:server_port")
    sys.exit()
# Try protocol part 1 and protocol part 2
try:
    client = socket.socket()
    # connect to server
    client.connect((IP,PORT))
    hello = client.recv(1024).decode('ascii')
    print(hello)
    # Send nick and receive ok!
    nick = 'NICK '+NICK
    client.sendall(nick.encode('ascii'))
    ok = client.recv(1024).decode('ascii')
    print(ok)
except Exception as e:
    print("Not able to send the nick name data",e)
    sys.exit()
while True:
    sockets = [sys.stdin, client]
    readsockets, writesockets, errorsockets = select.select(sockets,[],[])
    for socket in sockets:
        if socket==client:
            try:
                msg = socket.recv(1024).decode('ascii')
                print(msg[4:])
            except Exception as e:
                print(msg)
        else:
            msg = sys.stdin.readline()
            if msg=='\n':
                continue
            else:
                message_to_send = 'MSG '+msg
                client.sendall((message_to_send).encode('ascii'))
client.close()

