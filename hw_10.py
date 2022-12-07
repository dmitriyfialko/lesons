from collections import UserDict


class AddressBook(UserDict):
    """Хранит значения как в словаре"""

    def add_record(self, record):
        """Сохраняет записи в AddressBook"""
        self.data[record.name.value] = record.phone_list

    def record_search(self, name):
        """Поиск контактов по имени"""
        nm = self.data.get(name)
        return f'{name} {", ".join(nm)}' if nm else 'Такого имени нет в AddressBook'

    def show_all(self, *args, **kwargs):
        """Возвращает все сохранённе контакты в виде текста"""
        text = ''
        for name, phones in self.data.items():
            text += f'{name} {", ".join(phones)}\n'
        return text if text else 'В AddressBook нет записей'

    def del_user(self, name):
        self.data.pop(name.title())
        return f'Пользователь {name}, удалён из AddressBook'


class Field:
    pass


class Name(Field):
    def __init__(self, value):
        self.value = value


class Phone(Field):
    def __init__(self, value):
        self.value = value


class Record:
    """отвечает за логику добавления/удаления/редактирования необязательных полей
    и хранения обязательного поля Name."""
    def __init__(self, name, address_book):
        self.name = Name(name.title())
        self.phone_list = address_book.get(name.title(), [])

    def add_phone(self, phone):
        self.phone_list.append(Phone(phone).value)
        return f'Phone number for user "{self.name.value}" added'

    def del_phone(self, phone):
        try:
            self.phone_list.remove(phone)
            return f'Phone number for user "{self.name.value}" deleted'
        except ValueError:
            return f'Такого номера нет у {self.name.value}'

    def edit_phone(self, phone, new_phone):
        try:
            self.phone_list.remove(phone)
            self.add_phone(new_phone)
            return f'number {phone} of user {self.name.value} changed to {new_phone}'
        except ValueError:
            return f'Такого номера нет у {self.name.value}'


EXIT_FLAG = False
ADDRESS_BOOK = AddressBook()


def input_error(func):
    """Обработчик ошибок ввода"""
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except TypeError:
            return 'Give me name and phone please'
        except ValueError:
            return 'Phone number is incorrect. It should only be numbers.'
        except KeyError:
            return 'Could not find or create a user with this name'
        except IndexError:
            return 'Incorrect number of command arguments'
    return inner


@input_error
def add_command_handler(command_lst: list) -> str:
    """Обработчик добавления нового контакта или изменения и удаления существующего"""
    if len(command_lst) != 3 and command_lst[0] in ['add', 'del phone']:
        raise TypeError
    if not command_lst[2].isdigit():
        return 'Phone number is incorrect. It should only be numbers.'
    record = Record(command_lst[1], ADDRESS_BOOK)
    if command_lst[0] == 'add':
        text = record.add_phone(command_lst[2])
    elif command_lst[0] == 'del phone':
        text = record.del_phone(command_lst[2])
    else:
        text = record.edit_phone(command_lst[2], command_lst[3])
    ADDRESS_BOOK.add_record(record)
    return text


@input_error
def del_user(command_lst: list):
    """Функция удаляет пользователя вместе с контактами"""
    return ADDRESS_BOOK.del_user(command_lst[1])


@input_error
def phone_command_handler(command_lst: list) -> str:
    """Обработчик команды phone"""
    if len(command_lst) != 2:
        return 'Give me name please'
    return ADDRESS_BOOK.record_search(command_lst[1])


def exit_function(*args, **kwargs) -> str:
    """"Функция меняет EXIT_FLAG на True для выхода из цикла программы"""
    global EXIT_FLAG
    EXIT_FLAG = True
    return 'Good bye!'


def hello(*args, **kwargs):
    return 'How can I help you?'


COMMAND_DICT = {
    'add': add_command_handler,
    'change': add_command_handler,
    'phone': phone_command_handler,
    'show all': ADDRESS_BOOK.show_all,
    'good bye': exit_function,
    'close': exit_function,
    'exit': exit_function,
    'hello': hello,
    'del phone': add_command_handler,
    'del user': del_user
}


def command_parser(command: str) -> list:
    """Функция проверяет существует ли команда в словаре команд, отделяет команду от данных,
    и возвращает результат соответствующей функции если команда распознана, иначе None"""
    command = command.lower()
    for com in list(COMMAND_DICT.keys()):
        com_str = com if len(com) == len(command) else f'{com} '
        if command.find(com_str) == 0:
            data = command[len(com)+1:]
            command_lst = [com] + data.split()
            return COMMAND_DICT[com](command_lst)


def main():
    """Бот помощник"""
    while True:
        command_str = input()
        if not command_str:
            continue
        result = command_parser(command_str)
        if result:
            print(result)
            if EXIT_FLAG:
                break
        else:
            print("Command not recognized. Use the command from the list\n"
                  "'hello', 'show all', 'add', 'change', 'phone', 'del user', 'del phone', 'close', 'exit', 'good bye'")


if __name__ == '__main__':
    main()

