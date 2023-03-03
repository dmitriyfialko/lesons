from multiprocessing import Pool, cpu_count
import math
import time


def decor(func):
    def wrapper(*number):
        tm = time.time()
        print('Start factorize')
        f = func(*number)
        print(f'Time: {time.time()-tm} s')
        return f
    return wrapper


def search_f(number) -> list:
    lst = []
    nn = 1
    while nn <= number:
        if not math.fmod(number, nn):
            lst.append(nn)
        nn += 1
    return lst


@decor
def factorize(*number):
    # ls = map(search_f, number)
    with Pool(cpu_count()) as p:
        ls = p.map(search_f, number)
    return ls


if __name__ == '__main__':
    a, b, c, d = factorize(128, 255, 99999, 10651060)

    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]
