from datetime import datetime, timedelta


def get_birthdays_per_week(users: list):
    """выводит в консоль (при помощи print) список пользователей, которых надо поздравить по дням."""
    # находим начало и конец недели с учётом смещения на выходные дни
    time_now = datetime.now()
    if time_now.weekday() == 0:
        start_day = time_now - timedelta(days=2)
    elif time_now.weekday() == 6:
        start_day = time_now - timedelta(days=1)
    else:
        start_day = time_now
    end_day = start_day + timedelta(days=6)

    # создаём словарь с датами и днями недели с учётом смещения
    days_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Monday', 'Monday']
    days_week_dict = {}
    td = 0
    while True:
        dd = start_day + timedelta(days=td)
        days_week_dict[datetime.strftime(dd, '%m-%d')] = days_week[dd.weekday()]
        if dd == end_day:
            break
        td += 1

    # в списке users находим имена которые попадают в дату недели и создаём словарь {week: [name1, name2...], ... }
    start_day = datetime.strftime(start_day, '%m-%d')
    end_day = datetime.strftime(end_day, '%m-%d')
    birthday_dict = {}
    for user in users:
        if start_day <= (b_day := datetime.strftime(user['birthday'], '%m-%d')) <= end_day:
            if birthday_dict.get(days_week_dict[b_day]):
                birthday_dict[days_week_dict[b_day]].append(user['name'])
            else:
                birthday_dict[days_week_dict[b_day]] = [user['name']]
                
    # печатаем результат
    for week, name in birthday_dict.items():
        print(f'{week}: {", ".join(name)}')

