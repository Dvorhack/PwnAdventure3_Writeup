import socket, os, Protocol_Parser, sys
from threading import Thread
import importlib

class Proxy(Thread):
    def __init__(self, from_host, to_host, port):
        super(Proxy, self).__init__()
        self.from_host = from_host
        self.to_host = to_host
        self.port = port

    def run(self):
        while True:
            print(f"[proxy({self.port})] setting up")
            self.c2p = Client2Proxy(self.from_host, self.port) # waiting for a client
            self.p2s = Proxy2Server(self.to_host, self.port)
            print(f"[proxy({self.port})] connection established")

            # Exchange file descriptor
            self.c2p.server = self.p2s.server
            self.p2s.client = self.c2p.client

            self.c2p.start()
            self.p2s.start()

class Client2Proxy(Thread):
    def __init__(self, host, port):
        super(Client2Proxy, self).__init__()
        self.server = None # real server socket not known yet
        self.port = port
        self.host = host
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((host, port))
        sock.listen(1)
        # waiting for a connection
        self.client, addr = sock.accept()
    
    def run(self):
        while True:
            try:
                data = self.client.recv(4096)
                if data:
                    # First, display data
                    #print(f"[{self.port}] -> {data[:100].hex()}")

                
                    importlib.reload(Protocol_Parser)        
                    Protocol_Parser.parse(data, self.port, 'client')
                self.server.sendall(data)
            except Exception as e:
                print ('client[{self.port}]', e)
                # forward to server
                exit()

            # Then, send data to real server
            


class Proxy2Server(Thread):
    def __init__(self, host, port):
        super(Proxy2Server, self).__init__()
        self.client = None # game client socket not known yet
        self.port = port
        self.host = host
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connect((host, port))

    # run in thread
    def run(self):
        while True:
            try:
                data = self.server.recv(4096)
                if data:
                    # First, display data
                    #print(f"[{self.port}] <- {data[:100].hex()}")

                    importlib.reload(Protocol_Parser)                        
                    Protocol_Parser.parse(data, self.port, 'server')
                self.client.sendall(data)
            except Exception as e:
                print(f'server[{self.port}]', e)
                # forward to client
                exit()

                # Then, send data to real server
                

    

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: python3 {sys.argv[0]} <server ip>")
    else:
        SERVER_IP = sys.argv[1]
    SERVER_IP = 'pentest.hackutt.uttnetgroup.fr'    
    MASTER_PORT = 3333

    

    master_server = Proxy('0.0.0.0', SERVER_IP, MASTER_PORT)
    master_server.start()

    game_servers = []
    for port in range(3000, 3006):
        _game_server = Proxy('0.0.0.0', SERVER_IP, port)
        _game_server.start()
        game_servers.append(_game_server)


    while True:
        try:
            cmd = input('$ ')
            if cmd[:4] == 'quit':
                os._exit(0)
        except Exception as e:
            print(e)
