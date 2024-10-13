import socket
import threading
import json

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.clients = {}
        self.experiment_started = False
        self.experiment_number = 0
        self.target_number = None
        self.leaderboard = {}  # {client_address: {experiment_number: attempts}}
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.socket.listen()

        self.accept_thread = threading.Thread(target=self.accept_clients)
        self.accept_thread.start()

    def accept_clients(self):
        while True:
            client_socket, client_address = self.socket.accept()
            self.clients[client_address] = {"socket": client_socket, "history": []}
            client_thread = threading.Thread(target=self.client_observation, args=(client_socket, client_address))
            client_thread.start()

    def client_observation(self, client_socket, client_address):
        while True:
            try:
                data = client_socket.recv(1024).decode("utf-8")
                if not data:
                    break
                message = json.loads(data)
                if message["type"] == "guess":
                    self.guess_observation(client_socket, client_address, message["number"])
            except ConnectionResetError:
                del self.clients[client_address]
                break

    def guess_observation(self, client_socket, client_address, number):
        if not self.experiment_started:
            return

        self.clients[client_address]["history"].append(number)

        if number == self.target_number:
            response = {"type": "result", "result": "correct"}
            if client_address not in self.leaderboard:
                self.leaderboard[client_address] = {}
            number_of_attempts = len(self.clients[client_address]["history"])
            self.leaderboard[client_address][self.experiment_number] = number_of_attempts
            self.clients[client_address]["history"] = []
        elif number < self.target_number:
            response = {"type": "result", "result": "less"}
        else:
            response = {"type": "result", "result": "greater"}

        self.send_to_client(client_socket, response)

    def start_experiment(self, target_number=111):
        self.experiment_started = True
        self.experiment_number += 1
        self.target_number = target_number
        message = {"type": "start"}
        self.send_to_all(message)
        print("Эксперимент начат.")

    def send_to_all(self, message):
        for client_address, client_data in self.clients.items():
            self.send_to_client(client_data["socket"], message)

    def send_to_client(self, client_socket, message):
        try:
            client_socket.send(json.dumps(message).encode("utf-8"))
        except ConnectionResetError:
            print("Ошибка отправки сообщения клиенту.")

    def show_waiting_list(self):
        waiting_list = [client_address for client_address, client_data in self.clients.items() if client_data["history"]]
        print("Список участников, ожидающих ответа:", waiting_list)

    # лидер высчитывается по сумме попыток за все проведенные эксперименты
    def show_leaderboard(self):
        print("Таблица лидеров:")
        sorted_leaderboard = sorted(self.leaderboard.items(), key=lambda item: sum(item[1].values()))
        for client_address, attempts in sorted_leaderboard:
            print(f"{client_address}: {attempts}")

    def stop(self):
        self.accept_thread.join()
        self.socket.close()


if __name__ == "__main__":
    server = Server("127.0.0.1", 8080)
    while True:
        command = input("Введите команду (start, waiting, leaderboard, stop): ")
        if command == "start":
            server.start_experiment()
        elif command == "waiting":
            server.show_waiting_list()
        elif command == "leaderboard":
            server.show_leaderboard()
        elif command == "stop":
            server.stop()
            break
