from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd
import datetime


# Возвращает ссылки сотрудников
def get_staff_links(univer_name):
    url = 'https://www.s-vfu.ru/universitet/rukovodstvo-i-struktura/instituty/' + univer_name + '/staff'
    page = urlopen(url)
    html = page.read().decode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')
    links = []
    # soup.find_all('a') - список всех тегов а
    for link in soup.find_all('a'):
        # Получение ссылки из href лежащего внутри тега а
        l = link.get('href')
        # Если l не пустой и ссылка имеет /staff, то добавить в список
        if (l is not None) and (l.startswith('/staff')):
            links.append(l)
    return links


def main(univer_name):
    staff = dict()
    asd = ['/staff/724792', '/staff/722703']
    staff_category = ['Должность:', 'Повышение квалификации:', 'Участие в конференциях, симпозиумах:',
                      'Стаж работы по специальности:']
    # цикл элементов из списка ссылок на сотрудников
    for link in asd:
        url = 'https://www.s-vfu.ru' + link
        page = urlopen(url)
        html = page.read().decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')

        # Получение имени сотрудника по тегу h1, так как он единственный
        staff_name = soup.find('h1').get_text()
        staff_about = dict()
        for i in soup.find_all('h3', class_='h6 mb-0'):

            if i.text.strip() in staff_category:
                catt1 = i.find_next('div')
                casd = [tag.get_text(strip=True) for tag in catt1 if tag.get_text(strip=True)]
                staff_about[i.text.strip()] = casd
        staff[staff_name] = staff_about

    return staff


# print(main('imi'))


def push_in_excel():
    employees = main('imi')
    year_training = []
    year_konf = []
    year = datetime.datetime.now().year
    for i in range(0, 5):
        year_training.append(str(year - i))
    for i in range(0, 3):
        year_konf.append(str(year - i))
    FIO = []
    position = []
    training = []
    klaf = []
    work_exp = []
    for employee, employee_info in employees.items():
        FIO.append(employee)
        position.append(employee_info.get('Должность:')[0])
        training.append(employee_info.get('Повышение квалификации:'))
        klaf.append(employee_info.get('Участие в конференциях, симпозиумах:'))
        work_exp.append(employee_info.get('Стаж работы по специальности:'))

    # Поиск повышения квалификации за последние 5 лет
    for index1, empl in enumerate(training):
        if empl:
            for index2, train_info in enumerate(empl):
                if not any(x in train_info for x in year_training):
                    training[index1].pop(index2)

                    # Поиск участие в конференциях, симпозиумах за последние 3 года

    for index1, empl in enumerate(klaf):
        if empl:
            for index2, klaf_info in enumerate(empl):
                if not any(x in klaf_info for x in year_konf):
                    klaf[index1].pop(index2)

    print(klaf[0])


push_in_excel()