from gettext import find
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
    asd = ['/staff/724792', '/staff/895039920']
    staff_category = ['Должность:', 'Повышение квалификации:', 'Участие в конференциях, симпозиумах:',
                      'Стаж работы по специальности:']
    # цикл элементов из списка ссылок на сотрудников
    for link in asd:  #get_staff_links(univer_name):
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
    fio = []
    position = []  
    training = []
    training_in_string = []
    konf = []
    konf_in_string = []
    work_exp = []

    year = datetime.datetime.now().year
    for i in range(0, 5):
        year_training.append(str(year - i))
    for i in range(0, 3):
        year_konf.append(str(year - i))
    
    
    for employee, employee_info in employees.items():
        fio.append(employee)
        position.append(employee_info.get('Должность:')[0])
        training.append(employee_info.get('Повышение квалификации:'))
        konf.append(employee_info.get('Участие в конференциях, симпозиумах:'))
        work_exp.append(employee_info.get('Стаж работы по специальности:'))

    # Поиск повышения квалификации за последние 5 лет
    for index1, empl in enumerate(training):
        if not (empl is None):
            i = 0
            while i < len(training[index1]):
                if not any(x in training[index1][i] for x in year_training):
                    training[index1].pop(i)
                else:
                    i += 1    


    # Поиск участие в конференциях, симпозиумах за последние 3 года             
    for index1, empl in enumerate(konf):
        if not (empl is None):
            i = 0
            while i < len(konf[index1]):      
                if not any(x in konf[index1][i] for x in year_konf):
                    konf[index1].pop(i)
                else:
                    i += 1    

    #print(employees)

    for i in training:
        if not (i is None):
            training_in_string.append(' '.join(i))
    for i in konf:
        if not (i is None):
            konf_in_string.append(' '.join(i))

    if len(training_in_string) > len(konf_in_string):
        for i in range(0, (len(training_in_string) - len(konf_in_string))):
            konf_in_string.append('')
    if len(training_in_string) < len(konf_in_string):
        for i in range(0, (len(konf_in_string) - len(training_in_string))):
            training_in_string.append('')

    # print(training_in_string)
    df = pd.DataFrame({'ФИО': fio, 'Должность': position, 'Повышение квалификации': training_in_string, 'Участие в конференциях, симпозиумах': konf_in_string, 'Стаж работы по специальности': work_exp})
    df.to_excel('./employees.xlsx',  sheet_name='Сотрудники', index=False)    
    

push_in_excel()