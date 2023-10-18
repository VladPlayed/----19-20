import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
from PIL import Image, ImageTk
import pandas as pd

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

        # Кнопки для справочников
        label = tk.Label(self, text="Справочники")
        label.grid(row=3, column=0, columnspan=2)
        gender_button = tk.Button(self, text="Пол", command=self.open_gender_window)
        education_button = tk.Button(self, text="Образование", command=self.open_education_window)
        position_button = tk.Button(self, text="Должности", command=self.open_position_window)
        profession_button = tk.Button(self, text="Профессии", command=self.open_profession_window)

        # Располагаем кнопки 2 на 2 в ячейках сетки
        employee_button.grid(row=1, column=0)
        department_button.grid(row=1, column=1)
        vacancy_button.grid(row=2, column=0)
        application_button.grid(row=2, column=1)

        # Размещаем кнопки справочников
        gender_button.grid(row=4, column=0)
        education_button.grid(row=4, column=1)
        position_button.grid(row=5, column=0)
        profession_button.grid(row=5, column=1)

    def open_employee_window(self):
        EmployeeWindow(self)

    def open_department_window(self):
        DepartmentWindow(self)

    def open_vacancy_window(self):
        VacancyWindow(self)

    def open_application_window(self):
        ApplicationWindow(self)

    def open_gender_window(self):
        GenderWindow(self)

    def open_education_window(self):
        EducationWindow(self)

    def open_position_window(self):
        PositionWindow(self)

    def open_profession_window(self):
        ProfessionWindow(self)

# Окно для работы с таблицей "Сотрудники"
class EmployeeWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Таблица 'Сотрудники'")
        self.geometry("1300x400")

        # Создаем виджет Treeview для отображения данных таблицы "Сотрудники"
        self.tree = ttk.Treeview(self, columns=(
            "ID", "Full Name", "Gender", "Birth Date", "Education", "Position", "Profession", "Employment Date",
            "Salary", "Passport Data", "Address", "Department ID"))

        self.tree.heading("#0", text="")
        self.tree.heading("#1", text="ID")
        self.tree.heading("#2", text="Full Name")
        self.tree.heading("#3", text="Gender")
        self.tree.heading("#4", text="Birth Date")
        self.tree.heading("#5", text="Education")
        self.tree.heading("#6", text="Position")
        self.tree.heading("#7", text="Profession")
        self.tree.heading("#8", text="Employment Date")
        self.tree.heading("#9", text="Salary")
        self.tree.heading("#10", text="Passport Data")
        self.tree.heading("#11", text="Address")
        self.tree.heading("#12", text="Department ID")

        # Устанавливаем ширину колонок
        self.tree.column("#0", width=0)
        self.tree.column("#1", width=40)
        self.tree.column("#2", width=170)
        self.tree.column("#3", width=50)
        self.tree.column("#4", width=130)
        self.tree.column("#5", width=70)
        self.tree.column("#6", width=70)
        self.tree.column("#7", width=70)
        self.tree.column("#8", width=115)
        self.tree.column("#9", width=70)
        self.tree.column("#10", width=100)
        self.tree.column("#11", width=250)
        self.tree.column("#12", width=140)

        self.tree.pack()

        # Создаем фрейм для размещения кнопок в ряд
        button_frame = tk.Frame(self)
        button_frame.pack()

        # Кнопка для добавления сотрудника
        self.add_employee_button = tk.Button(button_frame, text="Добавить сотрудника", command=self.add_employee)
        self.add_employee_button.pack(side=tk.LEFT, padx=10, pady=5)

        # Кнопка для удаления сотрудника
        self.delete_employee_button = tk.Button(button_frame, text="Удалить сотрудника", command=self.delete_employee)
        self.delete_employee_button.pack(side=tk.LEFT, padx=10, pady=5)

        # Кнопка для редактирования сотрудника
        self.edit_employee_button = tk.Button(button_frame, text="Редактировать сотрудника", command=self.edit_employee)
        self.edit_employee_button.pack(side=tk.LEFT, padx=10, pady=5)

        # Создаем поле ввода для поиска сотрудника
        self.search_entry = tk.Entry(self)
        self.search_entry.pack()

        # Кнопка для поиска сотрудника
        search_employee_button = tk.Button(self, text="Найти сотрудника", command=self.search_employee)
        search_employee_button.pack()

        # Создаем атрибут для хранения окна добавления
        self.add_employee_dialog = None

        # Кнопка для экспорта данных в Excel
        export_button = tk.Button(self, text="Экспорт в Excel", command=self.export_to_excel)
        export_button.pack()

        # Обновляем таблицу "Сотрудники" при открытии окна
        self.update_employee_table()

    def update_employee_table(self):
        self.tree.delete(*self.tree.get_children())
        cursor.execute("SELECT * FROM employee")
        data = cursor.fetchall()
        for row in data:
            self.tree.insert("", "end", values=row)

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
        tk.Label(self.add_employee_dialog, text="Дата поступления:").grid(row=6, column=0, padx=10, pady=5)
        tk.Label(self.add_employee_dialog, text="Оклад:").grid(row=7, column=0, padx=10, pady=5)
        tk.Label(self.add_employee_dialog, text="Паспортные данные:").grid(row=8, column=0, padx=10, pady=5)
        tk.Label(self.add_employee_dialog, text="Адрес:").grid(row=9, column=0, padx=10, pady=5)
        tk.Label(self.add_employee_dialog, text="Отдел:").grid(row=10, column=0, padx=10, pady=5)

        # Создаем и размещаем поля ввода
        self.full_name_entry = tk.Entry(self.add_employee_dialog)
        self.full_name_entry.grid(row=0, column=1, padx=10, pady=5)
        self.gender_entry = tk.Entry(self.add_employee_dialog)
        self.gender_entry.grid(row=1, column=1, padx=10, pady=5)
        self.birthdate_entry = tk.Entry(self.add_employee_dialog)
        self.birthdate_entry.grid(row=2, column=1, padx=10, pady=5)
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
        self.passport_entry = tk.Entry(self.add_employee_dialog)
        self.passport_entry.grid(row=8, column=1, padx=10, pady=5)
        self.address_entry = tk.Entry(self.add_employee_dialog)
        self.address_entry.grid(row=9, column=1, padx=10, pady=5)
        self.department_entry = tk.Entry(self.add_employee_dialog)
        self.department_entry.grid(row=10, column=1, padx=10, pady=5)

        # Создаем кнопку для добавления сотрудника
        add_button = tk.Button(self.add_employee_dialog, text="Добавить", command=self.insert_employee)
        add_button.grid(row=11, columnspan=2, padx=10, pady=10)

    # Функция для вставки данных сотрудника в базу данных
    def insert_employee(self):
        # Получите данные из полей ввода
        full_name = self.full_name_entry.get()
        gender = self.gender_entry.get()
        birthdate = self.birthdate_entry.get()
        education = self.education_entry.get()
        position = self.position_entry.get()
        profession = self.profession_entry.get()
        hire_date = self.hire_date_entry.get()
        salary = self.salary_entry.get()
        passport = self.passport_entry.get()
        address = self.address_entry.get()
        department_id = self.department_entry.get()

        # Вставьте данные в таблицу "Сотрудники" в базе данных
        cursor.execute(
            "INSERT INTO employee (full_name, gender_id, birth_date, education_id, position_id, profession_id, employment_date, salary, passport_data, address, department_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (full_name, gender, birthdate, education, position, profession, hire_date, salary, passport, address, department_id))
        conn.commit()  # Сохраните изменения в базе данных
        self.update_employee_table()  # Обновите таблицу сотрудников
        if self.add_employee_dialog:
            self.add_employee_dialog.destroy()

    def delete_employee(self):
        try:
            employee_id = self.tree.item(self.tree.selection())['values'][0]
            cursor.execute("DELETE FROM employee WHERE employee_id=?", (employee_id,))
            conn.commit()
            self.update_employee_table()
        except IndexError:
            showinfo(title="Внимание!", message="Выберите запись для удаления")

    # Функция для редактирования данных сотрудника
    def edit_employee(self):
        selected_item = self.tree.selection()
        if selected_item:
            # Получите данные выбранной записи
            employee_id = self.tree.item(selected_item)['values'][0]
            # Откройте окно для редактирования с передачей идентификатора сотрудника и ссылки на EmployeeWindow
            EditEmployeeWindow(self, employee_id, self)
        else:
            showinfo(title="Внимание!", message="Выберите запись для редактирования")

    # Функция для поиска сотрудников
    def display_search_results(self, data):
        # Очистите виджет Treeview
        self.tree.delete(*self.tree.get_children())

        # Вставьте найденные записи в виджет Treeview
        for row in data:
            self.tree.insert("", "end", values=row)

    def search_employee(self):
        search_query = '%' + self.search_entry.get() + '%'
        cursor.execute(
            "SELECT * FROM employee WHERE full_name LIKE ? OR passport_data LIKE ? OR address LIKE ? OR department_id LIKE ?",
            (search_query, search_query, search_query, search_query))
        data = cursor.fetchall()

        # Вызовите функцию для отображения результатов поиска
        self.display_search_results(data)
    def export_to_excel(self):
        # Получите данные из базы данных
        cursor.execute("SELECT * FROM employee")
        data = cursor.fetchall()

        # Создайте DataFrame из данных
        df = pd.DataFrame(data, columns=["ID", "Full Name", "Gender", "Birth Date", "Education",
            "Position", "Profession", "Employment Date", "Salary", "Passport Data", "Address", "Department ID"])
        
        # Укажите путь к файлу Excel
        excel_file_path = "employees.xlsx"

        # Создайте объект writer для записи данных в Excel
        writer = pd.ExcelWriter(excel_file_path, engine='xlsxwriter')

        # Запишите DataFrame в файл Excel
        df.to_excel(writer, 'Лист 1', index=False)

        # Сохраните результат
        writer.close()

        showinfo(title="Успешно", message=f"Данные экспортированы в {excel_file_path}")

# Окно для редактирования данных сотрудника
class EditEmployeeWindow(tk.Toplevel):
    def __init__(self, parent, employee_id, employee_window):
        super().__init__(parent)
        self.title("Редактировать сотрудника")
        self.employee_id = employee_id  # Сохраняем значение employee_id как атрибут экземпляра
        self.employee_window = employee_window  # Сохраняем ссылку на экземпляр EmployeeWindow

        # Получите данные сотрудника по его идентификатору
        cursor.execute(
            "SELECT * FROM employee WHERE employee_id=?", (employee_id,))
        self.employee_data = cursor.fetchone()  # Сохраняем данные сотрудника

        # Создаем и размещаем подписи к полям
        tk.Label(self, text="ФИО:").grid(row=0, column=0, padx=10, pady=5)
        tk.Label(self, text="Пол:").grid(row=1, column=0, padx=10, pady=5)
        tk.Label(self, text="Дата рождения:").grid(row=2, column=0, padx=10, pady=5)
        tk.Label(self, text="Образование:").grid(row=3, column=0, padx=10, pady=5)
        tk.Label(self, text="Должность:").grid(row=4, column=0, padx=10, pady=5)
        tk.Label(self, text="Профессия:").grid(row=5, column=0, padx=10, pady=5)
        tk.Label(self, text="Дата поступления:").grid(row=6, column=0, padx=10, pady=5)
        tk.Label(self, text="Оклад:").grid(row=7, column=0, padx=10, pady=5)
        tk.Label(self, text="Паспортные данные:").grid(row=8, column=0, padx=10, pady=5)
        tk.Label(self, text="Адрес:").grid(row=9, column=0, padx=10, pady=5)
        tk.Label(self, text="Отдел:").grid(row=10, column=0, padx=10, pady=5)

        # Создаем и размещаем поля ввода, заполняя их текущими данными сотрудника
        self.full_name_entry = tk.Entry(self)
        self.full_name_entry.grid(row=0, column=1, padx=10, pady=5)
        self.full_name_entry.insert(0, self.employee_data[1])

        self.gender_entry = tk.Entry(self)
        self.gender_entry.grid(row=1, column=1, padx=10, pady=5)
        self.gender_entry.insert(0, self.employee_data[2])

        self.birthdate_entry = tk.Entry(self)
        self.birthdate_entry.grid(row=2, column=1, padx=10, pady=5)
        self.birthdate_entry.insert(0, self.employee_data[3])

        self.education_entry = tk.Entry(self)
        self.education_entry.grid(row=3, column=1, padx=10, pady=5)
        self.education_entry.insert(0, self.employee_data[4])

        self.position_entry = tk.Entry(self)
        self.position_entry.grid(row=4, column=1, padx=10, pady=5)
        self.position_entry.insert(0, self.employee_data[5])

        self.profession_entry = tk.Entry(self)
        self.profession_entry.grid(row=5, column=1, padx=10, pady=5)
        self.profession_entry.insert(0, self.employee_data[6])

        self.hire_date_entry = tk.Entry(self)
        self.hire_date_entry.grid(row=6, column=1, padx=10, pady=5)
        self.hire_date_entry.insert(0, self.employee_data[7])

        self.salary_entry = tk.Entry(self)
        self.salary_entry.grid(row=7, column=1, padx=10, pady=5)
        self.salary_entry.insert(0, self.employee_data[8])

        self.passport_entry = tk.Entry(self)
        self.passport_entry.grid(row=8, column=1, padx=10, pady=5)
        self.passport_entry.insert(0, self.employee_data[9])

        self.address_entry = tk.Entry(self)
        self.address_entry.grid(row=9, column=1, padx=10, pady=5)
        self.address_entry.insert(0, self.employee_data[10])

        self.department_entry = tk.Entry(self)
        self.department_entry.grid(row=10, column=1, padx=10, pady=5)
        self.department_entry.insert(0, self.employee_data[11])

        # Создаем кнопку для сохранения изменений
        save_button = tk.Button(self, text="Сохранить", command=self.save_employee)
        save_button.grid(row=11, columnspan=2, padx=10, pady=10)

    def save_employee(self):
        # Получите новые данные из полей ввода
        new_full_name = self.full_name_entry.get()
        new_gender = self.gender_entry.get()
        new_birthdate = self.birthdate_entry.get()
        new_education = self.education_entry.get()
        new_position = self.position_entry.get()
        new_profession = self.profession_entry.get()
        new_employment_date = self.hire_date_entry.get()
        new_salary = float(self.salary_entry.get())
        new_passport = self.passport_entry.get()
        new_address = self.address_entry.get()
        new_department_id = self.department_entry.get()

        # Обновите все поля данных сотрудника в базе данных
        cursor.execute(
            "UPDATE employee SET full_name=?, gender_id=?, birth_date=?, education_id=?, position_id=?, profession_id=?, employment_date=?, salary=?, passport_data=?, address=?, department_id=? WHERE employee_id=?",
            (new_full_name, new_gender, new_birthdate, new_education, new_position, new_profession, new_employment_date,
             new_salary, new_passport, new_address, new_department_id, self.employee_id))
        conn.commit()

        # Закройте окно редактирования
        self.destroy()

        # Обновите таблицу сотрудников, вызвав метод из EmployeeWindow
        self.employee_window.update_employee_table()

    def __init__(self, parent, employee_id, employee_window):
        super().__init__(parent)
        self.title("Редактировать сотрудника")
        self.employee_id = employee_id  # Сохраняем значение employee_id как атрибут экземпляра
        self.employee_window = employee_window  # Сохраняем ссылку на экземпляр EmployeeWindow

        # Получите данные сотрудника по его идентификатору
        cursor.execute("SELECT * FROM employee WHERE employee_id=?", (employee_id,))
        self.employee_data = cursor.fetchone()  # Сохраняем данные сотрудника

        # Создаем и размещаем подписи к полям
        tk.Label(self, text="ФИО:").grid(row=0, column=0, padx=10, pady=5)
        tk.Label(self, text="Пол:").grid(row=1, column=0, padx=10, pady=5)
        tk.Label(self, text="Дата рождения:").grid(row=2, column=0, padx=10, pady=5)
        tk.Label(self, text="Образование:").grid(row=3, column=0, padx=10, pady=5)
        tk.Label(self, text="Должность:").grid(row=4, column=0, padx=10, pady=5)
        tk.Label(self, text="Профессия:").grid(row=5, column=0, padx=10, pady=5)
        tk.Label(self, text="Дата приема на работу:").grid(row=6, column=0, padx=10, pady=5)
        tk.Label(self, text="Зарплата:").grid(row=7, column=0, padx=10, pady=5)
        tk.Label(self, text="Паспортные данные:").grid(row=8, column=0, padx=10, pady=5)
        tk.Label(self, text="Адрес:").grid(row=9, column=0, padx=10, pady=5)
        tk.Label(self, text="Отдел:").grid(row=10, column=0, padx=10, pady=5)

        # Создаем и размещаем поля ввода, заполняя их текущими данными сотрудника
        self.full_name_entry = tk.Entry(self)
        self.full_name_entry.grid(row=0, column=1, padx=10, pady=5)
        self.full_name_entry.insert(0, self.employee_data[1])
        self.gender_entry = tk.Entry(self)
        self.gender_entry.grid(row=1, column=1, padx=10, pady=5)
        self.gender_entry.insert(0, self.employee_data[2])
        self.birth_date_entry = tk.Entry(self)
        self.birth_date_entry.grid(row=2, column=1, padx=10, pady=5)
        self.birth_date_entry.insert(0, self.employee_data[3])
        self.education_entry = tk.Entry(self)
        self.education_entry.grid(row=3, column=1, padx=10, pady=5)
        self.education_entry.insert(0, self.employee_data[4])
        self.position_entry = tk.Entry(self)
        self.position_entry.grid(row=4, column=1, padx=10, pady=5)
        self.position_entry.insert(0, self.employee_data[5])
        self.profession_entry = tk.Entry(self)
        self.profession_entry.grid(row=5, column=1, padx=10, pady=5)
        self.profession_entry.insert(0, self.employee_data[6])
        self.hire_date_entry = tk.Entry(self)
        self.hire_date_entry.grid(row=6, column=1, padx=10, pady=5)
        self.hire_date_entry.insert(0, self.employee_data[7])
        self.salary_entry = tk.Entry(self)
        self.salary_entry.grid(row=7, column=1, padx=10, pady=5)
        self.salary_entry.insert(0, self.employee_data[8])
        self.passport_data_entry = tk.Entry(self)
        self.passport_data_entry.grid(row=8, column=1, padx=10, pady=5)
        self.passport_data_entry.insert(0, self.employee_data[9])
        self.address_entry = tk.Entry(self)
        self.address_entry.grid(row=9, column=1, padx=10, pady=5)
        self.address_entry.insert(0, self.employee_data[10])
        self.department_entry = tk.Entry(self)
        self.department_entry.grid(row=10, column=1, padx=10, pady=5)
        self.department_entry.insert(0, self.employee_data[11])

        # Создаем кнопку для сохранения изменений
        save_button = tk.Button(self, text="Сохранить", command=self.save_employee)
        save_button.grid(row=11, columnspan=2, padx=10, pady=10)

    def save_employee(self):
        # Получите новые данные из полей ввода
        new_full_name = self.full_name_entry.get()
        new_gender = self.gender_entry.get()
        new_birth_date = self.birth_date_entry.get()
        new_education = self.education_entry.get()
        new_position = self.position_entry.get()
        new_profession = self.profession_entry.get()
        new_employment_date = self.hire_date_entry.get()
        new_salary = self.salary_entry.get()
        new_passport_data = self.passport_data_entry.get()
        new_address = self.address_entry.get()
        new_department_id = self.department_entry.get()

        # Обновите все поля данных сотрудника в базе данных
        cursor.execute("UPDATE employee SET full_name=?, gender_id=?, birth_date=?, education_id=?, position_id=?, profession_id=?, employment_date=?, salary=?, passport_data=?, address=?, department_id=? WHERE employee_id=?",
                       (new_full_name, new_gender, new_birth_date, new_education, new_position, new_profession, new_employment_date, new_salary, new_passport_data, new_address, new_department_id, self.employee_id))
        conn.commit()

        # Закройте окно редактирования
        self.destroy()

        # Обновите таблицу сотрудников, вызвав метод из EmployeeWindow
        self.employee_window.update_employee_table()

# Окно для работы с таблицей "Отдел"
class DepartmentWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Таблица 'Отделы'")
        self.geometry("800x350")

        # Создаем виджет Treeview для отображения данных таблицы "Отдел"
        self.tree = ttk.Treeview(self, columns=(
            "Departament ID", "Name", "Head", "Contact Info"))

        self.tree.heading("#0", text="")
        self.tree.heading("#1", text="Departament ID")
        self.tree.heading("#2", text="Name")
        self.tree.heading("#3", text="Head")
        self.tree.heading("#4", text="Contact Info")

        # Устанавливаем ширину колонок
        self.tree.column("#0", width=0)
        self.tree.column("#1", width=100)
        self.tree.column("#2", width=150)
        self.tree.column("#3", width=160)
        self.tree.column("#4", width=250)

        self.tree.pack()

        # Создаем фрейм для размещения кнопок в ряд
        button_frame = tk.Frame(self)
        button_frame.pack()

        # Кнопка для добавления отдела
        self.add_department_button = tk.Button(button_frame, text="Добавить отдел", command=self.add_department)
        self.add_department_button.pack(side=tk.LEFT, padx=10, pady=5)

        # Кнопка для удаления отдела
        self.delete_department_button = tk.Button(button_frame, text="Удалить отдел", command=self.delete_department)
        self.delete_department_button.pack(side=tk.LEFT, padx=10, pady=5)

        # Кнопка для редактирования отдела
        self.edit_department_button = tk.Button(button_frame, text="Редактировать отдел", command=self.edit_department)
        self.edit_department_button.pack(side=tk.LEFT, padx=10, pady=5)

        # Создаем поле ввода для поиска отдела
        self.search_entry = tk.Entry(self)
        self.search_entry.pack()

        # Кнопка для поиска отдела
        search_department_button = tk.Button(self, text="Найти отдел", command=self.search_department)
        search_department_button.pack()

        # Создаем атрибут для хранения окна добавления
        self.add_department_dialog = None

        # Кнопка для экспорта данных в Excel
        export_button = tk.Button(self, text="Экспорт в Excel", command=self.export_to_excel)
        export_button.pack()

        # Обновляем таблицу "Отделы" при открытии окна
        self.update_department_table()

    def update_department_table(self, data=None):
        self.tree.delete(*self.tree.get_children())
        cursor.execute("SELECT * FROM department")
        data = cursor.fetchall()
        for row in data:
            self.tree.insert("", "end", values=row)

    # Функция для добавления нового отдела в базу данных
    def add_department(self):
        # Создаем окно для ввода данных отдела
        self.add_department_dialog = tk.Toplevel(self)
        self.add_department_dialog.title("Добавить отдел")

        # Создаем и размещаем подписи к полям
        tk.Label(self.add_department_dialog, text="Название отдела:").grid(row=0, column=0, padx=10, pady=5)

        # Создаем и размещаем поле ввода
        self.department_name_entry = tk.Entry(self.add_department_dialog)
        self.department_name_entry.grid(row=0, column=1, padx=10, pady=5)

        # Создаем кнопку для добавления отдела
        add_button = tk.Button(self.add_department_dialog, text="Добавить", command=self.insert_department)
        add_button.grid(row=1, columnspan=2, padx=10, pady=10)

    def insert_department(self):
        # Получите данные из поля ввода
        department_name = self.department_name_entry.get()

        # Вставьте данные в базу данных
        cursor.execute("INSERT INTO department (department_name) VALUES (?)", (department_name,))
        conn.commit()  # Сохраните изменения в базе данных
        self.update_department_table()  # Обновите таблицу отделов
        if self.add_department_dialog:
            self.add_department_dialog.destroy()

    # Функция для удаления отдела из базы данных
    def delete_department(self):
        try:
            department_id = self.tree.item(self.tree.selection())['values'][0]
            cursor.execute("DELETE FROM department WHERE department_id=?", (department_id,))
            conn.commit()
            self.update_department_table()
        except IndexError:
            showinfo(title="Внимание!", message="Выберите запись для удаления")

    # Функция для редактирования данных отдела
    def edit_department(self):
        selected_item = self.tree.selection()
        if selected_item:
            # Получите данные выбранной записи
            department_id = self.tree.item(selected_item)['values'][0]
            # Откройте окно для редактирования с передачей идентификатора отдела и ссылки на DepartmentWindow
            EditDepartmentWindow(self, department_id, self)
        else:
            showinfo(title="Внимание!", message="Выберите запись для редактирования")

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

        # Создаем и размещаем поля ввода
        self.name_entry = tk.Entry(self.add_department_dialog)
        self.name_entry.grid(row=0, column=1, padx=10, pady=5)
        self.head_entry = tk.Entry(self.add_department_dialog)
        self.head_entry.grid(row=1, column=1, padx=10, pady=5)
        self.contact_info_entry = tk.Entry(self.add_department_dialog)
        self.contact_info_entry.grid(row=2, column=1, padx=10, pady=5)

        # Создаем кнопку для добавления отдела
        add_button = tk.Button(self.add_department_dialog, text="Добавить", command=self.insert_department)
        add_button.grid(row=3, columnspan=2, padx=10, pady=10)

    # Функция для вставки данных отдела в базу данных
    def insert_department(self):
        # Получите данные из полей ввода
        name = self.name_entry.get()
        head = self.head_entry.get()
        contact_info = self.contact_info_entry.get()

        # Вставьте данные в таблицу "Отдел" в базе данных
        cursor.execute("INSERT INTO department (name, head, contact_info) VALUES (?, ?, ?)",
                    (name, head, contact_info))
        conn.commit()  # Сохраните изменения в базе данных
        self.update_department_table()  # Обновите таблицу отделов
        if self.add_department_dialog:
            self.add_department_dialog.destroy()

    # Функция для отображения результатов поиска
    def display_search_results(self, data):
        # Очистите виджет Treeview
        self.tree.delete(*self.tree.get_children())

        # Вставьте найденные записи в виджет Treeview
        for row in data:
            self.tree.insert("", "end", values=row)

    # Функция для поиска отделов
    def search_department(self):
        search_query = '%' + self.search_entry.get() + '%'
        cursor.execute("SELECT * FROM department WHERE Name LIKE ?", (search_query,))
        data = cursor.fetchall()

        # Вызовите функцию для отображения результатов поиска
        self.display_search_results(data)
    
    def export_to_excel(self):
        # Получите данные из базы данных
        cursor.execute("SELECT * FROM department")
        data = cursor.fetchall()

        # Создайте DataFrame из данных
        df = pd.DataFrame(data, columns=["ID", "Name", "Head", "Contact Info"])

        # Укажите путь к файлу Excel
        excel_file_path = "departments.xlsx"

        # Создайте объект writer для записи данных в Excel
        writer = pd.ExcelWriter(excel_file_path, engine='xlsxwriter')

        # Запишите DataFrame в файл Excel
        df.to_excel(writer, 'Лист 1', index=False)

        # Сохраните результат
        writer.close()

        showinfo(title="Успешно", message=f"Данные экспортированы в {excel_file_path}")

class EditDepartmentWindow(tk.Toplevel):
    def __init__(self, parent, department_id, department_window):
        super().__init__(parent)
        self.title("Редактировать отдел")
        self.department_id = department_id  # Сохраняем значение department_id как атрибут экземпляра
        self.department_window = department_window  # Сохраняем ссылку на экземпляр DepartmentWindow

        # Получите данные отдела по его идентификатору
        cursor.execute("SELECT * FROM department WHERE department_id=?", (department_id,))
        self.department_data = cursor.fetchone()  # Сохраняем данные отдела

        # Создаем и размещаем подписи к полям
        tk.Label(self, text="Название отдела:").grid(row=0, column=0, padx=10, pady=5)
        tk.Label(self, text="Руководитель:").grid(row=1, column=0, padx=10, pady=5)
        tk.Label(self, text="Контактная информация:").grid(row=2, column=0, padx=10, pady=5)

        # Создаем и размещаем поля ввода, заполняя их текущими данными отдела
        self.department_name_entry = tk.Entry(self)
        self.department_name_entry.grid(row=0, column=1, padx=10, pady=5)
        self.department_name_entry.insert(0, self.department_data[1])

        self.head_entry = tk.Entry(self)
        self.head_entry.grid(row=1, column=1, padx=10, pady=5)
        self.head_entry.insert(0, self.department_data[2])

        self.contact_info_entry = tk.Entry(self)
        self.contact_info_entry.grid(row=2, column=1, padx=10, pady=5)
        self.contact_info_entry.insert(0, self.department_data[3])

        # Создаем кнопку для сохранения изменений
        save_button = tk.Button(self, text="Сохранить", command=self.save_department)
        save_button.grid(row=4, columnspan=2, padx=10, pady=10)

    def save_department(self):
        # Получите новые данные из полей ввода
        new_department_name = self.department_name_entry.get()
        new_head = self.head_entry.get()
        new_contact_info = self.contact_info_entry.get()

        # Обновите все поля данных отдела в базе данных
        cursor.execute("UPDATE department SET name=?, head=?, contact_info=? WHERE department_id=?",
                       (new_department_name, new_head, new_contact_info, self.department_id))
        conn.commit()

        # Закройте окно редактирования
        self.destroy()

        # Обновите таблицу отделов, вызвав метод из DepartmentWindow
        self.department_window.update_department_table()

# Окно для работы с таблицей "Вакансия"
class VacancyWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Таблица 'Вакансии'")
        self.geometry("900x350")

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

        # Создаем фрейм для размещения кнопок в ряд
        button_frame = tk.Frame(self)
        button_frame.pack()

        # Кнопка для добавления вакансии
        self.add_vacancy_button = tk.Button(button_frame, text="Добавить вакансию", command=self.add_vacancy)
        self.add_vacancy_button.pack(side=tk.LEFT, padx=10, pady=5)

        # Кнопка для удаления вакансии
        self.delete_vacancy_button = tk.Button(button_frame, text="Удалить вакансию", command=self.delete_vacancy)
        self.delete_vacancy_button.pack(side=tk.LEFT, padx=10, pady=5)

        # Кнопка для редактирования вакансии
        self.edit_vacancy_button = tk.Button(button_frame, text="Редактировать вакансию", command=self.edit_vacancy)
        self.edit_vacancy_button.pack(side=tk.LEFT, padx=10, pady=5)

        # Создаем поле ввода для поиска вакансии
        self.search_entry = tk.Entry(self)
        self.search_entry.pack()

        # Кнопка для поиска вакансии
        search_vacancy_button = tk.Button(self, text="Найти вакансию", command=self.search_vacancy)
        search_vacancy_button.pack()

        # Кнопка для экспорта данных в Excel
        export_button = tk.Button(self, text="Экспорт в Excel", command=self.export_to_excel)
        export_button.pack()

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

        # Вставьте данные в таблицу "Вакансии" в базе данных
        cursor.execute("INSERT INTO vacancy (name, requirements, working_conditions) VALUES (?, ?, ?)",
                    (name, requirements, working_conditions))
        conn.commit()  # Сохраните изменения в базе данных
        self.update_vacancy_table()  # Обновите таблицу вакансий
        if self.add_vacancy_dialog:
            self.add_vacancy_dialog.destroy()

    def delete_vacancy(self):
        try:
            vacancy_id = self.tree.item(self.tree.selection())['values'][0]
            cursor.execute("DELETE FROM vacancy WHERE vacancy_id=?", (vacancy_id,))
            conn.commit()
            self.update_vacancy_table()
        except IndexError:
            showinfo(title="Внимание!", message="Выберите запись для удаления")

    # Функция для редактирования данных вакансии
    def edit_vacancy(self):
        selected_item = self.tree.selection()
        if selected_item:
            # Получите данные выбранной записи
            vacancy_id = self.tree.item(selected_item)['values'][0]
            # Откройте окно для редактирования с передачей идентификатора вакансии и ссылки на VacancyWindow
            EditVacancyWindow(self, vacancy_id, self)
        else:
            showinfo(title="Внимание!", message="Выберите запись для редактирования")

    # Функция для поиска вакансий
    def display_search_results(self, data):
        # Очистите виджет Treeview
        self.tree.delete(*self.tree.get_children())

        # Вставьте найденные записи в виджет Treeview
        for row in data:
            self.tree.insert("", "end", values=row)

    def search_vacancy(self):
        search_query = '%' + self.search_entry.get() + '%'
        cursor.execute("SELECT * FROM vacancy WHERE name LIKE ? OR requirements LIKE ? OR working_conditions LIKE ?",
                       (search_query, search_query, search_query))
        data = cursor.fetchall()

        # Вызовите функцию для отображения результатов поиска
        self.display_search_results(data)

    def export_to_excel(self):
        # Получите данные из базы данных
        cursor.execute("SELECT * FROM vacancy")
        data = cursor.fetchall()

        # Создайте DataFrame из данных
        df = pd.DataFrame(data, columns=["ID", "Name", "Requirements", "Working Conditions"])

        # Укажите путь к файлу Excel
        excel_file_path = "vacancies.xlsx"

        # Создайте объект writer для записи данных в Excel
        writer = pd.ExcelWriter(excel_file_path, engine='xlsxwriter')

        # Запишите DataFrame в файл Excel
        df.to_excel(writer, 'Лист 1', index=False)

        # Сохраните результат
        writer.close()

        showinfo(title="Успешно", message=f"Данные экспортированы в {excel_file_path}")
            
class EditVacancyWindow(tk.Toplevel):
    def __init__(self, parent, vacancy_id, vacancy_window):
        super().__init__(parent)
        self.title("Редактировать вакансию")
        self.vacancy_id = vacancy_id  # Сохраняем значение vacancy_id как атрибут экземпляра
        self.vacancy_window = vacancy_window  # Сохраняем ссылку на экземпляр VacancyWindow

        # Получите данные вакансии по её идентификатору
        cursor.execute("SELECT * FROM vacancy WHERE vacancy_id=?", (vacancy_id,))
        self.vacancy_data = cursor.fetchone()  # Сохраняем данные вакансии

        # Создаем и размещаем подписи к полям
        tk.Label(self, text="Название:").grid(row=0, column=0, padx=10, pady=5)
        tk.Label(self, text="Требования:").grid(row=1, column=0, padx=10, pady=5)
        tk.Label(self, text="Условия работы:").grid(row=2, column=0, padx=10, pady=5)

        # Создаем и размещаем поля ввода, заполняя их текущими данными вакансии
        self.title_entry = tk.Entry(self)
        self.title_entry.grid(row=0, column=1, padx=10, pady=5)
        self.title_entry.insert(0, self.vacancy_data[1])

        self.requirements_entry = tk.Entry(self)
        self.requirements_entry.grid(row=1, column=1, padx=10, pady=5)
        self.requirements_entry.insert(0, self.vacancy_data[2])

        self.working_conditions_entry = tk.Entry(self)
        self.working_conditions_entry.grid(row=2, column=1, padx=10, pady=5)
        self.working_conditions_entry.insert(0, self.vacancy_data[3])

        # Создаем кнопку для сохранения изменений
        save_button = tk.Button(self, text="Сохранить", command=self.save_vacancy)
        save_button.grid(row=3, columnspan=2, padx=10, pady=10)

    def save_vacancy(self):
        # Получите новые данные из полей ввода
        new_title = self.title_entry.get()
        new_requirements = self.requirements_entry.get()
        new_working_conditions = self.working_conditions_entry.get()

        # Обновите все поля данных вакансии в базе данных
        cursor.execute("UPDATE vacancy SET name=?, requirements=?, working_conditions=? WHERE vacancy_id=?",
                       (new_title, new_requirements, new_working_conditions, self.vacancy_id))
        conn.commit()

        # Закройте окно редактирования
        self.destroy()

        # Обновите таблицу вакансий, вызвав метод из VacancyWindow
        self.vacancy_window.update_vacancy_table()

# Окно для работы с таблицей "Заявка на вакансию"
class ApplicationWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Таблица 'Заявки на вакансии'")
        self.geometry("400x350")

        # Создаем виджет Treeview для отображения данных таблицы "Заявки на вакансии"
        self.tree = ttk.Treeview(self, columns=("ID", "Application Date", "Status"))

        self.tree.heading("#0", text="")
        self.tree.heading("#1", text="ID")
        self.tree.heading("#2", text="Application Date")
        self.tree.heading("#3", text="Status")

        self.tree.column("#0", width=0)
        self.tree.column("#1", width=40)
        self.tree.column("#2", width=150)
        self.tree.column("#3", width=150)

        self.tree.pack()

        # Создаем фрейм для размещения кнопок в ряд
        button_frame = tk.Frame(self)
        button_frame.pack()

        # Кнопка для добавления заявки
        self.add_application_button = tk.Button(button_frame, text="Добавить заявку", command=self.add_application)
        self.add_application_button.pack(side=tk.LEFT, padx=10, pady=5)

        # Кнопка для удаления заявки
        self.delete_application_button = tk.Button(button_frame, text="Удалить заявку", command=self.delete_application)
        self.delete_application_button.pack(side=tk.LEFT, padx=10, pady=5)

        # Кнопка для редактирования заявки
        self.edit_application_button = tk.Button(button_frame, text="Редактировать заявку", command=self.edit_application)
        self.edit_application_button.pack(side=tk.LEFT, padx=10, pady=5)

        # Создаем поле ввода для поиска заявки
        self.search_entry = tk.Entry(self)
        self.search_entry.pack()

        # Кнопка для поиска заявки
        search_application_button = tk.Button(self, text="Найти заявку", command=self.search_application)
        search_application_button.pack()

        # Кнопка для экспорта данных в Excel
        export_button = tk.Button(self, text="Экспорт в Excel", command=self.export_to_excel)
        export_button.pack()

        # Обновляем таблицу "Заявки на вакансии" при открытии окна
        self.update_application_table()

    def update_application_table(self):
        self.tree.delete(*self.tree.get_children())
        cursor.execute("SELECT application_id, application_date, status FROM application")
        data = cursor.fetchall()
        for row in data:
            self.tree.insert("", "end", values=row)

    def add_application(self):
        # Создаем окно для ввода данных заявки
        self.add_application_dialog = tk.Toplevel(self)
        self.add_application_dialog.title("Добавить заявку")

        # Создаем и размещаем подписи к полям
        tk.Label(self.add_application_dialog, text="Дата заявки:").grid(row=0, column=0, padx=10, pady=5)
        tk.Label(self.add_application_dialog, text="Статус:").grid(row=1, column=0, padx=10, pady=5)

        # Создаем и размещаем поля ввода
        self.application_date_entry = tk.Entry(self.add_application_dialog)
        self.application_date_entry.grid(row=0, column=1, padx=10, pady=5)
        self.status_entry = tk.Entry(self.add_application_dialog)
        self.status_entry.grid(row=1, column=1, padx=10, pady=5)

        # Создаем кнопку для добавления заявки
        add_button = tk.Button(self.add_application_dialog, text="Добавить", command=self.insert_application)
        add_button.grid(row=2, columnspan=2, padx=10, pady=10)

    def insert_application(self):
        # Получите данные из полей ввода
        application_date = self.application_date_entry.get()
        status = self.status_entry.get()

        # Вставьте данные в таблицу "Заявки на вакансии" в базе данных
        cursor.execute("INSERT INTO application (application_date, status) VALUES (?, ?)",
                    (application_date, status))
        conn.commit()  # Сохраните изменения в базе данных
        self.update_application_table()  # Обновите таблицу заявок
        if self.add_application_dialog:
            self.add_application_dialog.destroy()

    def delete_application(self):
        try:
            application_id = self.tree.item(self.tree.selection())['values'][0]
            cursor.execute("DELETE FROM application WHERE application_id=?", (application_id,))
            conn.commit()
            self.update_application_table()
        except IndexError:
            showinfo(title="Внимание!", message="Выберите запись для удаления")

    def edit_application(self):
        selected_item = self.tree.selection()
        if selected_item:
            application_id = self.tree.item(selected_item)['values'][0]
            EditApplicationWindow(self, application_id, self)
        else:
            showinfo(title="Внимание!", message="Выберите запись для редактирования")

    def display_search_results(self, data):
        self.tree.delete(*self.tree.get_children())
        for row in data:
            self.tree.insert("", "end", values=row)

    def search_application(self):
        search_query = '%' + self.search_entry.get() + '%'
        cursor.execute("SELECT application_id, application_date, status FROM application WHERE application_date LIKE ? OR status LIKE ?",
                       (search_query, search_query))
        data = cursor.fetchall()
        self.display_search_results(data)

    def export_to_excel(self):
        # Получите данные из базы данных
        cursor.execute("SELECT * FROM application")
        data = cursor.fetchall()

        # Создайте DataFrame из данных
        df = pd.DataFrame(data, columns=["ID", "Application Date", "Status", ""])

        # Укажите путь к файлу Excel
        excel_file_path = "applications.xlsx"

        # Создайте объект writer для записи данных в Excel
        writer = pd.ExcelWriter(excel_file_path, engine='xlsxwriter')

        # Запишите DataFrame в файл Excel
        df.to_excel(writer, 'Лист 1', index=False)

        # Сохраните результат
        writer.close()

        showinfo(title="Успешно", message=f"Данные экспортированы в {excel_file_path}")

class EditApplicationWindow(tk.Toplevel):
    def __init__(self, parent, application_id, application_window):
        super().__init__(parent)
        self.title("Редактировать заявку")
        self.application_id = application_id
        self.application_window = application_window

        cursor.execute("SELECT application_date, status FROM application WHERE application_id=?", (application_id,))
        self.application_data = cursor.fetchone()

        tk.Label(self, text="Дата заявки:").grid(row=0, column=0, padx=10, pady=5)
        tk.Label(self, text="Статус:").grid(row=1, column=0, padx=10, pady=5)

        self.application_date_entry = tk.Entry(self)
        self.application_date_entry.grid(row=0, column=1, padx=10, pady=5)
        self.application_date_entry.insert(0, self.application_data[0])

        self.status_entry = tk.Entry(self)
        self.status_entry.grid(row=1, column=1, padx=10, pady=5)
        self.status_entry.insert(0, self.application_data[1])

        save_button = tk.Button(self, text="Сохранить", command=self.save_application)
        save_button.grid(row=2, columnspan=2, padx=10, pady=10)

    def save_application(self):
        new_application_date = self.application_date_entry.get()
        new_status = self.status_entry.get()

        cursor.execute("UPDATE application SET application_date=?, status=? WHERE application_id=?",
                       (new_application_date, new_status, self.application_id))
        conn.commit()

        self.destroy()
        self.application_window.update_application_table()

# Справочники
class GenderWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Справочник 'Пол'")
        self.geometry("200x250")

        # Создаем виджет Treeview для отображения данных справочника
        self.tree = ttk.Treeview(self, columns=("ID", "Name"))

        self.tree.heading("#0", text="")
        self.tree.heading("#1", text="ID")
        self.tree.heading("#2", text="Наименование")

        self.tree.column("#0", width=0)
        self.tree.column("#1", width=40)
        self.tree.column("#2", width=150)

        self.tree.pack()

        # Обновляем справочник "Пол" при открытии окна
        self.update_gender_table()

    def update_gender_table(self):
        self.tree.delete(*self.tree.get_children())
        cursor.execute("SELECT * FROM gender")
        data = cursor.fetchall()
        for row in data:
            self.tree.insert("", "end", values=row)

class EducationWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Справочник 'Образование'")
        self.geometry("200x250")

        # Создаем виджет Treeview для отображения данных справочника "Образование"
        self.tree = ttk.Treeview(self, columns=("ID", "Name"))

        self.tree.heading("#0", text="")
        self.tree.heading("#1", text="ID")
        self.tree.heading("#2", text="Наименование")

        self.tree.column("#0", width=0)
        self.tree.column("#1", width=40)
        self.tree.column("#2", width=150)

        self.tree.pack()
 
        # Обновляем справочник "Образование" при открытии окна
        self.update_education_table()

    def update_education_table(self):
        self.tree.delete(*self.tree.get_children())
        cursor.execute("SELECT * FROM education")
        data = cursor.fetchall()
        for row in data:
            self.tree.insert("", "end", values=row)

class PositionWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Справочник 'Должности'")
        self.geometry("200x250")

        # Создаем виджет Treeview для отображения данных справочника "Должности"
        self.tree = ttk.Treeview(self, columns=("ID", "Name"))

        self.tree.heading("#0", text="")
        self.tree.heading("#1", text="ID")
        self.tree.heading("#2", text="Наименование")

        self.tree.column("#0", width=0)
        self.tree.column("#1", width=40)
        self.tree.column("#2", width=150)

        self.tree.pack()

        # Обновляем справочник "Должности" при открытии окна
        self.update_positions_table()

    def update_positions_table(self):
        self.tree.delete(*self.tree.get_children())
        cursor.execute("SELECT * FROM positions")
        data = cursor.fetchall()
        for row in data:
            self.tree.insert("", "end", values=row)

class ProfessionWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Справочник 'Профессии'")
        self.geometry("250x250")

        # Создаем виджет Treeview для отображения данных справочника "Профессии"
        self.tree = ttk.Treeview(self, columns=("ID", "Name"))

        self.tree.heading("#0", text="")
        self.tree.heading("#1", text="ID")
        self.tree.heading("#2", text="Наименование")

        self.tree.column("#0", width=0)
        self.tree.column("#1", width=40)
        self.tree.column("#2", width=200)

        self.tree.pack()

        # Обновляем справочник "Профессии" при открытии окна
        self.update_professions_table()

    def update_professions_table(self):
        self.tree.delete(*self.tree.get_children())
        cursor.execute("SELECT * FROM professions")
        data = cursor.fetchall()
        for row in data:
            self.tree.insert("", "end", values=row)

# Главное окно приложения
app = MainApp()
app.mainloop()
