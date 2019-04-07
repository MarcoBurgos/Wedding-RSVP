import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from weddingRegistry import app, db

MIGRATION_DIR = os.path.join('weddingRegistry', 'migrations')

app.config.from_object(os.environ['APP_SETTINGS'])

migrate = Migrate(app, db, directory=MIGRATION_DIR)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
