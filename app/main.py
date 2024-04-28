# author Глінський Артем Валерійович

from extras import *
from handlers import *

@error_handler
def main():
    interface = ConsoleInterface()
    address_book = load_data()
    pretty_print("Welcome to the assistant bot!")
    try:
        while True:
            user_input = input("Enter a command: ")
            if not user_input:  # Якщо введення порожнє, запросимо команду знову
                continue
            command, args = parse_input(user_input)
            if command in ["close", "exit"]:
                pretty_print("Good bye!")
                break

            elif command == "hello":
                pretty_print("How can I help you?")

            elif command == "add":
                if len(args) != 2:
                    pretty_print("Invalid command. Usage: add [contact_name] [phone]", "yellow")
                else:
                    name, phone = args[0], args[1]
                    try:
                        # Перевіряємо, чи існує контакт з таким іменем
                        if name not in address_book.data:
                            # Якщо контакт не існує, створюємо новий запис
                            record = Record(name)
                            address_book.add_record(record)
                        # Додаємо номер телефону до існуючого або нового контакту
                        pretty_print(address_book.data[name].add_phone(phone))
                    except ValueError as e:
                        pretty_print(str(e), "yellow")

            elif command == "delete":
                if len(args) != 1:
                    pretty_print("Invalid command. Usage: delete [contact_name]", "yellow")
                else:
                    name = args[0]
                    pretty_print(address_book.delete(name))

            elif command == "change":
                if len(args) != 3:
                    pretty_print("Invalid command. Usage: change [contact_name] [old_phone] [new_phone]" , "yellow")
                else:
                    try:
                        name, old_phone, new_phone = args[0], args[1], args[2]
                        #  Перевіряємо чи існує такий запис у телефонній книзі
                        if name in address_book.data:
                        # Викликаємо метод edit_phone для зміни номера телефону
                            pretty_print(address_book.data[name].edit_phone(old_phone, new_phone))
                        else:
                            pretty_print(f"Record <{name}> was not found in the address book." , "yellow")
                    except ValueError as e:
                        pretty_print(str(e), "yellow")

            elif command == "phone":
                if len(args) != 1:
                    pretty_print("Invalid command. Usage: phone [contact_name]", "yellow")
                else:
                    name = args[0]
                    if name in address_book.data:
                        pretty_print(f"Phone number(s) for {name}: {', '.join(str(p) for p in address_book.data[name].phones)}")
                    else:
                        pretty_print(f"Record <{name}> was not found in the address book." , "yellow")

            elif command == "all":
                pretty_print("All contacts:")
                # for record in address_book.data.values():
                #     pretty_print(str(record))
                interface.display_contacts(address_book.data.values())

            elif command == "add-birthday":
                if len(args) != 2:
                    pretty_print("Invalid command. Usage: add-birthday [contact_name] [birthday]", "yellow")
                else:
                    name, birthday = args[0], args[1]
                    try:
                        if name in address_book.data:
                            pretty_print(address_book.data[name].add_birthday(birthday))
                        else:
                            pretty_print(f"Record <{name}> not found in AddressBook", "yellow")
                    except ValueError as e:
                        pretty_print(str(e), "yellow")


            elif command == "show-birthday":
                if len(args) != 1:
                    pretty_print("Invalid command. Usage: show-birthday [contact_name]", "yellow")
                else:
                    name = args[0]
                    if name in address_book.data:
                        if address_book.data[name].birthday:
                            pretty_print(f"Birthday for {name}: {address_book.data[name].birthday.value}")
                        else:
                            pretty_print(f"Birthday for {name} not defined")
                    else:
                        pretty_print(f"Record <{name}> not found in AddressBook", "yellow")

            elif command == "birthdays":
                try:
                    upcoming_birthdays = address_book.get_upcoming_birthdays()
                    pretty_print("Upcoming birthdays:")
                    for birthday_info in upcoming_birthdays:
                        pretty_print(f"{birthday_info['name']}'s birthday is on {birthday_info['congratulation_date']}")
                except Exception as e:
                        pretty_print(str(e), "yellow")
            elif command == "help":
                commands_info = {
                    "close/exit": "Close the program.",
                    "hello": "Greet the user.",
                    "add": "Add a new contact.",
                    "change": "Change a contact's phone number.",
                    "phone": "Show a contact's phone number.",
                    "all": "Show all contacts.",
                    "add-birthday": "Add birthday to a contact.",
                    "show-birthday": "Show birthday of a contact.",
                    "birthdays": "Show upcoming birthdays.",
                    "help": "Display available commands info.",
                }
                interface.display_commands_info(commands_info)
            else:
                pretty_print("Invalid command", "yellow")
    finally:
        save_data(address_book)


if __name__ == "__main__":
    main()
