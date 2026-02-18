import socket
import os
from pathlib import Path

HOST = '0.0.0.0'
PORT = 5001
downloads_folder = str(Path.home() / "Downloads")

def recvall(conn, size):
    data = b''
    while len(data) < size:
        packet = conn.recv(size - len(data))
        if not packet:
            return None
        data += packet
    return data

server = socket.socket()
server.bind((HOST, PORT))
server.listen(5)

print("Сервер запущен...")

while True:
    conn, addr = server.accept()
    print("Подключился:", addr)

    try:
        # Получаем размер имени
        name_size_bytes = recvall(conn, 4)
        if not name_size_bytes:
            print("Ошибка: не удалось получить размер имени")
            conn.close()
            continue

        name_size = int.from_bytes(name_size_bytes, 'big')

        # Получаем имя файла
        filename_bytes = recvall(conn, name_size)
        if not filename_bytes:
            print("Ошибка: не удалось получить имя файла")
            conn.close()
            continue

        filename = filename_bytes.decode('utf-8')

        filepath = os.path.join(downloads_folder, filename)

        # Получаем файл
        with open(filepath, "wb") as f:
            while True:
                data = conn.recv(4096)
                if not data:
                    break
                f.write(data)

        print("Файл получен:", filename)

    except Exception as e:
        print("Ошибка сервера:", e)

    conn.close()
