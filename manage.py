from flask_script import Manager
from sqlalchemy import Column, String, Integer, create_engine
from flask_migrate import Migrate, MigrateCommand


from app import app
from models import db, studio, instructor

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


# custom seed command
@manager.command
def seed():
    studio(bizname='Artemis Yoga', opening_date='2018-12-12').insert()
    studio(bizname='Down Under Yoga', opening_date='2009-12-12').insert()
    studio(bizname='Cambridge Athletic Club', opening_date='2006-12-12').insert()

    instructor(name='Chris Miyachi', age=66, gender='male').insert()
    instructor(name='Kale Poland', age=50, gender='male').insert()
    instructor(name='Mari Puncel', age=32, gender='male').insert()

if __name__ == '__main__':
    manager.run()
