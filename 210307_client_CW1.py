# PROGRAMMING AND ALGIRITHMS 2
# NAME - ROHAN JOSHI
# STUDENT ID - 210307
# COURSEWORK ASSIGNMENT 1
#                         Secure Online Chatiing System


import socket
import threading
import tkinter
import tkinter.scrolledtext
from tkinter import simpledialog

HOST = '127.0.0.1'
PORT = 9090


class Client:
    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))

        msg = tkinter.Tk()
        msg.geometry("520x320")
        msg.title("Chatting System")
        msg.config(bg="#363945")
        first_label = tkinter.Label(
            msg, text="PROGRAMMING AND ALGORITHMS 2", font=('Bahnschrift SemiBold Condensed', 17, 'bold'), bg="#363945", fg="white")
        first_label.pack(pady=5)

        msg_label = tkinter.Label(
            msg, text="Welcome \nto", font=('Helvetica', 13), bg="#363945", fg="white")
        msg_label.pack(pady=7)

        msg_label = tkinter.Label(
            msg, text="'SECURE ONLINE CHATTING SYSTEM'", font=('Times New Roman', 18, 'bold'), bg="#363945", fg="white")
        msg_label.pack(pady=4)

        text_two = tkinter.Label(
            msg, text="Created by Rohan Joshi", font=('Helvetica', 12, 'italic'), bg="#363945", fg="white")
        text_two.pack()

        text_three = tkinter.Label(
            msg, text="Click the button below to enter a nickname", font=('Helvetica', 11), bg="#363945", fg="white")
        text_three.pack(pady=10)

        def nickkname():
            self.nickname = simpledialog.askstring(
                "Nickname", "Please choose a nickname", parent=msg)

            msg.destroy()

        nickname_btn = tkinter.Button(
            msg, text="Click Here !!", command=nickkname, font=('Helvetica', 9, 'bold'))
        nickname_btn.pack(pady=4)
        msg.mainloop()

        self.gui_done = False
        self.running = True

        gui_thread = threading.Thread(target=self.gui_loop)
        receive_thread = threading.Thread(target=self.receive)

        gui_thread.start()
        receive_thread.start()

    def gui_loop(self):
        self.win = tkinter.Tk()
        self.win.configure(bg="#C0C0C0")
        self.win.title(f"Chat of {self.nickname}")
        self.win.resizable(0, 0)

        self.chat_label = tkinter.Label(self.win, text="Chat:", bg="#C0C0C0")
        self.chat_label.config(font=("Arial", 12))
        self.chat_label.pack(padx=20, pady=5)

        self.text_area = tkinter.scrolledtext.ScrolledText(self.win)
        self.text_area.pack(padx=20, pady=5)
        self.text_area.config(state='disabled')

        self.msg_label = tkinter.Label(
            self.win, text="Message:", bg="#C0C0C0")
        self.msg_label.config(font=("Arial", 12))
        self.msg_label.pack(padx=20, pady=5)

        self.input_area = tkinter.Text(self.win, height=3, bg="#C0C0C0")
        self.input_area.pack(padx=20, pady=5)

        self.button_frame = tkinter.Frame(self.win, bg="#C0C0C0")
        self.button_frame.pack(padx=20, pady=5)

        self.send_button = tkinter.Button(
            self.button_frame, text="Send", command=self.write)
        self.send_button.config(font=("Arial", 12))
        self.send_button.grid(row=0, column=0, padx=20, pady=5)

        self.decrypt_button = tkinter.Button(
            self.button_frame, text="Decrypt", command=self.decrypt_message)
        self.decrypt_button.config(font=("Arial", 12))
        self.decrypt_button.grid(row=0, column=1, padx=20, pady=5)

        self.exit_btn = tkinter.Button(
            self.button_frame, text="Exit", command=exit)
        self.exit_btn.config(font=("Arial", 12))
        self.exit_btn.grid(row=0, column=2, padx=20, pady=5)

        self.gui_done = True
        self.win.protocol("WM_DELETE_WINDOW", self.stop)
        self.win.mainloop()

    def rot13_encode(self, text):
        result = ""
        for char in text:
            ascii_value = ord(char)
            if 65 <= ascii_value <= 90:
                result += chr((ascii_value - 65 + 13) % 26 + 65)
            elif 97 <= ascii_value <= 122:
                result += chr((ascii_value - 97 + 13) % 26 + 97)
            else:
                result += char
        return result

    def write(self):
        message = f"{self.nickname}: {self.input_area.get('1.0', 'end')}"
        message = self.rot13_encode(message)
        print(message)
        self.sock.send(message.encode('utf-8'))
        self.input_area.delete('1.0', 'end')

    def stop(self):
        self.running = False
        self.win.destroy()
        self.sock.close()
        exit(0)

    def rot13_decode(self, text):

        result = ""
        for char in text:
            ascii_value = ord(char)
            if 65 <= ascii_value <= 90:
                result += chr((ascii_value - 78) % 26 + 65)
            elif 97 <= ascii_value <= 122:
                result += chr((ascii_value - 110) % 26 + 97)
            else:
                result += char
        return result

    def decrypt_message(self):
        texts = self.text_area.get(1.0, tkinter.END)
        decrypt_message = self.rot13_decode(texts)
        self.text_area.config(state='normal', bg="#C0C0C0")
        self.text_area.delete(1.0, tkinter.END)
        self.text_area.insert('end', decrypt_message)
        self.text_area.yview('end')
        self.text_area.config(state='disabled', bg="#C0C0C0")

    def receive(self):
        while self.running:
            try:
                message = self.sock.recv(1024).decode('utf-8')

                if message == 'NICK':
                    self.sock.send(self.nickname.encode('utf-8'))
                else:
                    if self.gui_done:
                        self.text_area.config(state='normal', bg="#C0C0C0")
                        self.text_area.insert('end', message)
                        self.text_area.yview('end')
                        self.text_area.config(state='disabled', bg="#C0C0C0")
            except ConnectionAbortedError:
                break
            except:
                print("Error")
                self.sock.close()
                break


client = Client(HOST, PORT)
