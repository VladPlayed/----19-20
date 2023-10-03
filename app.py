import sqlite3
import tkinter as tk
from tkinter import ttk, simpledialog
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

        # Создаем атрибут для хранения окна добавления
        self.add_employee_dialog = None
        
        # Обновляем таблицу "Сотрудник" при открытии окна
        self.update_employee_table()

    def update_employee_table(self):
        self.tree.delete(*self.tree.get_children())
        cursor.execute("SELECT * FROM employee")
        data = cursor.fetchall()
        for row in data:
            self.tree.insert("", "end", values=row)

    # Функция для добавления нового сотрудника в базу данных
    def add_employee(self):
        # Создаем окно для ввода данных сотрудника
        self.add_employee_dialog = tk.Toplevel(self)
        self.add_employee_dialog.title("Добавить сотрудника")

        # Создаем и размещаем подписи к полям
        tk.Label(self.add_employee_dialog, text="ФИО:").grid(row=0, column=0, padx=10, pady=5)
        tk.Label(self.add_employee_dialog, text="Пол:").grid(row=1, column=0, padx=10, pady=5)
        tk.Label(self.add_employee_dialog, text="Дата рождения:").grid(row=2, column=0, padx=10, pady=5)
        tk.Label(self.add_employee_dialog, text="Образование:").grid(row=3, column=0, padx=10, pady=5)
        tk.Label(self.add_employee_dialog, text="Должность:").grid(row=4, column=0, padx=10, pady=5)
        tk.Label(self.add_employee_dialog, text="Профессия:").grid(row=5, column=0, padx=10, pady=5)
        tk.Label(self.add_employee_dialog, text="Дата приема на работу:").grid(row=6, column=0, padx=10, pady=5)
        tk.Label(self.add_employee_dialog, text="Зарплата:").grid(row=7, column=0, padx=10, pady=5)
        tk.Label(self.add_employee_dialog, text="Паспортные данные:").grid(row=8, column=0, padx=10, pady=5)
        tk.Label(self.add_employee_dialog, text="Адрес:").grid(row=9, column=0, padx=10, pady=5)

        # Создаем и размещаем поля ввода
        self.name_entry = tk.Entry(self.add_employee_dialog)
        self.name_entry.grid(row=0, column=1, padx=10, pady=5)
        self.gender_entry = tk.Entry(self.add_employee_dialog)
        self.gender_entry.grid(row=1, column=1, padx=10, pady=5)
        self.birth_date_entry = tk.Entry(self.add_employee_dialog)
        self.birth_date_entry.grid(row=2, column=1, padx=10, pady=5)
        self.education_entry = tk.Entry(self.add_employee_dialog)
        self.education_entry.grid(row=3, column=1, padx=10, pady=5)
        self.position_entry = tk.Entry(self.add_employee_dialog)
        self.position_entry.grid(row=4, column=1, padx=10, pady=5)
        self.profession_entry = tk.Entry(self.add_employee_dialog)
        self.profession_entry.grid(row=5, column=1, padx=10, pady=5)
        self.hire_date_entry = tk.Entry(self.add_employee_dialog)
        self.hire_date_entry.grid(row=6, column=1, padx=10, pady=5)
        self.salary_entry = tk.Entry(self.add_employee_dialog)
        self.salary_entry.grid(row=7, column=1, padx=10, pady=5)
        self.passport_data_entry = tk.Entry(self.add_employee_dialog)
        self.passport_data_entry.grid(row=8, column=1, padx=10, pady=5)
        self.address_entry = tk.Entry(self.add_employee_dialog)
        self.address_entry.grid(row=9, column=1, padx=10, pady=5)

        # Создаем кнопку для добавления сотрудника
        add_button = tk.Button(self.add_employee_dialog, text="Добавить", command=self.insert_employee)
        add_button.grid(row=10, columnspan=2, padx=10, pady=10)


    def insert_employee(self):
        # Получите данные из полей ввода
        name = self.name_entry.get()
        gender = self.gender_entry.get()
        birth_date = self.birth_date_entry.get()
        education = self.education_entry.get()
        position = self.position_entry.get()
        profession = self.profession_entry.get()
        hire_date = self.hire_date_entry.get()
        salary = self.salary_entry.get()
        passport_data = self.passport_data_entry.get()
        address = self.address_entry.get()

        # Вставьте данные в базу данных
        cursor.execute("INSERT INTO employee (full_name, gender, birth_date, education, position, profession, hire_date, salary, passport_data, address) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                       (name, gender, birth_date, education, position, profession, hire_date, salary, passport_data, address))
        conn.commit()  # Сохраните изменения в базе данных
        self.update_employee_table()  # Обновите таблицу сотрудников
        if self.add_employee_dialog:
            self.add_employee_dialog.destroy()
            
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
        # Создаем окно для ввода данных отдела
        self.add_department_dialog = tk.Toplevel(self)
        self.add_department_dialog.title("Добавить отдел")

        # Создаем и размещаем подписи к полям
        tk.Label(self.add_department_dialog, text="Название:").grid(row=0, column=0, padx=10, pady=5)
        tk.Label(self.add_department_dialog, text="Руководитель:").grid(row=1, column=0, padx=10, pady=5)
        tk.Label(self.add_department_dialog, text="Контактная информация:").grid(row=2, column=0, padx=10, pady=5)
        tk.Label(self.add_department_dialog, text="ID сотрудника:").grid(row=3, column=0, padx=10, pady=5)

        # Создаем и размещаем поля ввода
        self.name_entry = tk.Entry(self.add_department_dialog)
        self.name_entry.grid(row=0, column=1, padx=10, pady=5)
        self.head_entry = tk.Entry(self.add_department_dialog)
        self.head_entry.grid(row=1, column=1, padx=10, pady=5)
        self.contact_info_entry = tk.Entry(self.add_department_dialog)
        self.contact_info_entry.grid(row=2, column=1, padx=10, pady=5)
        self.employee_id_entry = tk.Entry(self.add_department_dialog)
        self.employee_id_entry.grid(row=3, column=1, padx=10, pady=5)

        # Создаем кнопку для добавления отдела
        add_button = tk.Button(self.add_department_dialog, text="Добавить", command=self.insert_department)
        add_button.grid(row=4, columnspan=2, padx=10, pady=10)

    # Функция для вставки данных отдела в базу данных
    def insert_department(self):
        # Получите данные из полей ввода
        name = self.name_entry.get()
        head = self.head_entry.get()
        contact_info = self.contact_info_entry.get()
        employee_id = self.employee_id_entry.get()

        # Вставьте данные в таблицу "Отдел" в базе данных
        cursor.execute("INSERT INTO department (name, head, contact_info, employee_id) VALUES (?, ?, ?, ?)",
                    (name, head, contact_info, employee_id))
        conn.commit()  # Сохраните изменения в базе данных
        self.update_department_table()  # Обновите таблицу отделов
        if self.add_department_dialog:
            self.add_department_dialog.destroy()

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
        # Создаем окно для ввода данных вакансии
        self.add_vacancy_dialog = tk.Toplevel(self)
        self.add_vacancy_dialog.title("Добавить вакансию")

        # Создаем и размещаем подписи к полям
        tk.Label(self.add_vacancy_dialog, text="Название:").grid(row=0, column=0, padx=10, pady=5)
        tk.Label(self.add_vacancy_dialog, text="Требования:").grid(row=1, column=0, padx=10, pady=5)
        tk.Label(self.add_vacancy_dialog, text="Условия работы:").grid(row=2, column=0, padx=10, pady=5)

        # Создаем и размещаем поля ввода
        self.name_entry = tk.Entry(self.add_vacancy_dialog)
        self.name_entry.grid(row=0, column=1, padx=10, pady=5)
        self.requirements_entry = tk.Entry(self.add_vacancy_dialog)
        self.requirements_entry.grid(row=1, column=1, padx=10, pady=5)
        self.working_conditions_entry = tk.Entry(self.add_vacancy_dialog)
        self.working_conditions_entry.grid(row=2, column=1, padx=10, pady=5)

        # Создаем кнопку для добавления вакансии
        add_button = tk.Button(self.add_vacancy_dialog, text="Добавить", command=self.insert_vacancy)
        add_button.grid(row=3, columnspan=2, padx=10, pady=10)

    # Функция для вставки данных вакансии в базу данных
    def insert_vacancy(self):
        # Получите данные из полей ввода
        name = self.name_entry.get()
        requirements = self.requirements_entry.get()
        working_conditions = self.working_conditions_entry.get()

        # Вставьте данные в таблицу "Вакансия" в базе данных
        cursor.execute("INSERT INTO vacancy (name, requirements, working_conditions) VALUES (?, ?, ?)",
                    (name, requirements, working_conditions))
        conn.commit()  # Сохраните изменения в базе данных
        self.update_vacancy_table()  # Обновите таблицу вакансий
        if self.add_vacancy_dialog:
            self.add_vacancy_dialog.destroy()
            
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
        # Создаем окно для ввода данных заявки на вакансию
        self.add_application_dialog = tk.Toplevel(self)
        self.add_application_dialog.title("Добавить заявку на вакансию")

        # Создаем и размещаем подписи к полям
        tk.Label(self.add_application_dialog, text="Дата подачи:").grid(row=0, column=0, padx=10, pady=5)
        tk.Label(self.add_application_dialog, text="Статус:").grid(row=1, column=0, padx=10, pady=5)

        # Создаем и размещаем поля ввода
        self.application_date_entry = tk.Entry(self.add_application_dialog)
        self.application_date_entry.grid(row=0, column=1, padx=10, pady=5)
        self.status_entry = tk.Entry(self.add_application_dialog)
        self.status_entry.grid(row=1, column=1, padx=10, pady=5)

        # Создаем кнопку для добавления заявки на вакансию
        add_button = tk.Button(self.add_application_dialog, text="Добавить", command=self.insert_application)
        add_button.grid(row=2, columnspan=2, padx=10, pady=10)
    
    # Функция для вставки данных заявки на вакансию в базу данных
    def insert_application(self):
        # Получите данные из полей ввода
        application_date = self.application_date_entry.get()
        status = self.status_entry.get()

        # Вставьте данные в таблицу "Заявка на вакансию" в базе данных
        cursor.execute("INSERT INTO application (application_date, status) VALUES (?, ?)",
                    (application_date, status))
        conn.commit()  # Сохраните изменения в базе данных
        self.update_application_table()  # Обновите таблицу заявок на вакансии
        if self.add_application_dialog:
            self.add_application_dialog.destroy()

# Главное окно приложения
app = MainApp()
app.mainloop()
