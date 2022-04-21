import os
from os import abort

from flask import Flask, render_template, request, make_response, session, url_for
from werkzeug.utils import redirect

from data import db_session
from data.demons import Demons
from data.others import Others
from data.suzhet import Suzhet
from data.users import User, LoginForm
from data.news import News
import datetime

from data import news_api
from forms.demons import DemonsForm
from forms.news import NewsForm
from forms.others import OthersForm
from forms.suzhet import SuzhetForm
from forms.user import RegisterForm
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(
    days=365
)
@app.route("/")
def first():
    return render_template("first.html")


@app.route("/Characters")
def index():
    db_sess = db_session.create_session()
    if current_user.is_authenticated:
        news = db_sess.query(News).filter(
            (News.user == current_user) | (News.is_private != True))
    else:
        news = db_sess.query(News).filter(News.is_private != True)
    return render_template("index.html", news=news)


@app.route("/Suzhets")
def indes():
    db_sess = db_session.create_session()
    if current_user.is_authenticated:
        suzhet = db_sess.query(Suzhet).filter(
            (Suzhet.user == current_user) | (Suzhet.is_private != True))
    else:
        suzhet = db_sess.query(Suzhet).filter(Suzhet.is_private != True)
    return render_template("index2.html", suzhet=suzhet)


@app.route("/Demons")
def indez():
    db_sess = db_session.create_session()
    if current_user.is_authenticated:
        demons = db_sess.query(Demons).filter(
            (Demons.user == current_user) | (Demons.is_private != True))
    else:
        demons = db_sess.query(Demons).filter(Demons.is_private != True)
    return render_template("index3.html", demons=demons)


@app.route('/addDemons',  methods=['GET', 'POST'])
@login_required
def add_demons():
    form = DemonsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        demons = Demons()
        demons.title = form.title.data
        demons.age = form.age.data
        demons.status = form.status.data
        demons.content = form.content.data
        demons.is_private = form.is_private.data
        current_user.demons.append(demons)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/Demons')
    return render_template('demons.html', title='Добавление демона',
                           form=form)


@app.route('/watch_demons/<int:id>', methods=['GET', 'POST'])
def watch_demons(id):
    form = DemonsForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        demons = db_sess.query(Demons).filter(Demons.id == id

                                          ).first()
        if demons:
            form.title.data = demons.title
            form.age.data = demons.age
            form.status.data = demons.status
            form.content.data = demons.content
            form.is_private.data = demons.is_private
        else:
            abort(404)
    if 'акадза' in form.title.data.lower():
        return render_template('demons2.html', form=form)
    if 'кокушибо' in form.title.data.lower():
        return render_template('demons_kok.html', form=form)
    if 'мудзан' in form.title.data.lower():
        return render_template('demons_muz.html', form=form)
    else:
        return render_template('demons_none.html', form=form)


@app.route('/edit_demons/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_demons(id):
    form = DemonsForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        demons = db_sess.query(Demons).filter(Demons.id == id,
                                          Demons.user == current_user
                                          ).first()
        if demons:
            form.title.data = demons.title
            form.age.data = demons.age
            form.status.data = demons.status
            form.content.data = demons.content
            form.is_private.data = demons.is_private
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        demons = db_sess.query(Demons).filter(Demons.id == id,
                                          Demons.user == current_user
                                          ).first()
        if demons:
            demons.title = form.title.data
            demons.age = form.age.data
            demons.status = form.status.data
            demons.content = form.content.data
            demons.is_private = form.is_private.data
            db_sess.commit()
            return redirect('/Demons')
        else:
            abort(404)
    return render_template('demons3.html', form=form)


@app.route('/demons_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def demons_delete(id):
    db_sess = db_session.create_session()
    demons = db_sess.query(Demons).filter(Demons.id == id,
                                      Demons.user == current_user
                                      ).first()
    if demons:
        db_sess.delete(demons)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/Demons')


@app.route("/Others")
def indew():
    db_sess = db_session.create_session()
    if current_user.is_authenticated:
        others = db_sess.query(Others).filter(
            (Others.user == current_user) | (Others.is_private != True))
    else:
        others = db_sess.query(Others).filter(Others.is_private != True)
    return render_template("index4.html", others=others)


@app.route('/addOthers',  methods=['GET', 'POST'])
@login_required
def add_others():
    form = OthersForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        others = Others()
        others.title = form.title.data
        others.age = form.age.data
        others.status = form.status.data
        others.content = form.content.data
        others.is_private = form.is_private.data
        current_user.others.append(others)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/Others')
    return render_template('others.html', title='Добавление персонажа',
                           form=form)


@app.route('/watch_others/<int:id>', methods=['GET', 'POST'])
def watch_others(id):
    form = OthersForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        others = db_sess.query(Others).filter(Others.id == id

                                          ).first()
        if others:
            form.title.data = others.title
            form.age.data = others.age
            form.status.data = others.status
            form.content.data = others.content
            form.is_private.data = others.is_private
        else:
            abort(404)
    if 'тамаё' in form.title.data.lower():
        return render_template('others2.html', form=form)
    if 'аой' in form.title.data.lower():
        return render_template('others_aoi.html', form=form)
    else:
        return render_template('demons_none.html', form=form)


@app.route('/edit_others/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_others(id):
    form = OthersForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        others = db_sess.query(Others).filter(Others.id == id,
                                          Others.user == current_user
                                          ).first()
        if others:
            form.title.data = others.title
            form.age.data = others.age
            form.status.data = others.status
            form.content.data = others.content
            form.is_private.data = others.is_private
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        others = db_sess.query(Others).filter(Others.id == id,
                                          Others.user == current_user
                                          ).first()
        if others:
            others.title = form.title.data
            others.age = form.age.data
            others.status = form.status.data
            others.content = form.content.data
            others.is_private = form.is_private.data
            db_sess.commit()
            return redirect('/Others')
        else:
            abort(404)
    return render_template('others3.html', form=form)


@app.route('/others_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def others_delete(id):
    db_sess = db_session.create_session()
    others = db_sess.query(Others).filter(Others.id == id,
                                      Others.user == current_user
                                      ).first()
    if others:
        db_sess.delete(others)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/Others')


@app.route('/addSuzhet',  methods=['GET', 'POST'])
@login_required
def add_suzhets():
    form = SuzhetForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        suzhets = Suzhet()
        suzhets.title = form.title.data
        suzhets.content = form.content.data
        suzhets.is_private = form.is_private.data
        current_user.suzhet.append(suzhets)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/Suzhets')
    return render_template('suzheti.html', title='Добавление события',
                           form=form)


@app.route('/watch_suzhet/<int:id>', methods=['GET', 'POST'])
def watch_suzhet(id):
    form = SuzhetForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        suzhet = db_sess.query(Suzhet).filter(Suzhet.id == id
                                              ).first()
        if suzhet:
            form.title.data = suzhet.title
            form.content.data = suzhet.content
            form.is_private.data = suzhet.is_private
        else:
            abort(404)
    return render_template('suzheti2.html', form=form)


@app.route('/suzhet/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_suzhet(id):
    form = SuzhetForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        suzhet = db_sess.query(Suzhet).filter(Suzhet.id == id,
                                          Suzhet.user == current_user
                                          ).first()
        if suzhet:
            form.title.data = suzhet.title
            form.content.data = suzhet.content
            form.is_private.data = suzhet.is_private
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        suzhet = db_sess.query(Suzhet).filter(Suzhet.id == id,
                                          Suzhet.user == current_user
                                          ).first()
        if suzhet:
            suzhet.title = form.title.data
            suzhet.content = form.content.data
            suzhet.is_private = form.is_private.data
            db_sess.commit()
            return redirect('/Suzhets')
        else:
            abort(404)
    return render_template('suzheti.html', form=form)


@app.route('/suzhet_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def suzhet_delete(id):
    db_sess = db_session.create_session()
    suzhet = db_sess.query(Suzhet).filter(Suzhet.id == id,
                                      Suzhet.user == current_user
                                      ).first()
    if suzhet:
        db_sess.delete(suzhet)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/Suzhets')


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/news',  methods=['GET', 'POST'])
@login_required
def add_news():
    form = NewsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        news = News()
        news.title = form.title.data
        news.age = form.age.data
        news.status = form.status.data
        news.content = form.content.data
        news.is_private = form.is_private.data
        current_user.hashiras.append(news)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/Characters')
    return render_template('news.html', title='Добавление новости',
                           form=form)


@app.route('/watch_news/<int:id>', methods=['GET', 'POST'])
def watch_news(id):
    form = NewsForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        news = db_sess.query(News).filter(News.id == id
                                          ).first()
        if news:
            form.title.data = news.title
            form.age.data = news.age
            form.status.data = news.status
            form.content.data = news.content
            form.is_private.data = news.is_private
        else:
            abort(404)
    if 'тандзиро' in form.title.data.lower():
        return render_template('news2.html', form=form)
    if 'томиока' in form.title.data.lower():
        return render_template('news_tomioka.html', form=form)
    if 'шинобу' in form.title.data.lower():
        return render_template('news_shinobu.html', form=form)
    else:
        return render_template('demons_none.html', form=form)


@app.route('/news/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_news(id):
    form = NewsForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        news = db_sess.query(News).filter(News.id == id,
                                          News.user == current_user
                                          ).first()
        if news:
            form.title.data = news.title
            form.age.data = news.age
            form.status.data = news.status
            form.content.data = news.content
            form.is_private.data = news.is_private
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        news = db_sess.query(News).filter(News.id == id,
                                          News.user == current_user
                                          ).first()
        if news:
            news.title = form.title.data
            news.age = form.age.data
            news.status = form.status.data
            news.content = form.content.data
            news.is_private = form.is_private.data
            db_sess.commit()
            return redirect('/Characters')
        else:
            abort(404)
    return render_template('news.html', form=form)


@app.route('/news_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def news_delete(id):
    db_sess = db_session.create_session()
    news = db_sess.query(News).filter(News.id == id,
                                      News.user == current_user
                                      ).first()
    if news:
        db_sess.delete(news)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/Characters')


def main():
    db_session.global_init("db/blogs.db")
    app.register_blueprint(news_api.blueprint)
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)


if __name__ == '__main__':
    main()