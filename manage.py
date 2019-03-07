from app import create_app,db
from flask_script import Manager,Server
from app.models import  Role, User, Comment, Disease, Agronomist, User_diseases
from  flask_migrate import Migrate, MigrateCommand
# Creating app instance
app = create_app('development')

manager = Manager(app)
manager.add_command('server',Server)
migrate = Migrate(app,db)
manager.add_command('db',MigrateCommand)

@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

@manager.shell
def make_shell_context():
    return dict(app = app,db = db,User = User, Role = Role, Comment = Comment, Disease = Disease, Agronomist=Agronomist, User_diseases=User_diseases )

   

if __name__ == '__main__':
    manager.run()