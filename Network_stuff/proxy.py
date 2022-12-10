#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Authors: Dvorhack & K8pl3r

This file is aimed to provide a tcp proxy for different ports
"""

from threading import Thread
from tkinter import END
import os
import socket
import sys
import importlib
import Protocol_Parser
import gui

GUI = False
root = None


class Proxy(Thread):
    """
    Class that contains one connexion from the Client>->Proxy and one connexion Proxy<->Server

    Parameters
    ----------
    from_host : str
        IP to listen to
    to_host : str
        IP of the server
    port : int
        port connect / listen

    Attributes
    ----------
    from_host : str
        IP to listen to
    to_host : str
        IP of the server
    port : int
        port of the connexion
    c2p : Client2Proxy
        Structure of Client<->Proxy connexion
    p2s : Proxy2Server
        Structure of Proxy<->Server connexion
    """

    def __init__(self, from_host, to_host, port) -> None:
        super().__init__()
        self.from_host = from_host
        self.to_host = to_host
        self.port = port
        self.c2p = None
        self.p2s = None

    def run(self):
        """
        Main loop of Thread
        """
        while True:
            if GUI:
                root.log_frame.textbox.insert("0.0",f"[proxy({self.port})] setting up\n")
            else:
                print(f"[proxy({self.port})] setting up")
            # Wait for a client to connect
            self.c2p = Client2Proxy(self.from_host, self.port)
            self.p2s = Proxy2Server(self.to_host, self.port)
            print(f"[proxy({self.port})] connection established")

            # Exchange file descriptor
            self.c2p.server = self.p2s.server
            self.p2s.client = self.c2p.client

            self.c2p.start()
            self.p2s.start()


class Client2Proxy(Thread):
    """
    Class wrapping the connexion Client<->Proxy

    Parameters
    ----------
    host : str
        IP to listen to
    port : int
        port connect / listen

    Attributes
    ----------
    server : Socket
        Socket of Proxy<->Server connexion
    host : str
        IP to listen to
    port : int
        port of the connexion
    sock : Client2Proxy
        Socket of Client<->Proxy connexion
    """

    def __init__(self, host, port):
        super().__init__()
        self.server = None  # real server socket not known yet
        self.port = port
        self.host = host
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((host, port))
        sock.listen(1)
        # waiting for a connection
        self.client, _addr = sock.accept()

    def run(self):
        """ Thread main loop """
        while True:
            try:
                data = self.client.recv(4096)
                if data:
                    # First, display data
                    #print(f"[{self.port}] -> {data[:100].hex()}")

                    # Reload the parser in order to be dynamic
                    importlib.reload(Protocol_Parser)
                    if not GUI:
                        Protocol_Parser.parse(data, 'client')
                    else:
                        if root.log_frame.activate_filter:
                            Protocol_Parser.parse(data, 'client',window_text=root.log_frame.textbox, filter_selected=root.log_frame.combobox.get())
                        else:
                            Protocol_Parser.parse(data, 'client',window_text=root.log_frame.textbox)

                # Then, send data to real server
                self.server.sendall(data)
            except ConnectionError as con_err:
                print('client[{self.port}]', con_err)
                break
            except Exception as o_err:
                print('client[{self.port}]', o_err)


class Proxy2Server(Thread):
    """
    Class wrapping the connexion Proxy<->Server

    Parameters
    ----------
    host : str
        IP to listen to
    port : int
        port connect / listen

    Attributes
    ----------
    server : Socket
        Socket of Proxy<->Server connexion
    host : str
        IP to listen to
    port : int
        port of the connexion
    client : Client2Proxy
        Socket of Client<->Proxy connexion
    """

    def __init__(self, host, port):
        super().__init__()
        self.client = None  # game client socket not known yet
        self.port = port
        self.host = host
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connect((host, port))

    # run in thread
    def run(self):
        """Thread main loop"""
        while True:
            try:
                data = self.server.recv(4096)
                if data:
                    # First, display data
                    #print(f"[{self.port}] <- {data[:100].hex()}")

                    importlib.reload(Protocol_Parser)
                    if not GUI:
                        Protocol_Parser.parse(data, 'client')
                    else:
                        if root.log_frame.activate_filter:
                            Protocol_Parser.parse(data, 'client',window_text=root.log_frame.textbox, filter_selected=root.log_frame.combobox.get())
                        else:
                            Protocol_Parser.parse(data, 'client',window_text=root.log_frame.textbox)

                # Then, send data to real server
                self.client.sendall(data)
            except ConnectionError as conn_err:
                print(f'client[{self.port}]', conn_err)
                break
            except Exception as o_err:
                print(f'client[{self.port}]', o_err)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: python3 {sys.argv[0]} <server ip>")
    else:
        SERVER_IP = sys.argv[1]

    GUI = bool("--gui" in sys.argv)

    if GUI:
        root = gui.MainWin()

    SERVER_IP = 'pentest.hackutt.uttnetgroup.fr'
    MASTER_PORT = 3333

    master_server = Proxy('0.0.0.0', SERVER_IP, MASTER_PORT)
    master_server.start()

    game_servers = []
    for port_t in range(3000, 3006):
        _game_server = Proxy('0.0.0.0', SERVER_IP, port_t)
        _game_server.start()
        game_servers.append(_game_server)

    if GUI:
        root.mainloop()
    else:
        while True:
            try:
                cmd = input('$ ')
                if cmd[:4] == 'quit':
                    os.exit(0)
            except Exception as err:
                print(err)
