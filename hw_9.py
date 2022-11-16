import json


PHONE_DICT = {}


def input_error(func):
    """Обработчик ошибок ввода"""
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IndexError:
            return 'IndexError'
        except ValueError:
            return 'ValueError'
        except KeyError:
            return 'KeyError'
    return inner


def command_parser(command: str) -> list:
    """Функция возвращает список команда + данные если команда существует иначе None"""
    # команды в несколько слов
    if command.lower() in ['show all', 'good bye']:
        return [command.lower()]
    # команды в одно слово
    command_list = ['hello', 'add', 'change', 'phone', 'close', 'exit']
    if (command := command.lower().split()) and command[0] in command_list:
        return command


@input_error
def add_command_handler(command_lst: list) -> str:
    """Обработчик добавления нового контакта или изменения"""
    global PHONE_DICT
    if len(command_lst) != 3:
        raise IndexError
    if not command_lst[2].isdigit():
        raise ValueError
    if command_lst[0] == 'add':
        if PHONE_DICT.get(command_lst[1]):
            raise KeyError
    else:
        if not PHONE_DICT.get(command_lst[1]):
            raise KeyError
    PHONE_DICT[command_lst[1]] = command_lst[2]
    save_json()
    return 'ok'


@input_error
def phone_command_handler(command_lst: list) -> str:
    """Обработчик команды phone"""
    if len(command_lst) != 2:
        raise IndexError
    return PHONE_DICT[PHONE_DICT[command_lst[1]]]


def show_all() -> str:
    """Возвращает все сохранённе контакты в виде текста"""
    text = ''
    for name, phone in PHONE_DICT.items():
        text += f'{name} {phone}\n'
    return text if text else 'No saved contacts'


def save_json(mode_write=True):
    """Сохраняет изменения PHONE_DICT в файл phone_book.json"""
    global PHONE_DICT
    if mode_write:
        with open('phone_book.json', 'w') as file:
            file.write(json.dumps(PHONE_DICT))
    else:
        try:
            with open('phone_book.json', 'r') as file:
                PHONE_DICT = json.loads(file.read())
        except FileNotFoundError:
            with open('phone_book.json', 'w') as file:
                file.write("{}")


def main():
    """Бот помощник"""
    global PHONE_DICT
    # чтение сохранённых контактов из файла
    save_json(mode_write=False)

    while True:
        command_lst = input()
        if not command_lst:
            continue
        command_lst = command_parser(command_lst)
        if command_lst:
            # проверяем, нужно ли остановить бота
            if command_lst[0] in ['good bye', 'close', 'exit']:
                print('Good bye!')
                break

            # работа с командами
            elif command_lst[0] == 'hello':
                print('How can I help you?')

            elif command_lst[0] in ['add', 'change']:
                if (a := add_command_handler(command_lst)) == 'ok':
                    if command_lst[0] == 'add':
                        print(f'Phone number for user "{command_lst[1]}" added')
                    else:
                        print(f'"{command_lst[1]}" user phone has changed')
                elif a == 'IndexError':
                    print('Give me name and phone please')
                elif a == 'ValueError':
                    print('Phone number is incorrect. It should only be numbers.')
                elif a == 'KeyError':
                    if command_lst[0] == 'add':
                        print('This name already exists')
                    else:
                        print('This name was not found')

            elif command_lst[0] == 'phone':
                if (a := phone_command_handler(command_lst)) == 'IndexError':
                    print('Give me name please')
                elif a == 'KeyError':
                    print('This name was not found')
                else:
                    print(a)

            elif command_lst[0] == 'show all':
                print(show_all())
        else:
            print("Command not recognized. Use the command from the list\n"
                  "'hello', 'show all', 'add', 'change', 'phone', 'close', 'exit', 'good bye'")


if __name__ == '__main__':
    main()


