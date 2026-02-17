import socket
import os
import tkinter as tk
from tkinter import filedialog

SERVER_IP = '172.20.10.3' 
PORT = 5001

def send_file():
    filepath = filedialog.askopenfilename()
    if not filepath:
        return

    client = socket.socket()
    client.connect((SERVER_IP, PORT))

    filename = os.path.basename(filepath)
    client.send(filename.encode())

    with open(filepath, "rb") as f:
        while True:
            data = f.read(1024)
            if not data:
                break
            client.send(data)

    client.close()
    status_label.config(text="Файл отправлен ✅")

# GUI
root = tk.Tk()
root.title("Отправка файла")

btn = tk.Button(root, text="Выбрать и отправить файл", command=send_file)
btn.pack(pady=20)

status_label = tk.Label(root, text="")
status_label.pack()

root.mainloop()
