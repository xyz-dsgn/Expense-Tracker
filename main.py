import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
from datetime import datetime

class ExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")

        self.expenses = []

        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        # Ввод данных
        frame_input = tk.Frame(self.root)
        frame_input.pack(padx=10, pady=10)

        tk.Label(frame_input, text="Сумма").grid(row=0, column=0, padx=5, pady=5)
        self.entry_amount = tk.Entry(frame_input)
        self.entry_amount.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_input, text="Категория").grid(row=1, column=0, padx=5, pady=5)
        self.category_var = tk.StringVar()
        self.combo_category = ttk.Combobox(frame_input, textvariable=self.category_var,
                                           values=["Еда", "Транспорт", "Развлечения", "Другое"])
        self.combo_category.grid(row=1, column=1, padx=5, pady=5)
        self.combo_category.current(0)  # Установить выбранную категорию по умолчанию

        tk.Label(frame_input, text="Дата (гггг-мм-дд)").grid(row=2, column=0, padx=5, pady=5)
        self.entry_date = tk.Entry(frame_input)
        self.entry_date.grid(row=2, column=1, padx=5, pady=5)
        self.entry_date.insert(0, datetime.now().strftime("%Y-%m-%d"))

        # Кнопка добавления расхода
        btn_add = tk.Button(self.root, text="Добавить расход", command=self.add_expense)
        btn_add.pack(pady=5)

        # Фильтры
        frame_filters = tk.Frame(self.root)
        frame_filters.pack(padx=10, pady=10)

        tk.Label(frame_filters, text="Фильтр по категории").grid(row=0, column=0, padx=5)
        self.filter_category_var = tk.StringVar()
        self.combo_filter_category = ttk.Combobox(frame_filters, textvariable=self.filter_category_var,
                                                  values=["Все", "Еда", "Транспорт", "Развлечения", "Другое"])
        self.combo_filter_category.current(0)
        self.combo_filter_category.grid(row=0, column=1, padx=5)

        tk.Label(frame_filters, text="По дате (гггг-мм-дд)").grid(row=0, column=2, padx=5)
        self.entry_filter_date = tk.Entry(frame_filters)
        self.entry_filter_date.grid(row=0, column=3, padx=5)

        btn_apply_filter = tk.Button(frame_filters, text="Применить фильтр", command=self.apply_filter)
        btn_apply_filter.grid(row=0, column=4, padx=5)

        btn_reset_filter = tk.Button(frame_filters, text="Сбросить фильтр", command=self.load_data)
        btn_reset_filter.grid(row=0, column=5, padx=5)

        # Таблица расходов
        columns = ("amount", "category", "date")
        self.tree = ttk.Treeview(self.root, columns=columns, show='headings')
        self.tree.heading('amount', text='Сумма')
        self.tree.heading('category', text='Категория')
        self.tree.heading('date', text='Дата')
        self.tree.pack(padx=10, pady=10, fill='both', expand=True)

        # Итоговая сумма
        self.label_total = tk.Label(self.root, text="Общая сумма: 0")
        self.label_total.pack(pady=5)

        # Меню для сохранения/загрузки
        menubar = tk.Menu(self.root)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Сохранить в JSON", command=self.save_to_json)
        file_menu.add_command(label="Загрузить из JSON", command=self.load_from_json)
        menubar.add_cascade(label="Файл", menu=file_menu)
        self.root.config(menu=menubar)

    def add_expense(self):
        amount_str = self.entry_amount.get().strip()
        category = self.category_var.get()
        date_str = self.entry_date.get().strip()

        # Проверка суммы
        try:
            amount = float(amount_str)
            if amount <= 0:
                raise ValueError
        except:
            messagebox.showerror("Ошибка", "Введите положительное число для суммы")
            return

        # Проверка даты
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
        except:
            messagebox.showerror("Ошибка", "Введите дату в формате ГГГГ-ММ-ДД")
            return

        expense = {
            "amount": amount,
            "category": category,
            "date": date_str
        }
        self.expenses.append(expense)
        self.update_treeview()
        self.update_total()
        self.clear_entries()

    def clear_entries(self):
        self.entry_amount.delete(0, tk.END)
        self.category_var.set("")
        self.entry_date.delete(0, tk.END)
        self.entry_date.insert(0, datetime.now().strftime("%Y-%m-%d"))

    def update_treeview(self, data=None):
        for item in self.tree.get_children():
            self.tree.delete(item)
        data_to_show = data if data is not None else self.expenses
        for exp in data_to_show:
            self.tree.insert('', tk.END, values=(exp["amount"], exp["category"], exp["date"]))
        self.update_total()

    def update_total(self):
        total = sum(exp["amount"] for exp in self.expenses)
        self.label_total.config(text=f"Общая сумма: {total:.2f}")

    def save_to_json(self):
        filename = filedialog.asksaveasfilename(defaultextension=".json",
                                                filetypes=[("JSON файлы", "*.json")])
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(self.expenses, f, ensure_ascii=False, indent=4)
                messagebox.showinfo("Успех", "Данные успешно сохранены")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка при сохранении: {e}")

    def load_from_json(self):
        filename = filedialog.askopenfilename(filetypes=[("JSON файлы", "*.json")])
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    self.expenses = json.load(f)
                self.update_treeview()
                self.update_total()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка при загрузке: {e}")

    def apply_filter(self):
        category_filter = self.combo_filter_category.get()
        date_filter = self.entry_filter_date.get().strip()

        filtered = self.expenses

        if category_filter != "Все":
            filtered = [e for e in filtered if e["category"] == category_filter]

        if date_filter:
            try:
                datetime.strptime(date_filter, "%Y-%m-%d")
                filtered = [e for e in filtered if e["date"] == date_filter]
            except:
                messagebox.showerror("Ошибка", "Введите дату в формате ГГГГ-ММ-ДД")
                return

        self.update_treeview(filtered)

    def load_data(self):
        # Можно реализовать загрузку из файла по умолчанию или очистку
        self.expenses = []
        self.update_treeview()
        self.update_total()

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTracker(root)
    root.mainloop()