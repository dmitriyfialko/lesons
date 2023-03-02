import argparse
from pathlib import Path
from threading import Thread
from shutil import move
import logging


OUTPUT = Path('output')


def is_file(path):
    path = Path(path)
    suffix = path.suffix.strip('.')
    output = Path(OUTPUT, suffix) if suffix else Path(OUTPUT, 'no_extension')
    if not output.exists():
        output.mkdir()
    try:
        move(path.absolute(), output.absolute())
        logging.debug(f'file {path} moved to folder {output}')
    except OSError:
        logging.debug(f'No access to file "{path}"')


def is_folder(path):
    threads = []
    path = Path(path)
    for folder_item in path.iterdir():
        item = Path(folder_item)
        if item.is_dir():
            if item.absolute() == OUTPUT.absolute():
                continue
            # запускаем потоки рекурсивно
            thread_f = Thread(target=is_folder, args=(item, ))
            thread_f.start()
            threads.append(thread_f)
        else:
            thread_d = Thread(target=is_file, args=(item, ))
            thread_d.start()
            threads.append(thread_d)
    # ждём окончания потоков и удаляем папку если она пустая
    [thr.join() for thr in threads]
    if len([a for a in path.iterdir()]) == 0:
        path.rmdir()
        logging.debug(f'folder {path} deleted')


def main(source):
    start_path = Path(source)
    if start_path.is_dir():
        global OUTPUT
        OUTPUT = Path(start_path, 'output')
        if not OUTPUT.exists():
            OUTPUT.mkdir()
        thread = Thread(target=is_folder, args=(start_path, ))
        thread.start()
        thread.join()
        logging.debug(f'Sorting complete')
    else:
        raise ValueError(f'{source} is not a folder')


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format='%(threadName)s %(message)s')

    parser = argparse.ArgumentParser(description='Sorting folder')
    parser.add_argument('-s', '--source', required=True)
    args = vars(parser.parse_args())

    main(args.get('source'))
