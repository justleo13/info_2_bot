import socket
import os
from pathlib import Path

HOST = '0.0.0.0'
PORT = 5001
downloads_folder = str(Path.home() / "Downloads")

server = socket.socket()
server.bind((HOST, PORT))
server.listen(5)

print("Сервер запущен...")

while True:
    try:
        conn, addr = server.accept()
        print("Подключился:", addr)

        filename = conn.recv(1024).decode().strip()
        if not filename:
            print("Ошибка: пустое имя файла")
            conn.close()
            continue

        filepath = os.path.join(downloads_folder, filename)

        with open(filepath, "wb") as f:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                f.write(data)

        print("Файл получен:", filename)
        conn.close()

    except Exception as e:
        print("Ошибка сервера:", e)
