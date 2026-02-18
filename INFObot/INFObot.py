import socket
import os
import sys
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

SERVER_IP = '172.20.10.14'  # <-- IP сервера
PORT = 5001


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def send_file():
    filepath = filedialog.askopenfilename()
    if not filepath:
        return

    try:
        client = socket.socket()
        client.connect((SERVER_IP, PORT))

        filename_bytes = os.path.basename(filepath).encode('utf-8')
        client.sendall(len(filename_bytes).to_bytes(4, 'big'))
        client.sendall(filename_bytes)

        with open(filepath, "rb") as f:
            while True:
                data = f.read(4096)
                if not data:
                    break
                client.sendall(data)

        client.close()
        status_label.config(text="Файл отправлен 🚀", fg="lime")

    except Exception as e:
        status_label.config(text="Ошибка ❌", fg="red")
        print(e)


# ================= GUI =================

root = tk.Tk()
root.title("INFObot Transfer")
root.geometry("900x550")
root.resizable(False, False)

# 🔥 Загружаем и масштабируем картинку
bg_path = resource_path("bg.png")

image = Image.open(bg_path)
image = image.resize((900, 550), Image.LANCZOS)

bg_image = ImageTk.PhotoImage(image)

canvas = tk.Canvas(root, width=900, height=550)
canvas.pack(fill="both", expand=True)

canvas.create_image(0, 0, image=bg_image, anchor="nw")

button = tk.Button(root,
                   text="Выбрать и отправить файл",
                   font=("Arial", 18),
                   command=send_file)

canvas.create_window(450, 300, window=button)

status_label = tk.Label(root,
                        text="",
                        font=("Arial", 14),
                        bg="black",
                        fg="white")

canvas.create_window(450, 380, window=status_label)

root.mainloop()
