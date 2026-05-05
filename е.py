import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import json
import os

class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Password Generator")
        
        tk.Label(root, text="Длина пароля:").pack()
        self.length_slider = tk.Scale(root, from_=4, to=32, orient="horizontal")
        self.length_slider.set(12)
        self.length_slider.pack()

        self.use_digits = tk.BooleanVar(value=True)
        tk.Checkbutton(root, text="Цифры", variable=self.use_digits).pack()
        
        self.use_letters = tk.BooleanVar(value=True)
        tk.Checkbutton(root, text="Буквы", variable=self.use_letters).pack()
        
        self.use_spec = tk.BooleanVar(value=False)
        tk.Checkbutton(root, text="Спецсимволы", variable=self.use_spec).pack()

        self.gen_button = tk.Button(root, text="Сгенерировать", command=self.generate_password)
        self.gen_button.pack(pady=10)

        self.history_tree = ttk.Treeview(root, columns=("Password"), show='headings')
        self.history_tree.heading("Password", text="История паролей")
        self.history_tree.pack(padx=10, pady=10)
        
        self.load_history()

    def generate_password(self):
        chars = ""
        if self.use_digits.get(): chars += string.digits
        if self.use_letters.get(): chars += string.ascii_letters
        if self.use_spec.get(): chars += string.punctuation

        if not chars:
            messagebox.showwarning("Ошибка", "Выберите хотя бы один тип символов!")
            return

        length = self.length_slider.get()
        password = "".join(random.choice(chars) for _ in range(length))
        
        self.save_to_history(password)
        self.history_tree.insert("", 0, values=(password,))

    def save_to_history(self, password):
        history = self.read_json()
        history.append(password)
        with open("history.json", "w") as f:
            json.dump(history, f)

    def read_json(self):
        if not os.path.exists("history.json"): return []
        with open("history.json", "r") as f:
            try: return json.load(f)
            except: return []

    def load_history(self):
        for pw in self.read_json():
            self.history_tree.insert("", "end", values=(pw,))

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()
