import tkinter as tk
from tkinter import ttk, messagebox
import requests
import json
import os


class GitHubUserFinder:
    def __init__(self, root):
        self.root = root
        self.root.title("GitHub User Finder")
        self.root.geometry("600x500")

        # Файл для хранения избранных пользователей
        self.favorites_file = "favorites.json"
        self.load_favorites()

        self.setup_ui()

    def setup_ui(self):
        # Поле ввода
        input_frame = ttk.Frame(self.root)
        input_frame.pack(pady=10, padx=20, fill="x")

        ttk.Label(input_frame, text="Введите имя пользователя GitHub:").pack(side="left")
        self.search_entry = ttk.Entry(input_frame, width=40)
        self.search_entry.pack(side="left", padx=5)
        ttk.Button(input_frame, text="Найти", command=self.search_user).pack(side="left")

        # Результаты поиска
        results_frame = ttk.LabelFrame(self.root, text="Результаты поиска")
        results_frame.pack(pady=10, padx=20, fill="both", expand=True)

        self.results_list = tk.Listbox(results_frame, height=10)
        self.results_list.pack(fill="both", expand=True, padx=5, pady=5)

        # Кнопки управления избранным
        buttons_frame = ttk.Frame(self.root)
        buttons_frame.pack(pady=5, padx=20, fill="x")

        ttk.Button(buttons_frame, text="Добавить в избранное",
                   command=self.add_to_favorites).pack(side="left", padx=5)
        ttk.Button(buttons_frame, text="Показать избранное",
                   command=self.show_favorites).pack(side="left", padx=5)

        # Список избранного
        favorites_frame = ttk.LabelFrame(self.root, text="Избранное")
        favorites_frame.pack(pady=10, padx=20, fill="both", expand=True)

        self.favorites_list = tk.Listbox(favorites_frame, height=5)
        self.favorites_list.pack(fill="both", expand=True, padx=5, pady=5)

    def search_user(self):
        username = self.search_entry.get().strip()
        if not username:
            messagebox.showerror("Ошибка", "Поле поиска не должно быть пустым!")
            return

        try:
            response = requests.get(f"https://api.github.com/users/{username}")
            if response.status_code == 200:
                user_data = response.json()
                self.display_user(user_data)
            else:
                messagebox.showerror("Ошибка", f"Пользователь '{username}' не найден!")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка: {e}")

    def display_user(self, user_data):
        self.results_list.delete(0, tk.END)
        display_text = f"{user_data['login']} - {user_data.get('name', 'No name')} ({user_data.get('company', 'No company')})"
        self.results_list.insert(tk.END, display_text)

    def add_to_favorites(self):
        selection = self.results_list.curselection()
        if not selection:
            messagebox.showwarning("Предупреждение", "Выберите пользователя из результатов поиска!")
            return

        user_text = self.results_list.get(selection[0])
        if user_text not in self.favorites:
            self.favorites.append(user_text)
            self.save_favorites()
            self.update_favorites_list()
            messagebox.showinfo("Успех", "Пользователь добавлен в избранное!")
        else:
            messagebox.showinfo("Информация", "Этот пользователь уже в избранном!")

    def load_favorites(self):
        if os.path.exists(self.favorites_file):
            with open(self.favorites_file, 'r', encoding='utf-8') as f:
                self.favorites = json.load(f)
        else:
            self.favorites = []

    def save_favorites(self):
        with open(self.favorites_file, 'w', encoding='utf-8') as f:
            json.dump(self.favorites, f, ensure_ascii=False, indent=2)

    def update_favorites_list(self):
        self.favorites_list.delete(0, tk.END)
        for user in self.favorites:
            self.favorites_list.insert(tk.END, user)

    def show_favorites(self):
        self.update_favorites_list()

if __name__ == "__main__":
    root = tk.Tk()
    app = GitHubUserFinder(root)
    root.mainloop()
