
import os
from app import create_app, db
from app.models import User
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manage = Manager(app)

def make_shell_context():
    return dict(app=app, db=db, User=User)

manage.add_command('shell', Shell(make_context=make_shell_context))


@manage.command
def init_db(tablename):
    """Init the db table of tablename"""
    with app.app_context():
        _tablename = "";
        if tablename == 'Users':
            _tablename = "create_table_user.sql"
        elif tablename == 'Roles':
            _tablename = "create_table_roles.sql"
        else:
            _tablename = ""

        if _tablename != "":
            print ("init database", _tablename)
            return 
            # with app.open_resource(_tablename, mode='r') as f:
            #     db.cursor.executescripts(f.read())
            #     db.commit()  


@manage.command
def hello(name):
    """say hello to [name]"""
    print ("hello ", name)


if __name__ == '__main__':
    manage.run()