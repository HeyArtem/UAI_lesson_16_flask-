# **Веб-сайт на Flask. <br/>Home work for UAI, lesson 16.**


![alt-текст](https://github.com/HeyArtem/UAI_lesson_15_tgbot_scraping/blob/master/picture_for_readme/main.png "Текст заголовка логотипа 1")



## **Тех.детали:** 
* _Flask_
* _Flask-SQLAlchemy_
* _Jinja2_
* _requests_
* _os_
* _json_
* _json_
* _random_
<br/><br/>
<hr>

## **Описание:**
## Проект состоит из трех частей:

I часть Articles (Статьи) <br/>
Здесь я создаю базу данных и предлагаю пользователью:
- ввести свою статью 
- отредактировать любую статью 
- детальный вывод статьи
- удалить статью

Все статьи храняться в базе данных. Интерфейс редактирования и удаления статьей разместил в header (шапке страницы)
<br/>
<br/>

II часть Quotes (Цитаты)<br/>
Пользователь может:
- Вывести все цитаты
- Вывести общее количество цитат
- Вывести случайную цитату
- Вывести цитату по Id
- Создать цитату

Этот раздел работает без базы данных, при остановке сервиса сохраняются только первые четыре цитаты которые прописаны у меня в скрипте.<br/>
Весь интерфейс работы с цитатами, я специально разместил только внутри этого раздела.
<br/>
<br/>

III часть Head hunter<br/>
Подключил к проекту скрипт, который работает с hh api.<br/>
Пользователю предлагается ввести на странице Вакансию и город.

Скрипт ответит:

- Среднюю зарплату 
- 20 популярных скилов
<br/><br/>
<hr>

## **Архитектура:**
- app.py<br/> 
oсновной фаил, который нужно запускать [$ python app.py]

- headhunter.py<br/>
скрипт работающий с hh api

- f_data<br/>
директорию (автоматически создается при работе headhunter.py) в которую записываются

- numb_pages.json<br/>
количество страниц с запрашиваемой вакансией на сайте https://hh.ru

- vacancies.json<br/>
все вакансии по запрашиваемой проффесии

- instance<br/>
директория (создается автоматически) с базой данных со статьями 

- templates<br/>
располложены все html-шаблоны для вывода на сайте.<br/><br/>
Все разместил согласно логике 
    - article_posts-шаблоны для работы со статьями  
    - hh-шаблоны hh 
    - quotes-для работы с цитатами
<br/><br/>
<hr>

## **Особенности:**
В проекте много уязвимостей, скрипт теряется напрмер: 
* если нет запрашиваемой вакансии в нужном городе
* если нет цитат будет ошибка: 
    * при выборе "Случайная цитата" 
    * при попытке создания цитаты
* если при создании статьи, ни чего не писать и нажать "Опубликовать", то опубликуется пустая статья


Алгоритм выбора релевантных скилов не совершенен (берет первые 20 слов с максимальным вхождением, я постарался отсортировать неинформативные), поэтому на выводе встречаются малосмысленные слова, в том числе.
<br/><br/>
<hr>

## **Что бы запустить проект:**
- создать директорию на компьютере
- открыть нужный репозиторий-Code-HTTPS-скопировать ссылку
- $ git clone + ссылка
- перейти в паку с проектом
- $ python3 -m venv venv -создать виртуальное окружение
- $ source venv/bin/activate -активировать виртуальное окружение
- $ pip install -U pip setuptools
- $ pip install -r requirements.txt -установить библиотеки из requirements.txt
- $ code . -открыть проект в VS Code
- в headhunter.py -> def get_salar_average -> прописать file_path (путь до vacancies.json)
- запустить app.py
<br/><br/>
<hr>



```
![alt-текст](https://github.com/HeyArtem/UAI_lesson_15_tgbot_scraping/blob/master/picture_for_readme/1.png "Exemple 1")
![alt-НЕтекст](https://github.com/HeyArtem/UAI_lesson_15_tgbot_scraping/blob/master/picture_for_readme/2.png "Exemple 2")
![alt-текст](https://github.com/HeyArtem/UAI_lesson_15_tgbot_scraping/blob/master/picture_for_readme/3.png "Exemple 3")
![alt-текст](https://github.com/HeyArtem/UAI_lesson_15_tgbot_scraping/blob/master/picture_for_readme/4.png "Exemple 4")
![alt-текст](https://github.com/HeyArtem/UAI_lesson_15_tgbot_scraping/blob/master/picture_for_readme/5.png "Exemple 5")

