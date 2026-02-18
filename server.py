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

def recvall(conn, size):
    data = b''
    while len(data) < size:
        packet = conn.recv(size - len(data))
        if not packet:
            return None
        data += packet
    return data

while True:
    try:
        conn, addr = server.accept()
        print("Подключился:", addr)

        name_size = int.from_bytes(recvall(conn, 4), 'big')
        filename = recvall(conn, name_size).decode('utf-8')

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
