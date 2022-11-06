import socket, sys, json
import threading
import platform
from time import sleep

import psutil

getInfo = False

class Server(object):
    def __init__(self, address, port):
        self.conn = socket.socket()
        self.address = address
        self.port = port

    def start(self):
        self.conn.connect((self.address, int(self.port)))
        threading.Thread(target=self.proccess, args=(self.conn,), name="Commands").start()
        threading.Thread(target=self.commands, args=(self.conn,), name="Commands").start()

    def proccess(self, connection):
        while True:
            cpuperc = psutil.cpu_percent(2)
            connection.settimeout(60)
            tmp = {"percent": cpuperc}
            data = json.dumps(tmp)
            if not getInfo:
                connection.sendall(bytes(data, encoding="utf-8"))
            else:
                continue
            print(f"{cpuperc}%")
        sys.exit()

    def commands(self, connection):
        global getInfo
        while True:
            try:
                command = connection.recv(1024).decode("utf-8")
                if len(command) != 0:
                    if command == "quit":
                        connection.close()
                        break
                        sys.exit()
                    if command == "getInfo":
                        getInfo = True
                        tmp = {"System": platform.system(), "Version": platform.version()}
                        data = json.dumps(tmp)
                        sleep(3)
                        connection.sendall(bytes(data, encoding="utf-8"))
                        getInfo = False
                        break
                else:
                    continue
            except:
                sys.exit()


if __name__ == '__main__':
    address, port = input("Введите ip-адрес сервера и порт через пробел: ").split()
    server = Server(address, port)
    thr1 = threading.Thread(target=server.start, name="Connect_server").start()

