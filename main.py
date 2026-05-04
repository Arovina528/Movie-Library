import json
import os
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class MovieLibrary:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Library - Личная кинотека")
        self.root.geometry("800x500")
        self.root.resizable(True, True)
        
        self.data_file = "movies.json"
        self.movies = []
        
        # Загрузка данных из JSON
        self.load_data()
        
        # Создание интерфейса
        self.create_widgets()
        
        # Обновление таблицы
        self.refresh_table()
    
    def create_widgets(self):
        # === Форма ввода ===
        input_frame = tk.LabelFrame(self.root, text="Информация о фильме", padx=10, pady=10)
        input_frame.pack(fill="x", padx=10, pady=5)
        
        # Название
        tk.Label(input_frame, text="Название:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.title_entry = tk.Entry(input_frame, width=30)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Жанр
        tk.Label(input_frame, text="Жанр:").grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.genre_entry = tk.Entry(input_frame, width=20)
        self.genre_entry.grid(row=0, column=3, padx=5, pady=5)
        
        # Год выпуска
        tk.Label(input_frame, text="Год выпуска:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.year_entry = tk.Entry(input_frame, width=10)
        self.year_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # Рейтинг
        tk.Label(input_frame, text="Рейтинг (0-10):").grid(row=1, column=2, sticky="w", padx=5, pady=5)
        self.rating_entry = tk.Entry(input_frame, width=10)
        self.rating_entry.grid(row=1, column=3, padx=5, pady=5)
        
        # Кнопка добавления
        self.add_btn = tk.Button(input_frame, text="Добавить фильм", command=self.add_movie, bg="#4CAF50", fg="white")
        self.add_btn.grid(row=1, column=4, padx=10, pady=5)
        
        # === Фильтры ===
        filter_frame = tk.LabelFrame(self.root, text="Фильтрация", padx=10, pady=10)
        filter_frame.pack(fill="x", padx=10, pady=5)
        
        tk.Label(filter_frame, text="Фильтр по жанру:").pack(side="left", padx=5)
        self.filter_genre_entry = tk.Entry(filter_frame, width=15)
        self.filter_genre_entry.pack(side="left", padx=5)
        
        tk.Label(filter_frame, text="Год выпуска:").pack(side="left", padx=5)
        self.filter_year_entry = tk.Entry(filter_frame, width=8)
        self.filter_year_entry.pack(side="left", padx=5)
        
        self.filter_btn = tk.Button(filter_frame, text="Применить фильтр", command=self.filter_movies, bg="#2196F3", fg="white")
        self.filter_btn.pack(side="left", padx=10)
        
        self.reset_filter_btn = tk.Button(filter_frame, text="Сбросить", command=self.reset_filter, bg="#FF9800", fg="white")
        self.reset_filter_btn.pack(side="left", padx=5)
        
        # === Таблица с фильмами ===
        table_frame = tk.Frame(self.root)
        table_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Создание таблицы Treeview
        columns = ("title", "genre", "year", "rating")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        
        self.tree.heading("title", text="Название")
        self.tree.heading("genre", text="Жанр")
        self.tree.heading("year", text="Год")
        self.tree.heading("rating", text="Рейтинг")
        
        self.tree.column("title", width=250)
        self.tree.column("genre", width=150)
        self.tree.column("year", width=80)
        self.tree.column("rating", width=80)
        
        # Скроллбар
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Кнопка удаления
        self.delete_btn = tk.Button(self.root, text="Удалить выбранный фильм", command=self.delete_movie, bg="#f44336", fg="white")
        self.delete_btn.pack(pady=5)
    
    def validate_movie(self, title, genre, year_str, rating_str):
        """Проверка корректности введённых данных"""
        if not title or not genre:
            messagebox.showerror("Ошибка", "Название и жанр обязательны для заполнения!")
            return False
        
        try:
            year = int(year_str)
            current_year = datetime.now().year
            if year < 1888 or year > current_year + 5:
                messagebox.showerror("Ошибка", f"Год должен быть между 1888 и {current_year + 5}!")
                return False
        except ValueError:
            messagebox.showerror("Ошибка", "Год должен быть целым числом!")
            return False
        
        try:
            rating = float(rating_str)
            if rating < 0 or rating > 10:
                messagebox.showerror("Ошибка", "Рейтинг должен быть от 0 до 10!")
                return False
        except ValueError:
            messagebox.showerror("Ошибка", "Рейтинг должен быть числом!")
            return False
        
        return True
    
    def add_movie(self):
        """Добавление нового фильма"""
        title = self.title_entry.get().strip()
        genre = self.genre_entry.get().strip()
        year = self.year_entry.get().strip()
        rating = self.rating_entry.get().strip()
        
        if self.validate_movie(title, genre, year, rating):
            movie = {
                "title": title,
                "genre": genre,
                "year": int(year),
                "rating": float(rating)
            }
            self.movies.append(movie)
            self.save_data()
            self.refresh_table()
            
            # Очистка полей ввода
            self.title_entry.delete(0, tk.END)
            self.genre_entry.delete(0, tk.END)
            self.year_entry.delete(0, tk.END)
            self.rating_entry.delete(0, tk.END)
            
            messagebox.showinfo("Успех", f"Фильм \"{title}\" добавлен!")
    
    def delete_movie(self):
        """Удаление выбранного фильма"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите фильм для удаления!")
            return
        
        # Получение названия фильма из таблицы
        item = self.tree.item(selected[0])
        title = item['values'][0]
        
        if messagebox.askyesno("Подтверждение", f"Удалить фильм \"{title}\"?"):
            # Удаление из списка
            self.movies = [m for m in self.movies if m['title'] != title]
            self.save_data()
            self.refresh_table()
            messagebox.showinfo("Успех", "Фильм удалён!")
    
    def filter_movies(self):
        """Фильтрация фильмов по жанру и/или году"""
        genre_filter = self.filter_genre_entry.get().strip().lower()
        year_filter = self.filter_year_entry.get().strip()
        
        filtered_movies = self.movies.copy()
        
        if genre_filter:
            filtered_movies = [m for m in filtered_movies if genre_filter in m['genre'].lower()]
        
        if year_filter:
            try:
                year = int(year_filter)
                filtered_movies = [m for m in filtered_movies if m['year'] == year]
            except ValueError:
                messagebox.showerror("Ошибка", "Год фильтрации должен быть целым числом!")
                return
        
        self.update_table(filtered_movies)
    
    def reset_filter(self):
        """Сброс фильтрации"""
        self.filter_genre_entry.delete(0, tk.END)
        self.filter_year_entry.delete(0, tk.END)
        self.refresh_table()
    
    def refresh_table(self):
        """Обновление таблицы всеми фильмами"""
        self.update_table(self.movies)
    
    def update_table(self, movies_list):
        """Обновление таблицы указанным списком фильмов"""
        # Очистка таблицы
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Заполнение таблицы
        for movie in movies_list:
            self.tree.insert("", tk.END, values=(
                movie['title'],
                movie['genre'],
                movie['year'],
                f"{movie['rating']:.1f}"
            ))
    
    def load_data(self):
        """Загрузка данных из JSON файла"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    self.movies = json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                self.movies = []
        else:
            self.movies = []
    
    def save_data(self):
        """Сохранение данных в JSON файл"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.movies, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    root = tk.Tk()
    app = MovieLibrary(root)
    root.mainloop()