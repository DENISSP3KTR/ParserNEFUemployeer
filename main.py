from bs4 import BeautifulSoup
from urllib.request import urlopen
#import pandas as pd




# Возвращает ссылки сотрудников
def get_staff_links(univer_name):
    url = 'https://www.s-vfu.ru/universitet/rukovodstvo-i-struktura/instituty/'+univer_name+'/staff'
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
    staff_about = dict()
    staff = dict()
    asd = ['/staff/724792', '/staff/722703']
    staff_category = ['Должность:', 'Повышение квалификации:', 'Участие в конференциях, симпозиумах:',
                      'Стаж работы по специальности:']
    # цикл элементов из списка ссылок на сотрудников
    for link in asd:
        url = 'https://www.s-vfu.ru'+link
        page = urlopen(url)
        html = page.read().decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')

        # Получение имени сотрудника по тегу h1, так как он единственный
        staff_name = soup.find('h1').get_text()
        for i in soup.find_all('h3', class_='h6 mb-0'):

            if i.text.strip() in staff_category:
                catt1 = i.find_next('div')
                casd = [tag.get_text(strip=True) for tag in catt1 if tag.get_text(strip=True)]
                print(staff_name, casd)
                staff_about[i.text.strip()] = casd
                print(staff_about)
        staff[staff_name] = staff_about

    return staff

print(main('imi')['Нюргуяна Романовна Пинигина'])
# print(main('imi'))


# def push_in_excel():
#     employees = main('imi')
#     FIO = []
#     position = []
#     training = []
#     for employee, employee_info in employees.items():
#         FIO.append(employee)
#         position.append(employee_info.get('Должность:'))
#         training.append(employee_info.get('Повышение квалификации:'))
#     konf = []
#     for employee, employee_info in employees.items():
#         FIO.append(employee)
#         position.append(employee_info.get('Повышение квалификации:'))
#         konf.append(employee_info.get('Участие в конференциях, симпозиумах:'))
#         print(*position)
#         print(*konf)
#
#
#
#
# print(training[1].split("/r"))
# push_in_excel()


