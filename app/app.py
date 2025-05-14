from flask import Flask, render_template
from flask_login import LoginManager

from data import db_session


app = Flask(__name__)
app.config['SECRET_KEY'] = 'kwmconcibcwnqklmsmlknxjwbncbwud'

# login_manager = LoginManager()
# login_manager.init_app(app)

@app.route('/')
def index():
    return render_template('base.html')


if __name__ == '__main__':
    db_session.global_init("app/db/gym.db")
    app.run()
