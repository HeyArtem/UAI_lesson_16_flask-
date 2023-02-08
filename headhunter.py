import requests
import os
import json

# def test_hh():
#     print(f"\n [!] Активирована функция def test_hh внутри страницы headhunter.py")
#     search = input("Введите число: ")
    
#     a = 10 * int(search)
#     print(f"\n    [!] Принт результата test_hh(): {a}")
    
#     # почему не передаются данные в кортеже?
#     tuple_data = (f"{search}", f"{a}")
#     print(f"\n    [!] Принт внутри test_hh type tuple_data: {type(tuple_data)}")
#     print(f"\n    [!] Принт внутри test_hh tuple_data[0]: {tuple_data[0]}")
#     print(f"\n    [!] Принт внутри test_hh tuple_data[1]: {tuple_data[1]}")
#     return tuple_data

#     # # пробую передать денные в словаре
#     # dict_data = {}
#     # dict_data['search'] = search
#     # dict_data['res'] = a

#     # print(f"\n    [!] Принт внутри test_hh dict_data: {dict_data}")
#     # print(f"\n    [!] Принт внутри test_hh type dict_data: {type(dict_data)}")
#     # return dict_data



# Сбор вакансий
def data_vacancies(search):
    # Поисковый запрос разделил и склеил союзом "AND"
    data = search.split()    
    search = " AND ".join(data)
    
    # Записал поисковые слова в params
    params = {"text": f"{search}"}

    url = "https://api.hh.ru/vacancies"

    # Нашел количество страниц
    pages = requests.get(url=url, params=params).json()["pages"]

    # Создаю директорию "f_data" для сохранения файлов
    if not os.path.exists("f_data"):
        os.mkdir("f_data")

    # Записал результат (количество страниц) в "numb_pages.json"
    with open("f_data/numb_pages.json", mode="w") as file:
        json.dump(pages, file, indent=4, ensure_ascii=False)

    # В эту переменную буду записывать вакансии
    vacancies = []

    # В цикле прохожу по всем страницам, делаю запрос к каждой
    # for page in range(pages):
    for page in range(2):
        params = {"text": f"{search}", "page": page}
        items = requests.get(url=url, params=params).json()["items"]

        # Полученные вакансии записываю в переменную "vacancies"
        vacancies.extend(items)

    # Информацию из "vacancies" записываю в фаил "vacancies.json"
    with open("f_data/vacancies.json", mode="w") as file:
        json.dump(vacancies, file, indent=4, ensure_ascii=False)
    
    return f"\n [!] Вакансии по запросу: {search}, записаны в фаил: vacancies.json"


# Высчитываю среднюю зарплату
# ! Путь прописать по месту
def get_salar_average(file_path="/home/heyartem/PycharmProjects/uai_lesson_16_flask/f_data/vacancies.json"): 

    # Читаю данные в переменную "src"
    with open(file=file_path) as file:
        src = json.load(file)

    # в эту переменну. буду записывать среднюю зп
    salary_average = []

    for vac in src:
        # Переменные Максимальной и Минимальной зп
        max_sal, min_sal = 0, 0

        # Если в вакансии (vac) есть раздел "salary" и он в рублях ("currency": "RUR")
        if vac["salary"] and vac["salary"]["currency"] == "RUR":

            # Если в разделе "salary", есть подразделы "from" & "to" (если оба раздела не заполнены, то "from" & "to" - нет, а "salary": null)
            if vac["salary"]["from"] and vac["salary"]["to"]:
                min_sal = int(vac["salary"]["from"])
                max_sal = int(vac["salary"]["to"])

            # Если в разделе "salary", нет подраздела "from", но есть "to"
            elif not vac["salary"]["from"] and vac["salary"]["to"]:
                max_sal = int(vac["salary"]["to"])
                min_sal = max_sal

            # Если в разделе "salary", есть подраздел "from", но нет подраздела "to"
            elif vac["salary"]["from"] and not vac["salary"]["to"]:
                min_sal = int(vac["salary"]["from"])
                max_sal = min_sal

        # print(f"\n    [!] Вычисление средней зп: {max_sal} & {min_sal}\n Средняя зп : {((max_sal + min_sal) / 2)}\n")

        # Если сумма Максимальной и Минимальной зарплат > 0, высчитываю среднюю зарплату
        if (min_sal + max_sal) / 2 > 0:            
            salary_average.append((min_sal + max_sal) / 2)

            # print(f"\n    [!] salary_average: {salary_average}\n")

    # Вывожу среднюю зп, поделил сумму зарплат на их количество
    total_salaty_average = round(sum(salary_average) / len(salary_average), 2)
    # return "get_salart_average is ok!"
    res = f"\n Средняя зп составляет: {int(total_salaty_average)}" 
    # print("\n [!] А так? ", total_salaty_average)
    return int(total_salaty_average)
    # return res


# Работа со скилами (requirement - требование)
def get_skills(file_path="/home/heyartem/PycharmProjects/uai_lesson_16_flask/f_data/vacancies.json"):

    # Читаю данные в переменную 
    with open(file=file_path) as file:
        vacancies = json.load(file)

    # в эту переменную записываю требуемые скилы
    skills = []

    # Из всех вакансий выписал требования
    for vac in vacancies:
        if vac["snippet"]["requirement"]:
            skills.append(vac["snippet"]["requirement"])

    # Список слов
    words_list = []

    # Требования разбил на слова
    for char in skills:
        words_list.extend(char.split())
    
    # print(words_list)

    # Грязная зачистка. Из последовательности world_list, убираю следующие символы, привожу их к нижнему регистру
    symbols = [',', '.', ';', ':', '<highlighttext>', '</highlighttext>', '/', ')', '(', 'e.g.', '—', '–', '1', '2']
    
    for word in range(len(words_list)):
        for symbol in symbols:
            if symbol in words_list[word].lower():
                words_list[word] = words_list[word].replace(symbol, "")

    # print("\nпосле Грязной зачистки: ", words_list)

    # Привожу все участников последовательности к нижнему регистру
    lower_case = [item_case.lower() for item_case in words_list if item_case]

    # print("\nПривели к нижнему регистру: ", lower_case)

    # Вторичная зачистка. Удаляю разные союзы, предлоги, неинформативные слова
    symbols_2 = ['и', 'знание', 'с', 'на', 'работы', 'в', 'к', 'and', 'хорошее', 'языках', 'отличное', 'имеете' 'имеете', 'использования' 'приложений', 'образование',  'писать', 'автоматизации', 'разработки', 'или', 'программирования', 'данных', 'понимание', 'умение', 'от', '-', 'знания', 'лет', 'навыки', 'языков', 'владение', 'будет', 'написания', 'уверенное', 'уровне', 'для', 'по', 'принципов', 'из', 'плюсом', 'желательно', 'работать', 'высшее', '3', 'языка', 'r', 'не',  'скриптов',  'experience', 'систем', 'как', 'желание', 'года', 'базовые', 'in', 'анализа', 'мы', 'вы', 'гибкость', 'под', 'есть', 'если', 'приветствуется', 'одного'] 

    for word in range(len(lower_case)):
        for symbol in symbols_2:
            if symbol == lower_case[word].lower():
                lower_case[word] = lower_case[word].replace(symbol, "")
    lower_case = [item.lower() for item in lower_case if item]

    # print("\nпосле Вторичной зачистки: ", lower_case)

    # Считаю вхождение (встречаемость слов)
    frequency_dict = {}

    for k in lower_case:
        frequency_dict[k] = lower_case.count(k)

    # print("\nПодсчитал вхождения: ", frequency_dict)

    # Сортирую по убыванию
    sort_skills = list(frequency_dict.items())
    sort_skills.sort(key=lambda x: x[1], reverse=True)

    number = sum([i[1] for i in sort_skills[:20]])

    # навыки и % встречаемости
    skills_result = []

    for item in sort_skills:
        skills_result.append(
            {
                item[0]: round(100*item[1]/number, 2)
            }
        )
    
    return skills_result[:20]



    # return "get_skills is OK!"

    

# print(data_vacancies())
# print(get_salar_average())
print(get_skills())

# def main():
    # data_vacancies()
    # print(f"Средняя зп: {get_salar_average} рублей.")

    # result = get_skills()
    # print("Навыки и % Встречаемости:")
    # for item in result:
    #     for k,v in item.items():
    #         print(f"{k.title()}: {v}%")
    # print(test_hh())
    # test_hh()
