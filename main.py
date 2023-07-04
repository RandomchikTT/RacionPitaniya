import requests
from bs4 import BeautifulSoup
import re

class Food:
    def __int__(self, name, calories):
        self.Name = name
        self.Calories = calories
    def Print(self):
        print("Название:", self.Name, "Ккалории продукта:", self.Calories)

weight = float(input("Введите ваш вес: "))
height = int(input("Введите ваш рост: "))
years = int(input("Введите сколько вам лет: "))
isGender = bool(input("Введите ваш пол(1 - Мужской, 0 - Женский): "))

norma = 1
if isGender:
    norma = 66.5 + (13.75 * weight) + (5.003 * height) - (6.775 * years)
else:
    norma = 655.1 + (9.563 * weight) + (1.85 * height) - (4.676 * years)

print("Норма каллорий для вас в день:", norma)

ListMyFood = []
ReceptArrays = ["recept", "recipes"]

countEatTake = int(input("Сколько было приемов пищи сегодня: "))
for i in range(countEatTake):
    # Цикл на то если не найдет элемент на сайте
    while True:
        eat = input("Введите название еды: ")
        # Поиск подходящей еды
        response = requests.get('https://calorizator.ru/search/node/' + eat)
        soup = BeautifulSoup(response.text, 'html.parser')
        # Поиск всех подходяших элементов
        dlList = soup.find('dl')
        if dlList == None:
            print("Данный предмет не был найден. Повторите название")
            continue
        ListFindItems = dlList.findAll('a')
        ListAcceptItems = []
        # Сортировка подходяших обектов
        for item in ListFindItems:
            if not re.findall(r'|'.join(ReceptArrays), str(item["href"])):
                ListAcceptItems.append(item)
        # Вывод всех подходящих элементов
        selectItem = -1
        if len(ListAcceptItems) <= 0:
            print("По вашему запросы не было найдено подходящей еды!")
            continue
        # Выбор подходяшего элемента
        if len(ListAcceptItems) > 1:
            print("По вашему запросы были найдены:")
            for eat in ListAcceptItems:
                print("Название продукта:", eat.text, "Номер:", ListAcceptItems.index(eat))
            indexSelectItem = int(input("Введите номер который вам подошел: "))
            if not indexSelectItem in range(len(ListAcceptItems)):
                print("Вы ввели неверный номер!")
                exit()
            selectItem = ListAcceptItems[indexSelectItem]
        else:
            selectItem = ListAcceptItems[0]
        # Достаем данные с карточки выбранного предмета
        try:
            selectItemJSON = requests.get(selectItem["href"])
            soup = BeautifulSoup(selectItemJSON.text, 'html.parser')
            itemCallories = soup.find("fieldset", class_="fieldgroup group-base").find("div", class_="field-item odd").contents[2]
            food = Food()
            food.Name = str(selectItem.text)
            food.Calories = float(itemCallories)
            ListMyFood.append(food)
            print("Предмет был успешно добавлен в список.")
        except:
            print("Ошибка получения данных об продуктах.")
            continue
        break
eatingCallories = 0
print("Список еды которую вы сьели:")
for food in ListMyFood:
    food.Print()
    eatingCallories += food.Calories
if eatingCallories > norma:
    print("Вы переели сегодня норму ккаллорий на", eatingCallories - norma)
else:
    if eatingCallories == norma:
        print("Вы сьели свою норму ккаллорий")
    else:
        print("Вы не доели свою норму ккалорий:", norma - eatingCallories)