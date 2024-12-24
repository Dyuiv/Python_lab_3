import json
import os
from datetime import datetime
FILE_NAME = "phone_directory.json"
def load_directory():
    if (os.path.exists(FILE_NAME)):
        with open(FILE_NAME, "r", encoding="utf-8") as file:
            return json.load(file)
    return {}

def save_directory(directory):
    with open("phone_directory.json", "w", encoding="utf-8") as file:
        json.dump(directory, file,indent=4, ensure_ascii=False)

def format_name(name):
    name = name.strip().title()
    if (not all(c.isalnum() or c.isspace() for c in name)):
        raise ValueError("Имя и фамилия могут содержать только латинские буквы, цифры и пробелы.")
    return name

def is_valid_phone(phone):
    if (phone.startswith("+7")):
        phone = "8" + phone[2:]
    return phone.isdigit() and len(phone) == 11

def is_valid_date(date_str):
    try:
        datetime.strptime(date_str, "%d.%m.%Y")
        return True
    except ValueError:
        return False

def display_records(directory):
    if(not directory):
        print("\nСправочник пуст.\n")
        return
    print("\nТекущие записи в справочнике:")
    for key, data in directory.items():
        print(f"{data['Имя']} {data['Фамилия']} | Телефон: {data['Телефон']} | Дата рождения: {data.get('Дата рождения', 'Не указана')}")
    print()

def add_record(directory):
    try:
        first_name = format_name(input("Введите имя: "))
        last_name = format_name(input("Введите фамилию: "))
    except ValueError as e:
        print(f"\nОшибка: {e}\n")
        return

    identifier = f"{first_name}_{last_name}"
    if (identifier in directory):
        print("\nЗапись с таким именем уже существует.\n")
        return

    phone = input("Введите номер телефона (11 цифр): ").strip()
    if (not is_valid_phone(phone)):
        print("\nНеверный формат номера телефона.\n")
        return

    birth_date = input("Введите дату рождения (дд.мм.гггг) или оставьте пустым: ").strip()
    if (birth_date and not is_valid_date(birth_date)):
        print("\nНеверный формат даты рождения.\n")
        return

    directory[identifier] = {
        "Имя": first_name,
        "Фамилия": last_name,
        "Телефон": phone,
        "Дата рождения": birth_date if birth_date else None
    }
    print("\nЗапись успешно добавлена.\n")
    save_directory(directory)

def delete_record(directory):

    first_name = format_name(input("Введите имя для удаления: "))
    last_name = format_name(input("Введите фамилию для удаления: "))
    identifier = f"{first_name}_{last_name}"
    if (identifier in directory):
        del directory[identifier]
        print("\nЗапись успешно удалена.\n")
        save_directory(directory)
    else:
        print("\nЗапись не найдена.\n")

def search_record(directory):
    search_field = input("Введите имя, фамилию или номер для поиска: ").strip()
    found = [data for key, data in directory.items() if search_field in key or search_field in data.values()]

    if found:
        print("\nНайденные записи:")
        for record in found:
            print(f"{record['Имя']} {record['Фамилия']} | Телефон: {record['Телефон']} | Дата рождения: {record.get('Дата рождения', 'Не указана')}")
    else:
        print("\nСовпадений не найдено.\n")

def update_record(directory):
    first_name = format_name(input("Введите имя для изменения: "))
    last_name = format_name(input("Введите фамилию для изменения: "))
    identifier = f"{first_name}_{last_name}"
    if(identifier not in directory):
        print("\nЗапись не найдена.\n")
        return

    field = input("Что изменить? (Имя, Фамилия, Телефон, Дата рождения): ").strip().lower()

    if(field == "имя"):
        try:
            new_first_name = format_name(input("Введите новое имя: "))
            directory[identifier]["Имя"] = new_first_name
        except ValueError as e:
            print(f"\nОшибка: {e}\n")
            return
    elif(field == "фамилия"):
        try:
            new_last_name = format_name(input("Введите новую фамилию: "))
            directory[identifier]["Фамилия"] = new_last_name
        except ValueError as e:
            print(f"\nОшибка: {e}\n")
            return
    elif (field == "телефон"):
        new_phone = input("Введите новый номер телефона: ").strip()
        if not is_valid_phone(new_phone):
            print("\nНеверный формат номера телефона.\n")
            return
        directory[identifier]["Телефон"] = new_phone
    elif (field == "дата рождения"):
        new_birth_date = input("Введите новую дату рождения (дд.мм.гггг): ").strip()
        if (new_birth_date and not is_valid_date(new_birth_date)):
            print("\nНеверный формат даты рождения.\n")
            return
        directory[identifier]["Дата рождения"] = new_birth_date
    else:
        print("\nНекорректное поле.\n")
        return

    print("\nЗапись успешно обновлена.\n")
    save_directory(directory)

def calculate_age(birth_date):
    birth_date = datetime.strptime(birth_date, "%d.%m.%Y")
    today = datetime.today()

    return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

def get_age(directory):
    first_name = format_name(input("Введите имя: "))
    last_name = format_name(input("Введите фамилию: "))
    identifier = f"{first_name}_{last_name}"
    if(identifier in directory):
        birth_date = directory[identifier].get("Дата рождения")
        if birth_date:
            age = calculate_age(birth_date)
            print(f"\nВозраст: {age} лет\n")
        else:
            print("\nДата рождения не указана.\n")
    else:
        print("\nЗапись не найдена.\n")

directory = load_directory()
while True:
    print("\nВыберите команду:")
    print("1. Просмотр всех записей")
    print("2. Поиск записи")
    print("3. Добавление записи")
    print("4. Удаление записи")
    print("5. Изменение записи")
    print("6. Вывод возраста записи")
    print("7. Выход")
    command = input("Введите номер команды: ").strip()
    if(command == "1"):
        display_records(directory)
    elif (command == "2"):
        search_record(directory)
    elif (command == "3"):
        add_record(directory)
    elif(command == "4"):
        delete_record(directory)
    elif (command == "5"):
        update_record(directory)
    elif (command == "6"):
        get_age(directory)
    elif (command == "7"):
        print("\nЗавершение работы программы. \n")
        break
    else:
        print("\nНеверная команда. Попробуйте снова.\n")


