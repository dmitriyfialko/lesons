from pathlib import Path
from sys import argv
from zipfile import ZipFile
from shutil import move


START_PATH = None
EXTENSION_DICT = {'images': ['JPEG', 'PNG', 'JPG', 'SVG'],
                  'video': ['AVI', 'MP4', 'MOV', 'MKV'],
                  'documents': ['DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'],
                  'audio': ['MP3', 'OGG', 'WAV', 'AMR'],
                  'archives': ['ZIP', 'GZ', 'TAR']}


def chek_start():
    """Функция проверяет наличие аргумента и является ли он папкой
    Возвращает путь или None"""
    if len(argv) < 2:
        print('Directory not specified when running script')
        return None
    folder = Path(argv[1])
    if folder.is_dir():
        return argv[1]
    elif folder.is_file():
        print(f'specified path "{argv[1]}" is not folder')
    else:
        print(f'folder "{argv[1]}" not found')


def normalize(file_name: str) -> str:
    """Проводит транслитерацию кириллического алфавита на латинский.
    Заменяет все символы кроме латинских букв, цифр на '_'."""
    translation = {1072: 'a', 1040: 'A', 1073: 'b', 1041: 'B', 1074: 'v', 1042: 'V', 1075: 'g', 1043: 'G', 1076: 'd',
                   1044: 'D', 1077: 'e', 1045: 'E', 1105: 'e', 1025: 'E', 1078: 'j', 1046: 'J', 1079: 'z', 1047: 'Z',
                   1080: 'i', 1048: 'I', 1081: 'j', 1049: 'J', 1082: 'k', 1050: 'K', 1083: 'l', 1051: 'L', 1084: 'm',
                   1052: 'M', 1085: 'n', 1053: 'N', 1086: 'o', 1054: 'O', 1087: 'p', 1055: 'P', 1088: 'r', 1056: 'R',
                   1089: 's', 1057: 'S', 1090: 't', 1058: 'T', 1091: 'u', 1059: 'U', 1092: 'f', 1060: 'F', 1093: 'h',
                   1061: 'H', 1094: 'ts', 1062: 'TS', 1095: 'ch', 1063: 'CH', 1096: 'sh', 1064: 'SH', 1097: 'sch',
                   1065: 'SCH', 1098: '', 1066: '', 1099: 'y', 1067: 'Y', 1100: '', 1068: '', 1101: 'e', 1069: 'E',
                   1102: 'yu', 1070: 'YU', 1103: 'ya', 1071: 'YA', 1108: 'je', 1028: 'JE', 1110: 'i', 1030: 'I',
                   1111: 'ji', 1031: 'JI', 1169: 'g', 1168: 'G'}
    file = Path(file_name)
    suffix = file.suffix
    name = file_name.rstrip(suffix)
    new_name = ''
    for symbol in name:
        if s := translation.get(ord(symbol)):
            new_name += s
        elif 'a' <= symbol <= 'z' or 'A' <= symbol <= 'Z' or symbol.isdigit():
            new_name += symbol
        else:
            new_name += '_'
    return new_name + suffix


def is_file(path, file_type):
    """Перемещает и переименовует файлы"""
    path = Path(path)
    new_name = normalize(path.name)
    path.rename(Path(path.parent, new_name))
    path = Path(Path(path.parent, new_name))
    if file_type == 'archives':
        archive = ZipFile(path)
        n_path = Path(START_PATH, file_type, path.name.rstrip(path.suffix))
        # проверяем существует ли папка с таким именем
        nn = 1
        while True:
            if not n_path.is_dir():
                break
            else:
                nn += 1
                n_path = Path(START_PATH, file_type, f'{path.name.rstrip(path.suffix)}_{nn}')
        # распаковываем архив
        archive.extractall(n_path.absolute())
    else:
        n_path = Path(START_PATH, file_type, path.name)
        n = 1
        while True:     # меняем имя если файл с таким именем существует в папке
            if not n_path.is_file():
                move(path.absolute(), n_path.absolute())
                break
            else:
                n += 1
                n_path = Path(START_PATH, file_type, f'{path.name.rstrip(path.suffix)}_{n}{path.suffix}')


def is_folder(path):
    """Функция работает с содержимым папки
    запускается рекурсивно, если находит папку"""
    path = Path(path)
    for folder_item in path.iterdir():
        item = Path(folder_item)
        if item.is_dir():
            if item.name in EXTENSION_DICT.keys():
                continue
            # переименовуем папку
            new_name = normalize(item.name)
            if new_name != item.name:
                item.rename(Path(item.parent, new_name))
            # запускаем рекурсию
            is_folder(Path(item.parent, new_name))
        else:
            # получаем тип файла
            file_type = None
            for key, value in EXTENSION_DICT.items():
                if item.suffix.lstrip('.').upper() in value:
                    file_type = key
                    break
            # запускаем функцию для работы с файлами если файл с определённым разрешением
            if file_type:   # игнорируем файлы разрешение которых неизвестно
                is_file(folder_item, file_type)
    # удаляем папку если она пустая
    if len([a for a in path.iterdir()]) == 0:
        path.rmdir()


if __name__ == '__main__':
    if START_PATH := chek_start():
        # создаём папки для сортировки
        for fl in EXTENSION_DICT.keys():
            ff = Path(START_PATH, fl)
            if not ff.is_dir():
                ff.mkdir()
        # запускаем функцию работы с папками
        is_folder(START_PATH)
        input('Сортировка завершена успешно. Для выхода нажмите Enter')
    else:
        input('Для выхода нажмите Enter')
