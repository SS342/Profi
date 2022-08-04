import flask
from flask_bcrypt import Bcrypt
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from wtforms.validators import ValidationError
from databases import FeedBackDataBase, ViewsDataBase
import logging
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

log = logging.getLogger('werkzeug')
log.disabled = True

app = flask.Flask(
    import_name=__name__,
    static_url_path=None,
    static_folder="static",
    static_host=None,
    host_matching=False,
    subdomain_matching=False,
    template_folder="templates",
    instance_path=None,
    instance_relative_config=False,
    root_path=None
)

SQLAlchemyDB = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# 2k04QdNC8FL4vbVrUjqUGGxjtKrPd1TkWThGWRtz
# PTrDXlE5pW^*KnYeOf#hWSdy!%2iR&n%NLO2hXz6@T5X2q5stu
# print(bcrypt.generate_password_hash('PTrDXlE5pW^*KnYeOf#hWSdy!%2iR&n%NLO2hXz6@T5X2q5stu'))

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///static/databases/admins.db'
app.config['SECRET_KEY'] = "IESBaofWPIfhohw398fheIUFEWGF(W3fsdbOU#F(WFGEJDSBIUW#"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
app.config['APPLICATION_ROOT'] = '/'
app.config['MAX_COOKIE_SIZE'] = 8 * 1024


class User(SQLAlchemyDB.Model, UserMixin):
    id = SQLAlchemyDB.Column(SQLAlchemyDB.Integer, primary_key=True)
    username = SQLAlchemyDB.Column(SQLAlchemyDB.String(20), nullable=False, unique=True)
    password = SQLAlchemyDB.Column(SQLAlchemyDB.String(80), nullable=False)

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(username=username.data).first()
        if existing_user_username:
            raise ValidationError(
                'That username already exists. Please choose a different one.')


SQLAlchemyDB.create_all()

'''mainADM = User(id=0,username='2k04QdNC8FL4vbVrUjqUGGxjtKrPd1TkWThGWRtz', password=bcrypt.generate_password_hash('PTrDXlE5pW^*KnYeOf#hWSdy!%2iR&n%NLO2hXz6@T5X2q5stu'))
SQLAlchemyDB.session.add(mainADM)
SQLAlchemyDB.session.commit()'''


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/admin', methods=['POST', 'GET'])
def login():
    if flask.request.method == 'POST':

        user = User.query.filter_by(username=flask.request.form['nick']).first()
        if user:
            print(user.password, flask.request.form['password'])
            if bcrypt.check_password_hash(user.password, flask.request.form['password']):
                login_user(user)

                return flask.redirect(flask.url_for('dashboard'))
            else:
                return flask.render_template('login.html')
        else:
            return flask.render_template('login.html')
    else:
        return flask.render_template('login.html')


@app.route('/dashboard')
@login_required
def dashboard():
    this_current_user = current_user
    feedback = FeedBackDataBase().GetAllFeedBackData()
    print(feedback)
    return flask.render_template('dashboard.html', feedback=feedback)


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    ViewsDataBase().NewView(page='home')
    if flask.request.method == 'POST':
        category = str(flask.request.form['exampleFormControlSelect1'])
        fio = flask.request.form['FIO']
        contact = flask.request.form['Contact']
        TextFromUser = flask.request.form['TextFromUser']
        FeedBackDataBase().NewFeedBack(category=category, fio=fio, contact=contact, feedback=TextFromUser)
        return flask.render_template('index.html')
    else:
        return flask.render_template('index.html')


HOST = config['SERVER']['host']
PORT = config['SERVER']['port']
DEBUG = eval(config['SERVER']['debug'])


if __name__ == '__main__':
    app.run(debug=True)
