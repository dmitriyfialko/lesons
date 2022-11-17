PHONE_DICT = {}
EXIT_FLAG = False


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
        # except IndexError:
        #     return ''
    return inner


@input_error
def add_command_handler(command_lst: list) -> str:
    """Обработчик добавления нового контакта или изменения существующего"""
    global PHONE_DICT
    if len(command_lst) != 3:
        raise TypeError
    if not command_lst[2].isdigit():
        raise ValueError
    if command_lst[0] == 'add':
        if PHONE_DICT.get(command_lst[1]):
            raise KeyError
    else:
        if not PHONE_DICT.get(command_lst[1]):
            raise KeyError
    PHONE_DICT[command_lst[1]] = command_lst[2]
    return f'Phone number for user "{command_lst[1]}" added' if command_lst[0] == 'add'\
        else f'"{command_lst[1]}" user phone has changed'


@input_error
def phone_command_handler(command_lst: list) -> str:
    """Обработчик команды phone. Возвращает номер если находит имя"""
    if len(command_lst) != 2:
        return 'Give me name please'
    return PHONE_DICT[command_lst[1]]


def show_all(*args, **kwargs) -> str:
    """Возвращает все сохранённе контакты в виде текста"""
    text = ''
    for name, phone in PHONE_DICT.items():
        text += f'{name} {phone}\n'
    return text if text else 'No saved contacts'


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
    'show all': show_all,
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
                  "'hello', 'show all', 'add', 'change', 'phone', 'close', 'exit', 'good bye'")


if __name__ == '__main__':
    main()


