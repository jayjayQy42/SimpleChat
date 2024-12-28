# Chat Client Application

import socket
import threading
import tkinter as tk
from tkinter import simpledialog, scrolledtext, messagebox

# Server Configuration
HOST = 'your ip here'
PORT = your port here

# Create a socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client_socket.connect((HOST, PORT))
    print(f"Connected to {HOST}:{PORT}")
except Exception as e:
    print(f"Connection failed: {e}")

# GUI Setup
class ChatClientApp:
    def __init__(self, master):
        self.master = master
        master.title("Chat Client Application")

        self.chat_area = scrolledtext.ScrolledText(master, state='disabled')
        self.chat_area.pack(padx=10, pady=10)

        self.message_entry = tk.Entry(master)
        self.message_entry.pack(padx=10, pady=10)
        self.message_entry.bind("<Return>", self.send_message)

        self.send_button = tk.Button(master, text="Send", command=self.send_message)
        self.send_button.pack(padx=10, pady=10)

        self.bomb_button = tk.Button(master, text="Bomb Chat", command=self.bomb_chat)
        self.bomb_button.pack(padx=10, pady=10)

        self.connected_users_button = tk.Button(master, text="Connected Users", command=self.show_connected_users)
        self.connected_users_button.pack(padx=10, pady=10)

        self.username = simpledialog.askstring("Username", "Enter your username:")
        self.chat_area.config(state='normal')
        self.chat_area.insert(tk.END, f"Welcome, {self.username}!\n")
        self.chat_area.config(state='disabled')

        threading.Thread(target=self.receive_messages, daemon=True).start()

    def send_message(self, event=None):
        message = self.message_entry.get()
        self.message_entry.delete(0, tk.END)
        full_message = f"{self.username}: {message}"
        self.chat_area.config(state='normal')
        self.chat_area.insert(tk.END, f"You: {message}\n")
        self.chat_area.config(state='disabled')
        client_socket.send(full_message.encode('utf-8'))

    def bomb_chat(self):
        for _ in range(10):  # Send the message 10 times
            client_socket.send(f"{self.username}: sigmaboywashere\n".encode('utf-8'))

    def receive_messages(self):
        while True:
            try:
                message = client_socket.recv(1024).decode('utf-8')
                if message:
                    self.chat_area.config(state='normal')
                    self.chat_area.insert(tk.END, f"{message}\n")
                    self.chat_area.config(state='disabled')
                else:
                    break
            except Exception as e:
                print(f"An error occurred: {e}")
                client_socket.close()
                break

    def show_connected_users(self):
        # This is a placeholder for the actual implementation
        connected_users = "User1 (192.168.2.179)\nUser2 (192.168.2.180)"  # Example data
        messagebox.showinfo("Connected Users", connected_users)

def run_client_gui():
    root = tk.Tk()
    chat_client_app = ChatClientApp(root)
    root.mainloop()

# Start the client GUI
if __name__ == "__main__":
    run_client_gui()
