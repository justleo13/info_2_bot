import socket
import os
import tkinter as tk
from tkinter import filedialog

SERVER_IP = '172.20.10.3'   # <-- впиши IP сервера
PORT = 5001

def send_file():
    filepath = filedialog.askopenfilename()
    if not filepath:
        return

    try:
        client = socket.socket()
        client.connect((SERVER_IP, PORT))

        filename_bytes = os.path.basename(filepath).encode('utf-8')

        # Отправляем размер имени
        client.sendall(len(filename_bytes).to_bytes(4, 'big'))

        # Отправляем имя
        client.sendall(filename_bytes)

        # Отправляем файл
        with open(filepath, "rb") as f:
            while True:
                data = f.read(4096)
                if not data:
                    break
                client.sendall(data)

        client.close()
        status_label.config(text="Файл отправлен 🚀", fg="green")

    except Exception as e:
        status_label.config(text="Ошибка ❌", fg="red")
        print("Ошибка клиента:", e)

# GUI
root = tk.Tk()
root.title("INFObot Transfer")
root.geometry("400x250")
root.resizable(False, False)

btn = tk.Button(root,
                text="Выбрать и отправить файл",
                font=("Arial", 14),
                command=send_file)
btn.pack(pady=60)

status_label = tk.Label(root, text="", font=("Arial", 12))
status_label.pack()

root.mainloop()
