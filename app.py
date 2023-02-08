from flask import Flask, request, render_template, url_for, redirect, abort
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import random
from headhunter import data_vacancies, get_salar_average, get_skills


app = Flask(__name__)

# Выводит славянописи
app.config['JSON_AS_ASCII'] = False

about_me = {
           "name": "Артем",
           "surname": "Рожков",
           "email": "artemwhite666@gmail.com",
           "mobile_phone": "+7 916 440 6 110",
           "telegram": "@ArtemWhite",
           "website": "http://www.heyartem.ru/"
        }


@app.route("/about")
def about():
    
    # вывод в консоль url page 
    print(url_for("about"))

    return render_template("about.html", about_me=about_me)


@app.route("/")
def hello_world():

    # вывод в консоль адреса открываемой страницы
    print(url_for("hello_world"))
    data = "Hello, World! & Привет Артем!"

    return render_template ("hello.html", data= data)
    # return "Hello, World! & Привет Артем!"


# устанавливаю значение БД с которой буду работать
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'

# создание объекта db
db = SQLAlchemy(app)


# модель блога со статьями
class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title_art = db.Column(db.String(100), nullable=False)   
    intro_art = db.Column(db.String(300), nullable=False)
    text_art = db.Column(db.Text, nullable=False)
    date_art = db.Column(db.DateTime, default=datetime.utcnow)

    # когда буду выбирать объект, то буду получать и объект и id
    def __repr__(self) -> str:        
        return Article


# создание статьи (POST-принятие данных из формы) а если GET отправка на страницу
@app.route("/create_article", methods=["POST", "GET"])
def create_article():
    print(url_for("create_article"))

    # принимаю данные из формы
    if request.method == "POST":
        title_art = request.form["title_art"]
        intro_art = request.form["intro_art"]
        text_art = request.form["text_art"]

        # передаю данные в экземпляр класса
        article = Article(title_art=title_art, intro_art=intro_art, text_art=text_art)

        # сохраняю объект в БД
        try:
            db.session.add(article) #добавляю
            db.session.commit() #сохраняю
            return redirect("/posts")   #переадресовываю пользователя на главную страницу            
        except:
            return "При добавлении статьи произошла ошибка"

    else:
        return render_template("/article_posts/create_article.html")
    

# вывод всех статей
@app.route("/posts")
def all_posts():
    print(url_for("all_posts"))

    # # все статьи
    # articles = Article.query.all()

    # все посты с сортировкой п дате от свежих, к старым
    articles = Article.query.order_by(Article.date_art.desc()).all()

    return render_template("/article_posts/posts.html", articles=articles)


# детальный вывод статьи
@app.route("/posts/<int:id>")
def post_detail(id):    
    article = Article.query.get(id)

    return render_template("/article_posts/post_detail.html", article=article)


# удаление статьи
@app.route("/posts/<int:id>/delete")
def post_delete(id):    
    article = Article.query.get_or_404(id)  # в случае не нахождения поста вернет ошибку 404

    try:
        db.session.delete(article)
        db.session.commit()
        return redirect("/posts")
    except:
        return "При удалении поста произошла ошибка"


# редактирование статьи
@app.route("/posts/<int:id>/update", methods=["POST", "GET"])
def post_update(id):    
    article = Article.query.get(id)

    if request.method == "POST":
        article.title_art = request.form["title_art"]
        article.intro_art = request.form["intro_art"]
        article.text_art = request.form["text_art"]

        try:            
            db.session.commit()
            return redirect("/posts")
        except:
            return "При редактировании поста произошла ошибка"

    else:        
        return render_template("/article_posts/post_update.html", article=article)


# Пример 2, работа с цитатами
quotes = [
   {
       "id": 1,
       "author": "Rick Cook",
       "text": "Программирование сегодня — это гонка разработчиков программ, стремящихся писать программы с большей и лучшей идиотоустойчивостью, и вселенной, которая пытается создать больше отборных идиотов. Пока вселенная побеждает."
   },
   {
       "id": 2,
       "author": "Waldi Ravens",
       "text": "Программирование на С похоже на быстрые танцы на только что отполированном полу людей с острыми бритвами в руках."
   },
   {
       "id": 3,
       "author": "Mosher’s Law of Software Engineering",
       "text": "Не волнуйтесь, если что-то не работает. Если бы всё работало, вас бы уволили."
   },
   {
       "id": 4,
       "author": "Yoggi Berra",
       "text": "В теории, теория и практика неразделимы. На практике это не так."
   },

]


# вывод всех цитат
@app.route("/quotes")
def all_quotes():
    print(url_for("all_quotes"))

    # при выводе, сортировка в обратном порядке по id
    return render_template("/quotes/quotes.html", quotes=quotes[::-1])


# вывод общего числа цитат
@app.route("/quotes/digital")
def quotes_digital():
    print(url_for("quotes_digital"))

    digital= {
        "total_quotes": len(quotes)
    }

    return render_template("/quotes/quotes_digital.html", digital=digital)


# вывод случайной цитаты
@app.route("/quotes/random")
def quotes_random():    
    print(url_for("quotes_random"))
    quote_random = random.choice(quotes)

    return render_template("/quotes/quotes_random.html", quote_random=quote_random)


# форма ввода id цитаты для дальнейшего ее вывода
@app.route("/quotes/input_id")
def quote_input_form_id():
    print(url_for("quote_input_form_id"))

    return render_template("/quotes/quote_input_id.html")


# форма для вывода цитаты по id
@app.route("/quotes/response_id_form", methods=["POST", "GET"])
def input_id_form(): 

    if request.method == "POST":
        id_quote = int(request.form["id_qu"])        

        for quote in quotes:
            if quote["id"] == id_quote:                
                return render_template("/quotes/quote_id.html", quote=quote)

        else:
            text = "Цитаты с таким id нет 😕"
            return render_template("/quotes/quotes_no.html", text=text) 
    

# Создание новой цитаты 
@app.route("/quotes/create", methods=["POST", "GET"])
def new_quote():
    print(url_for("new_quote")) 
    
    # принимаю данные из формы
    if request.method == "POST":
        author = request.form["author"]
        text = request.form["text"]
        last_id = quotes[-1]["id"]
        new_id = last_id + 1

        new_quote = {        
            "id": new_id,
            "author": author,
            "text": text
        }
        quotes.append(new_quote)

        try:
            return redirect("/quotes") # переадресовываю на страницу со всеми цитатами            
        except:
            return "При добавлении цитаты произошла ошибка"

    else:
        return render_template("/quotes/quote_create.html")        


# удаление цитаты
@app.route("/quotes/<int:id>/delete")
def delete_quotes(id):    
    for quote in quotes:
        if int(id) == quote["id"]:
            quotes.remove(quote)
            
            return redirect("/quotes")


# Пример 3, работа с api head hunter
# Фома ввода города и вакансии
@app.route("/hh", methods=["POST", "GET"])
def hh():
    # принимаю данные из формы
    if request.method == "POST":
        data_user = request.form["data_user"]     
        data_vacancies(data_user)
        avg_salary = get_salar_average()
        skills = get_skills()
        return render_template("/hh/hh.html", avg_salary=avg_salary, skills=skills)
    else:
        skills = []
        return render_template("/hh/hh.html", skills=skills)


def main():
    app.run(debug=True)


if __name__ == "__main__":
    main()
