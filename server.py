# Chat Application

import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, Toplevel, Label, messagebox
import random

# Server Configuration
HOST = '192.168.2.178'
PORT = 8080
USERNAME = "adminownerceo"

# Create a socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)

clients = []
addresses = {}

def handle_client(client_socket, addr):
    addresses[client_socket] = addr
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                broadcast(message, client_socket)
            else:
                remove(client_socket)
        except:
            continue

def broadcast(message, client_socket):
    for client in clients:
        if client != client_socket:
            try:
                client.send(message.encode('utf-8'))
            except:
                remove(client)

def remove(client_socket):
    if client_socket in clients:
        clients.remove(client_socket)
        del addresses[client_socket]

def accept_connections():
    while True:
        client_socket, addr = server_socket.accept()
        clients.append(client_socket)
        print(f"Connection from {addr} has been established.")
        threading.Thread(target=handle_client, args=(client_socket, addr)).start()

# GUI Setup
class ChatApp:
    def __init__(self, master):
        self.master = master
        master.title("Chat Application")

        self.chat_area = scrolledtext.ScrolledText(master, state='disabled')
        self.chat_area.pack(padx=10, pady=10)

        self.message_entry = tk.Entry(master)
        self.message_entry.pack(padx=10, pady=10)
        self.message_entry.bind("<Return>", self.send_message)

        self.send_button = tk.Button(master, text="Send", command=self.send_message)
        self.send_button.pack(padx=10, pady=10)

        self.connected_button = tk.Button(master, text="Show Connected", command=self.show_connected)
        self.connected_button.pack(padx=10, pady=10)

        self.emotion_button = tk.Button(master, text="Show Emotions", command=self.show_emotions)
        self.emotion_button.pack(padx=10, pady=10)

        self.link_button = tk.Button(master, text="Send Link", command=self.send_link)
        self.link_button.pack(padx=10, pady=10)

        self.login_button = tk.Button(master, text="Login as Admin", command=self.login)
        self.login_button.pack(padx=10, pady=10)

    def send_message(self, event=None):
        message = self.message_entry.get()
        self.message_entry.delete(0, tk.END)
        self.chat_area.config(state='normal')
        self.chat_area.insert(tk.END, f"{USERNAME}: {message}\n")
        self.chat_area.config(state='disabled')
        broadcast(message.encode('utf-8'), None)

    def show_connected(self):
        connected_window = Toplevel(self.master)
        connected_window.title("Connected Clients")
        for client, addr in addresses.items():
            Label(connected_window, text=f"{addr[0]}:{addr[1]}").pack()

    def show_emotions(self):
        emotions = ["😊", "😂", "😢", "😡", "😍", "😎", "🤔", "🤗", "🥳", "😱"]
        emotion_window = Toplevel(self.master)
        emotion_window.title("Select Emotion")
        for emotion in emotions:
            button = tk.Button(emotion_window, text=emotion, command=lambda e=emotion: self.send_emotion(e))
            button.pack(padx=10, pady=5)

    def send_emotion(self, emotion):
        self.chat_area.config(state='normal')
        self.chat_area.insert(tk.END, f"{USERNAME}: {emotion}\n")
        self.chat_area.config(state='disabled')
        broadcast(emotion.encode('utf-8'), None)

    def send_link(self):
        link = self.message_entry.get()
        self.message_entry.delete(0, tk.END)
        self.chat_area.config(state='normal')
        self.chat_area.insert(tk.END, f"{USERNAME}: {link}\n")
        self.chat_area.config(state='disabled')
        broadcast(link.encode('utf-8'), None)

    def login(self):
        login_window = Toplevel(self.master)
        login_window.title("Admin Login")
        
        Label(login_window, text="Username:").pack(padx=10, pady=5)
        username_entry = tk.Entry(login_window)
        username_entry.pack(padx=10, pady=5)

        Label(login_window, text="Password:").pack(padx=10, pady=5)
        password_entry = tk.Entry(login_window, show='*')
        password_entry.pack(padx=10, pady=5)

        def check_credentials():
            if username_entry.get() == "sigma" and password_entry.get() == "sigma":
                login_window.destroy()
                self.admin_panel()
            else:
                messagebox.showerror("Error", "Invalid credentials")

        tk.Button(login_window, text="Login", command=check_credentials).pack(padx=10, pady=10)

    def admin_panel(self):
        admin_window = Toplevel(self.master)
        admin_window.title("Admin Sigma")

        buttons = []
        correct_button_index = random.randint(0, 19)

        for i in range(20):
            button = tk.Button(admin_window, text=f"Button {i+1}", command=lambda i=i: self.check_admin_button(i, correct_button_index))
            if i == correct_button_index:
                button.config(font=("Helvetica", 10, "bold"))
            button.pack(padx=10, pady=5)
            buttons.append(button)

    def check_admin_button(self, index, correct_index):
        if index == correct_index:
            self.chat_area.config(state='normal')
            self.chat_area.insert(tk.END, "Admin: Great!\n")
            self.chat_area.config(state='disabled')
            broadcast("Admin: Great!", None)
            self.username = "adminrights"
        else:
            messagebox.showinfo("Info", "Try again!")

def run_gui():
    root = tk.Tk()
    chat_app = ChatApp(root)
    root.mainloop()

# Start the server and GUI
if __name__ == "__main__":
    threading.Thread(target=accept_connections).start()
    run_gui()
