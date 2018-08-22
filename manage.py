import os
from dotenv import load_dotenv, find_dotenv
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import db, create_app
from app.models.user import User
from app.models.ride import Ride
from app.models.request import Request
from app.models.rate import Rate

load_dotenv(find_dotenv())

config_name = os.environ.get('DEV_ENVIRON')
app = create_app(config_name)
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
