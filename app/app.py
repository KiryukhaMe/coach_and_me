from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from data import db_session
from data.users import User
from data.workouts import Workout
from forms import LoginForm, RegisterForm, WorkoutForm
import datetime
from config import SECRET_KEY, SQLALCHEMY_DATABASE_URI


app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

def main():
    db_session.global_init(SQLALCHEMY_DATABASE_URI)
    app.run()

@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)

@app.route('/')
def index():
    return render_template('index.html', title='Coach and Me!')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('profile'))
        flash("Неправильный email или пароль", "danger")
        return redirect(url_for('login'))
    return render_template('login.html', title='Coach and Me! - Вход', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            flash('Пароли не совпадают', 'danger')
            return redirect(url_for('register'))
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            flash('Такой пользователь уже есть', 'danger')
            return redirect(url_for('register'))
        user = User(
            name=form.name.data,
            email=form.email.data,
            created_date=datetime.datetime.now()
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        flash('Регистрация прошла успешно!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Coach and Me! - Регистрация', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', title='Coach and Me! - Профиль')

@app.route('/workouts')
@login_required
def workouts():
    db_sess = db_session.create_session()
    workouts = db_sess.query(Workout).filter(Workout.user_id == current_user.id).all()[::-1]
    return render_template('workouts.html', title='Coach and Me! - Тренировки', workouts=workouts)

@app.route('/add_workout', methods=['GET', 'POST'])
@login_required
def add_workout():
    form = WorkoutForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        workout = Workout(
            title=form.title.data,
            description=form.description.data,
            duration=form.duration.data,
            user_id=current_user.id
        )
        db_sess.add(workout)
        db_sess.commit()
        flash('Тренировка добавлена!', 'success')
        return redirect(url_for('workouts'))
    return render_template('add_workout.html', title='Coach and Me! - Добавить тренировку', form=form)

@app.route('/edit_workout/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_workout(id):
    db_sess = db_session.create_session()
    workout = db_sess.query(Workout).filter(Workout.id == id, Workout.user_id == current_user.id).first()

    if not workout:
        flash('Тренировка не найдена', 'danger')
        return redirect(url_for('workouts'))

    form = WorkoutForm()
    if form.validate_on_submit():
        workout.title = form.title.data
        workout.description = form.description.data
        workout.duration = form.duration.data
        db_sess.commit()
        flash('Тренировка успешно обновлена!', 'success')
        return redirect(url_for('workouts'))

    elif request.method == 'GET':
        form.title.data = workout.title
        form.description.data = workout.description
        form.duration.data = workout.duration

    return render_template('edit_workout.html', title='Редактировать тренировку', form=form)

@app.route('/delete_workout/<int:id>', methods=['POST'])
@login_required
def delete_workout(id):
    db_sess = db_session.create_session()
    workout = db_sess.query(Workout).filter(Workout.id == id, Workout.user_id == current_user.id).first()

    if workout:
        db_sess.delete(workout)
        db_sess.commit()
        flash('Тренировка успешно удалена!', 'success')
    else:
        flash('Тренировка не найдена', 'danger')

    return redirect(url_for('workouts'))

if __name__ == '__main__':
    main()
