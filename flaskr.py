import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash

app = Flask(__name__)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path,'flaskr.db'),
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
    )
)
app.config.from_envvar('FLASK_SETTINGS', silent = True)


def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql',mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
    pass


@app.cli.command('initdb')
def initdb_command():
    init_db()
    print ('Ininitate the database')


def get_db():
    if not hasattr(g,'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    if hasattr(g,'sqlite_db'):
        g.sqlite_db.close()


@app.route('/')
def show_entries():
    db = get_db()
    cur = db.execute("select title,text from entries order by id desc")
    entries = cur.fetchall()
    return render_template('show_entries.html',entries=entries)


@app.route('/add', methods = ['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    db.execute('insert into entries (title, text) values (?,?)',[request.form['title'], request.form['text']])
    db.commit()
    flash('New entry successfully be posted')
    return redirect(url_for('show_entries'))


@app.route('/login', methods = ['POST','GET'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] == app.config['USERNAME'] and request.form['password'] == app.config['PASSWORD']:
            session['logged_in'] = True
            flash('you are successfully logged in')
            return redirect(url_for('show_entries'))
        else:
            error = 'Invalid username or password!'
    return render_template('login.html',error = error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('you are successfully logged out')
    return render_template('show_entries.html')


if __name__ == '__main__':
    app.run()