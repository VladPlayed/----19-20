import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk

# Создаем подключение к базе данных
conn = sqlite3.connect('employee_db.db')
cursor = conn.cursor()

# Главное окно приложения
class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Управление базой данных")

        # Загружаем изображение и создаем виджет Label для него
        image = Image.open("icon.png")  # Укажите путь к вашему изображению
        photo = ImageTk.PhotoImage(image)
        image_label = tk.Label(self, image=photo)
        image_label.image = photo  # Сохраняем ссылку на изображение, чтобы оно не уничтожалось сборщиком мусора
        image_label.grid(row=0, column=0, columnspan=2)  # Размещаем изображение в верхней левой ячейке

        # Создаем кнопки для каждой таблицы
        employee_button = tk.Button(self, text="Сотрудники", command=self.open_employee_window)
        department_button = tk.Button(self, text="Отделы", command=self.open_department_window)
        vacancy_button = tk.Button(self, text="Вакансии", command=self.open_vacancy_window)
        application_button = tk.Button(self, text="Заявки на вакансии", command=self.open_application_window)

        # Располагаем кнопки 2 на 2 в ячейках сетки
        employee_button.grid(row=1, column=0)
        department_button.grid(row=1, column=1)
        vacancy_button.grid(row=2, column=0)
        application_button.grid(row=2, column=1)

    def open_employee_window(self):
        EmployeeWindow(self)

    def open_department_window(self):
        DepartmentWindow(self)

    def open_vacancy_window(self):
        VacancyWindow(self)

    def open_application_window(self):
        ApplicationWindow(self)


# Окно для работы с таблицей "Сотрудник"
class EmployeeWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Таблица 'Сотрудники'")
        self.geometry("1450x400")

        # Создаем виджет Treeview для отображения данных таблицы "Сотрудник"
        self.tree = ttk.Treeview(self, columns=(
            "Departament ID", "Full Name", "Gender", "Birth Date", "Education",
            "Position", "Profession", "Hire Date", "Salary", "Passport Data", "Address"))

        self.tree.heading("#0", text="")
        self.tree.heading("#1", text="Departament ID")
        self.tree.heading("#2", text="Full Name")
        self.tree.heading("#3", text="Gender")
        self.tree.heading("#4", text="Birth Date")
        self.tree.heading("#5", text="Education")
        self.tree.heading("#6", text="Position")
        self.tree.heading("#7", text="Profession")
        self.tree.heading("#8", text="Hire Date")
        self.tree.heading("#9", text="Salary")
        self.tree.heading("#10", text="Passport Data")
        self.tree.heading("#11", text="Address")

        # Устанавливаем ширину колонок
        self.tree.column("#0", width=0)
        self.tree.column("#1", width=100)
        self.tree.column("#2", width=180)
        self.tree.column("#3", width=60)
        self.tree.column("#4", width=80)
        self.tree.column("#5", width=80)
        self.tree.column("#6", width=100)
        self.tree.column("#7", width=160)
        self.tree.column("#8", width=80)
        self.tree.column("#9", width=60)
        self.tree.column("#10", width=100)
        self.tree.column("#11", width=300)

        self.tree.pack()

        # Кнопка для добавления сотрудника
        self.add_employee_button = tk.Button(self, text="Добавить сотрудника", command=self.add_employee)
        self.add_employee_button.pack()

        # Обновляем таблицу "Сотрудник" при открытии окна
        self.update_employee_table()

    def update_employee_table(self):
        self.tree.delete(*self.tree.get_children())
        cursor.execute("SELECT * FROM employee")
        data = cursor.fetchall()
        for row in data:
            self.tree.insert("", "end", values=row)

    def add_employee(self):
        # Ваш код для добавления сотрудника в базу данных
        pass

# Окно для работы с таблицей "Отдел"
class DepartmentWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Таблица 'Отделы'")
        self.geometry("800x400")

        # Создаем виджет Treeview для отображения данных таблицы "Отдел"
        self.tree = ttk.Treeview(self, columns=(
            "Departament ID", "Name", "Head", "Contact Info", "Employee ID"))

        self.tree.heading("#0", text="")
        self.tree.heading("#1", text="Departament ID")
        self.tree.heading("#2", text="Name")
        self.tree.heading("#3", text="Head")
        self.tree.heading("#4", text="Contact Info")
        self.tree.heading("#5", text="Employee ID")

        # Устанавливаем ширину колонок
        self.tree.column("#0", width=0)
        self.tree.column("#1", width=100)
        self.tree.column("#2", width=150)
        self.tree.column("#3", width=160)
        self.tree.column("#4", width=250)
        self.tree.column("#5", width=100)

        self.tree.pack()

        # Кнопка для добавления отдела
        self.add_department_button = tk.Button(self, text="Добавить отдел", command=self.add_department)
        self.add_department_button.pack()

        # Обновляем таблицу "Отдел" при открытии окна
        self.update_department_table()

    def update_department_table(self):
        self.tree.delete(*self.tree.get_children())
        cursor.execute("SELECT * FROM department")
        data = cursor.fetchall()
        for row in data:
            self.tree.insert("", "end", values=row)


    def add_department(self):
        # Ваш код для добавления отдела в базу данных
        pass


# Окно для работы с таблицей "Вакансия"
class VacancyWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Таблица 'Вакансии'")
        self.geometry("1000x400")

        # Создаем виджет Treeview для отображения данных таблицы "Вакансия"
        self.tree = ttk.Treeview(self, columns=(
            "ID", "Name", "Requirements", "Working Conditions"))

        self.tree.heading("#0", text="")
        self.tree.heading("#1", text="ID")
        self.tree.heading("#2", text="Name")
        self.tree.heading("#3", text="Requirements")
        self.tree.heading("#4", text="Working Conditions")

        # Устанавливаем ширину колонок
        self.tree.column("#0", width=0)
        self.tree.column("#1", width=40)
        self.tree.column("#2", width=150)
        self.tree.column("#3", width=350)
        self.tree.column("#4", width=350)

        self.tree.pack()

        # Кнопка для добавления вакансии
        self.add_vacancy_button = tk.Button(self, text="Добавить вакансию", command=self.add_vacancy)
        self.add_vacancy_button.pack()

        # Обновляем таблицу "Вакансия" при открытии окна
        self.update_vacancy_table()

    def update_vacancy_table(self):
        self.tree.delete(*self.tree.get_children())
        cursor.execute("SELECT * FROM vacancy")
        data = cursor.fetchall()
        for row in data:
            self.tree.insert("", "end", values=row)

    def add_vacancy(self):
        # Ваш код для добавления вакансии в базу данных
        pass


# Окно для работы с таблицей "Заявка на вакансию"
class ApplicationWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Таблица 'Заявки на вакансии'")
        self.geometry("400x400")

        # Создаем виджет Treeview для отображения данных таблицы "Заявка на вакансию"
        self.tree = ttk.Treeview(self, columns=(
            "ID", "Application Date", "Status"))

        self.tree.heading("#0", text="")
        self.tree.heading("#1", text="ID")
        self.tree.heading("#2", text="Application Date")
        self.tree.heading("#3", text="Status")

        # Устанавливаем ширину колонок
        self.tree.column("#0", width=0)
        self.tree.column("#1", width=40)
        self.tree.column("#2", width=150)
        self.tree.column("#3", width=150)

        self.tree.pack()

        # Кнопка для добавления заявки на вакансию
        self.add_application_button = tk.Button(self, text="Добавить заявку", command=self.add_application)
        self.add_application_button.pack()

        # Обновляем таблицу "Заявка на вакансию" при открытии окна
        self.update_application_table()

    def update_application_table(self):
        self.tree.delete(*self.tree.get_children())
        cursor.execute("SELECT * FROM application")
        data = cursor.fetchall()
        for row in data:
            self.tree.insert("", "end", values=row)

    def add_application(self):
        # Ваш код для добавления заявки на вакансию в базу данных
        pass


# Главное окно приложения
app = MainApp()
app.mainloop()
