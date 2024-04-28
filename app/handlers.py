# author Глінський Артем Валерійович
from collections import UserDict
from datetime import datetime, timedelta
from abc import ABC, abstractmethod
import pickle
from extras import *

#абстрактний базовий клас для користувальницьких уявлень та конкретні реалізації для консольного інтерфейсу
class UserInterface(ABC):
    @abstractmethod
    def display_contacts(self, contacts):
        pass

    @abstractmethod
    def display_commands_info(self, commands_info):
        pass

class ConsoleInterface(UserInterface):
    def display_contacts(self, contacts):
        for contact in contacts:
            pretty_print(str(contact),delay=0.02)

    def display_commands_info(self, commands_info):
        for command, info in commands_info.items():
            pretty_print(f"{command}: {info}", 'yellow', 0.02)

# Field: Базовий клас для полів запису.
class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

# Name: Клас для зберігання імені контакту. Обов'язкове поле.
class Name(Field):
    def __init__(self, value):
        super().__init__(value)

# Phone: Клас для зберігання номера телефону. Має валідацію формату (10 цифр).
class Phone(Field):
    def __init__(self, value):
        super().__init__(value)

# Клас для зберігання дня народження
class Birthday(Field):
    def __init__(self, value):
        try:
            datetime.strptime(value, "%Y.%m.%d")
        except ValueError:
            raise ValueError("Incorrect date format for birthday. Correct format: %Y.%m.%d")
        super().__init__(value)

# Record: Клас для зберігання інформації про контакт, включаючи ім'я та список телефонів.
class Record:
    def __init__(self, name, birthday=None):
        if len(name) < 1:
            raise ValueError("Name must not be not empty")
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        if birthday:
            self.add_birthday(birthday)

    # Додавання телефонів.
    def add_phone(self, phone):
        if len(phone) != 10 or not phone.isdigit():
            raise ValueError("Phone number must be 10 digits.\nThe contact will be saved without a new phone number. You can add the number later. ")
        else:
            self.phones.append(Phone(phone))
            return f"Phone {phone} was added to <{self.name.value}>."


    # Видалення телефонів.
    def delete_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                return(f"Record {p.value} was deleted from {self.name.value}.")
        return("Phone number not found")

    # Редагування телефонів.
    def edit_phone(self, old_phone, new_phone):
        for p in self.phones:
            if p.value == old_phone:
                if len(new_phone) != 10 or not new_phone.isdigit():
                    raise ValueError("Phone number must be 10 digits.\nThe phone number was not changed")
                p.value = new_phone
                return (f"<{self.name.value}> phone number {old_phone} was changed to {new_phone}")
        raise ValueError (f"Phone number <{old_phone}> not found")

    # Пошук телефону.
    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        print("Phone number not found")
        return None

    # Додавання дня народження.
    def add_birthday(self, birthday):
        if not isinstance(birthday, Birthday):
            birthday = Birthday(birthday)
        self.birthday = birthday
        return(f"Birthday {birthday} was added to {self.name.value}.")

    def __str__(self):
        if self.birthday:
            return f"Contact name: {self.name.value}, phones: {', '.join(str(p) for p in self.phones)}, birthday: {self.birthday.value}"
        else:
            return f"Contact name: {self.name.value}, phones: {', '.join(str(p) for p in self.phones)}, birthday: None"

# AddressBook: Клас для зберігання та управління записами.
class AddressBook(UserDict):
    # Додавання телефонів.
    def add_record(self, record):
        self.data[record.name.value] = record
        return(f"Record {record.name.value} was added to AddressBook")

    # Видалення записів за іменем.
    def delete(self, name):
        if name in self.data:
            confirmation = input(f"Are you sure you want to delete record <{name}>? (yes/no): ").lower()
            if confirmation == "yes":
                del self.data[name]
                return f"Record <{name}> was deleted"
            else:
                return "Deletion canceled"
        else:
            return f"Record <{name}> not found in AddressBook"


    # Пошук записів за іменем.
    def find(self, name):
        if name in self.data:
            return self.data[name]
        else:
            return f"Record <{name}> not found in AddressBook"

    # Функція для отримання списку користувачів, яких потрібно привітати по днях на наступному тижні
    def get_upcoming_birthdays(self):
        try:
            today = datetime.today().date()
            next_week = today + timedelta(days=7)
            upcoming_birthdays = []

            for record in self.data.values():
                if record.birthday:
                    birthday_this_year = datetime.strptime(record.birthday.value, "%Y.%m.%d").date().replace(year=today.year)
                    # процесiм тих у кого день народження буде в найближчи 7 днiв
                    if today <= birthday_this_year < next_week:
                        # Якщо день народження буде у вихiдний - переносимо дату вiттання на найближчий понедiлок
                        if birthday_this_year.weekday() >= 5:
                            while birthday_this_year.weekday() != 0:
                                birthday_this_year += timedelta(days=1)
                        upcoming_birthdays.append({
                            "name": record.name.value,
                            "congratulation_date": birthday_this_year.strftime("%Y.%m.%d")
                        })

            return upcoming_birthdays
        except Exception as error:
            print(f"Error: ", error)
            return []

# Функція для збереження адресноi книги
def save_data(book, filename="addressbook.pkl"):
    try:
        with open(filename, "wb") as f:
            pickle.dump(book, f)
        pretty_print("Address book successfully saved.", 'yellow')
    except Exception as error:
        print(f"Error: ", error)

# Функція завантаження адресноi книги
def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()  # Повернення нової адресної книги, якщо файл не знайдено
    except pickle.UnpicklingError:
        print("File is corrupted. Unable to unpickle the data.")
        return None  # Повернення None в разі пошкодження файлу
