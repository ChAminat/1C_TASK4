import socket
import threading
import json

class Client:
    def __init__(self, server_address):
        self.server_address = server_address
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.history = []

    def connect(self):
        self.socket.connect(self.server_address)
        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.start()

    def receive_messages(self):
        while True:
            try:
                data = self.socket.recv(1024).decode("utf-8")
                if not data:
                    break
                message = json.loads(data)
                if message["type"] == "start":
                    print("Эксперимент начат!")
                    self.history = []
                elif message["type"] == "result":
                    result = message["result"]
                    if result == "correct":
                        print("Число угадано")
                    elif result == "greater":
                        print("Число больше загаданного")
                    elif result == "less":
                        print("Число меньше загаданного")
            except ConnectionResetError:
                break

    def send_guess(self, number):
        message = {"type": "guess", "number": number}
        self.socket.send(json.dumps(message).encode("utf-8"))
        self.history.append(number)

    def show_history(self):
        print("История:", self.history)

    def disconnect(self):
        self.socket.close()


if __name__ == "__main__":
    server_address = ("127.0.0.1", 8080)
    client = Client(server_address)
    client.connect()

    while True:
        command = input("Введите команду (guess, history, disconnect): ")
        if command == "guess":
            number = int(input("Введите число: "))
            client.send_guess(number)
        elif command == "history":
            client.show_history()
        elif command == "disconnect":
            client.disconnect()
            break
