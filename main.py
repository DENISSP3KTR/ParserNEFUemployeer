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
    staff = dict()
    asd = ['/staff/724792', '/staff/722703']
    # цикл элементов из списка ссылок на сотрудников
    for link in asd:
        url = 'https://www.s-vfu.ru'+link
        page = urlopen(url)
        html = page.read().decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')

        # Получение имени сотрудника по тегу h1, так как он единственный
        staff_name = soup.find('h1').get_text()

        # Ищим все имена категорий. Например: Должность, Ученая степень и тд
        category_key = soup.find_all('h3', class_='h6 mb-0')
        # Ищим все значение категорий. Например: директор, кдн
        category_value = soup.find_all('div', class_='g-px-10 pre-wrap')

        # внутри цикла создается словарь Категория ключ - имя категории, значение - значение категории
        staff_about = dict()
        for i, j in zip(category_key, category_value):
            staff_about[i.text.strip()] = j.text.strip()

        #создается словарь: ключ = имя сотрудника, значение = словарь Категория
        staff[staff_name] = staff_about
    return staff


#print(main('imi'))

def push_in_excel():
    employees = main('imi')
    FIO = []
    position = []
    training = []
    for employee, employee_info in employees.items():
        FIO.append(employee)
        position.append(employee_info.get('Должность:'))
        training.append(employee_info.get('Повышение квалификации:'))

    

    print(training[1].split("/r"))
push_in_excel()
