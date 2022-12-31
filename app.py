from flask import Flask, request, render_template, url_for, redirect, abort
import sqlite3
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import random


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
        # return '<Article %r>' % self.id     # !! переделать на нов f row ????????
        return Article   # !! переделать на нов f row ????????


# создание поста (POST-принятие данных из формы) а если GET отправка на страницу создания????????
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
            # return redirect("/")   
        except:
            return "При добавлении статьи произошла ошибка"

    else:
        return render_template("/article_posts/create_article.html")
    

# вывод всех постов
@app.route("/posts")
def all_posts():
    print(url_for("all_posts"))

    # # все статьи
    # articles = Article.query.all()

    # все посты с сортировкой п дате от свежих, к старым
    articles = Article.query.order_by(Article.date_art.desc()).all()    
    
    # return f"Hello, World! & Привет Артем!"
    # return render_template("posts_test.html", articles=articles)
    return render_template("/article_posts/posts.html", articles=articles)


# детальный вывод поста
@app.route("/posts/<int:id>")
def post_detail(id):
    # print(url_for("post_detail"))
    article = Article.query.get(id)
    return render_template("/article_posts/post_detail.html", article=article)


# удаление поста
@app.route("/posts/<int:id>/delete")
def post_delete(id):
    # print(url_for("post_delete"))
    article = Article.query.get_or_404(id)  # в случае не нахождения поста вернет ошибку 404

    try:
        db.session.delete(article)
        db.session.commit()
        return redirect("/posts")
    except:
        return "При удалении поста произошла ошибка"


# редактирование поста
@app.route("/posts/<int:id>/update", methods=["POST", "GET"])
def post_update(id):
    # print(url_for("/posts/<int:id>/update"))
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
    # quotes_sort = quotes.order_by(quotes.id.desc()).all()    
    # quotes_sort = quotes.order_by(quotes.id.desc()).all()    
    # quotes_sort = quotes.sort(int(quotes["id"]))
    # quotes_sort = quotes.sort(key=lambda dictionary: dictionary["id"])
    # quotes_sort = quotes.sort(quotes.)
    
    # return quotes_sort

    return render_template("/quotes/quotes.html", quotes=quotes)


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


# форма ввода id
@app.route("/quotes/input_id")
def quote_input_form_id():
    print(url_for("quote_input_form_id"))

    return render_template("/quotes/quote_input_id.html")

# форма для ввода цитаты по id
@app.route("/quotes/response_id_form", methods=["POST", "GET"])
def input_id_form(): 

    if request.method == "POST":
        id_quote = int(request.form["id_qu"])
        print(f" [!] id_quote: {id_quote}")

        for quote in quotes:
            print(f" [!] Перебор цитат: {quote}")

            if quote["id"] == id_quote:
                print(f" [!] quote['id']: {quote['id']}")
                
                result = quote['id']
                print(f" [!] result: {result}")

                return render_template("/quotes/quote_id.html", quote=quote)

        else:
            text = "Цитаты с таким id нет 😕"

            return render_template("/quotes/quotes_no.html", text=text) 
    

# Создание новой цитаты 
@app.route("/quotes/create", methods=["POST", "GET"])
def new_quote():
    print(url_for("new_quote")) 
    # return render_template("quote_create.html")
    
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
            # return render_template("quotes_new.html", new_quotes=new_quotes)
            return redirect("/quotes") # переадресовываю на страницу со всеми цитатами
            # return new_quote
        except:
            return "При добавлении цитаты произошла ошибка"

    else:
        return render_template("/quotes/quote_create.html")
        # return "Hui"
    # http://localhost:5000/quotes/create


# удаление цитаты
# @app.route("/quotes/<int:id>/delete", methods=["DELETE"])
@app.route("/quotes/<int:id>/delete")
def delete_quotes(id):
    # print(url_for("delete_quotes"))
    print(" [!] start delete_quotes")   
    
    for quote in quotes:
        if int(id) == quote["id"]:
            quotes.remove(quote)
            # return f"Цитата {id} удалена"
            return redirect("/quotes")
        



@app.route("/hui")
def hui_tebe():
    x = "hui tebe"
    return render_template("/test_fol/hui.html", data=x)












def main():
    app.run(debug=True)


if __name__ == "__main__":
    main()