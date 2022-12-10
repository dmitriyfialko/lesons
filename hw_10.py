from collections import UserDict


class AddressBook(UserDict):
    """Хранит значения как в словаре"""

    def add_record(self, record):
        """Сохраняет записи в AddressBook"""
        self.data[record.name.value] = record

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
        if not value.isdigit():
            raise ValueError('Only numbers')
        self.value = value

    def __str__(self):
        return self.value


class Record:
    """отвечает за логику добавления/удаления/редактирования необязательных полей
    и хранения обязательного поля Name."""
    def __init__(self, name):
        self.name = Name(name.title())
        self.phone_list = []

    def search_in_phone_list(self, phone):
        """Функция возвращает индекс объекта в списке self.phone_list если Phone.value == phone иначе None"""
        for i, ph in enumerate(self.phone_list):
            if ph.value == phone:
                return i

    def add_phone(self, phone):
        """Добавляет Phone в phone_list"""
        if self.search_in_phone_list(phone) is None:
            self.phone_list.append(Phone(phone))
            return f'Phone number for user "{self.name.value}" added'
        return f'Number {phone} is already in the contact list'

    def del_phone(self, phone):
        """Удаляет Phone(phone) из phone_list если находит соответствующий Phone.value"""
        if (index_phone := self.search_in_phone_list(phone)) is not None:
            self.phone_list.pop(index_phone)
            return f'Phone number {phone} for user "{self.name.value}" deleted'
        return f"{self.name.value} doesn't have that number"

    def edit_phone(self, phone, new_phone):
        """Заменяет Phone(phone) на Phone(new_phone) если находит соответствующий Phone.value"""
        if (index_phone := self.search_in_phone_list(phone)) is not None:
            self.phone_list[index_phone] = Phone(new_phone)
            return f'number {phone} of user {self.name.value} changed to {new_phone}'
        return f"{self.name.value} doesn't have that number"


EXIT_FLAG = False
ADDRESS_BOOK = AddressBook()


def input_error(func):
    """Обработчик ошибок ввода"""
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return 'Phone number is incorrect. It should only be numbers.'
        except IndexError:
            return 'Give me name and phone please'
        except KeyError:
            return 'This user name is not in the Book'
    return inner


@input_error
def add_command_handler(command_lst: list) -> str:
    """Обработчик добавления нового контакта"""
    if not (record := ADDRESS_BOOK.get(command_lst[1].title())):
        record = Record(command_lst[1])
    text = record.add_phone(command_lst[2])
    ADDRESS_BOOK.add_record(record)
    return text


@input_error
def del_command_handler(command_lst: list) -> str:
    """Обработчик удаления существующего телефона"""
    record = ADDRESS_BOOK.get(command_lst[1].title())
    if record:
        text = record.del_phone(command_lst[2])
        ADDRESS_BOOK.add_record(record)
        return text
    else:
        return 'This user name is not in the Book'


def change_command_handler(command_lst: list) -> str:
    """Обработчик изменения существующего телефона"""
    try:
        record = ADDRESS_BOOK.get(command_lst[1].title())
        if record:
            text = record.edit_phone(command_lst[2], command_lst[3])
            ADDRESS_BOOK.add_record(record)
            return text
        else:
            return 'This user name is not in the Book'
    except IndexError:
        return 'name, phone number and new phone number are required'


@input_error
def del_user(command_lst: list):
    """Функция удаляет пользователя вместе со всеми контактами"""
    if len(command_lst) != 2:
        return 'Give me name please'
    return ADDRESS_BOOK.del_user(command_lst[1])


def phone_command_handler(command_lst: list) -> str:
    """Обработчик команды phone"""
    if len(command_lst) != 2:
        return 'Give me name please'
    if record := ADDRESS_BOOK.get(command_lst[1].title()):
        ls = []
        for phone in record.phone_list:
            ls.append(phone.value)
        return f'{record.name.value} -> {", ".join(ls)}\n'
    else:
        return 'This user name is not in the Book'


def show_all_phone(*args, **kwargs):
    """список всех телефонов из AddressBook"""
    text = ''
    for name, record in ADDRESS_BOOK.items():
        ls = []
        for phone in record.phone_list:
            ls.append(phone.value)
        text += f'{name} -> {", ".join(ls)}\n'
    return text or 'Address book is empty'


def exit_function(*args, **kwargs) -> str:
    """"Функция меняет EXIT_FLAG на True для выхода из цикла программы"""
    global EXIT_FLAG
    EXIT_FLAG = True
    return 'Good bye!'


def hello(*args, **kwargs):
    return 'How can I help you?'


COMMAND_DICT = {
    'add': add_command_handler,
    'change': change_command_handler,
    'del phone': del_command_handler,
    'del user': del_user,
    'phone': phone_command_handler,
    'show all': show_all_phone,
    'good bye': exit_function,
    'close': exit_function,
    'exit': exit_function,
    'hello': hello
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
