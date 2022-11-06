import os
import socket
import keyboard
import sys
import json
import threading
from time import sleep


Menu_status = True
Clients_list = {}
keyboard.add_hotkey("ctrl+e", lambda: menu())

class style():
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'

def menu():
    global Menu_status, Clients_list
    Menu_status = False
    sleep(1)
    os.system("cls")
    i = input("Доступные команды:\r\n"
          "1) Отключить клиента\r\n"
          "2) Информация о ПК\r\n"
            "3) Нагрузка\r\n")


    if i == "1":
        try:
            for i, cl in enumerate(Clients_list):
                print(f"id {i}: {cl}")
            id = input("Введите номер id для отключения:" )
            if id != "" and id != "exit":
                for i, cl in enumerate(Clients_list):
                    if i == int(id):
                        try:
                            found = Clients_list.get(cl)
                            found.sendall(bytes("quit", encoding="utf-8"))
                            Clients_list.pop(cl)
                        except Exception as e:
                            print(f"Ошибка {e}")
        except Exception as e:
            print(f"Ошибка - {e}")

    if i == "2":
        for i, cl in enumerate(Clients_list):
            print(f"id {i}: {cl}")
        id = input("Введите номер id для информации:" )
        if id != "" and id != "exit":
            for i, cl in enumerate(Clients_list):
                if i == int(id):
                    found = Clients_list.get(cl)
                    found.sendall(bytes("getInfo", encoding="utf-8"))
                    print("Запрос информации...")
                    sleep(1)
                    while True:
                        message = found.recv(1024).decode("utf-8")
                        if len(message) != 0:
                            message = json.loads(message)
                            print(f"{message['System']} : {message['Version']}")
                            break
                        else:
                            print("Получить информации не удалось, попробуйте позже")
                            break
    if i == "3":
        sleep(1)
        os.system("cls")
        Menu_status = True
        sleep(1)

    if not Menu_status:
        menu()





class Server(object):
    def __init__(self):
        self.sock = socket.socket()
        self.sock.bind(("", 8080))

    def listen(self):
        self.sock.listen(15)
        global Clients_list
        while True:
            try:
                client, address = self.sock.accept()
                client.settimeout(60)
                threading.Thread(target=self.client_message,args=(client,address),name="Clients_message").start()
                Clients_list[address[0]] = client
                print(f"Новое подключение! ip:{address[0]}")
            except:
                continue


    def client_message(self, client, address):
        global Menu_status
        while True:
            try:
                message = client.recv(1024).decode("utf-8")
                if Menu_status:
                    if len(message) != 0:
                        message = json.loads(message)
                        if (float(message['percent']) < 55.0):
                            print(f"ip: {address[0]} Загрузка ЦП: {style.GREEN}{message['percent']}%{style.RESET}")
                        if (float(message['percent']) >= 55.0 and float(message['percent']) <= 75.0):
                            print(f"ip: {address[0]} Загрузка ЦП: {style.YELLOW}{message['percent']}%{style.RESET}")
                        if (float(message['percent']) > 75.0):
                            print(f"ip: {address[0]} Загрузка ЦП: {style.RED}{message['percent']}%{style.RESET}")
                else:
                    continue
            except (KeyboardInterrupt, SystemExit):
                client.close()
                self.sock.close()
                break
            except:
                client.close()
                self.sock.close()
                break

if __name__ == "__main__":
    Server().listen()