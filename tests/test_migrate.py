from model.database import Database
from controller.db_migrator import DBMigrator
from controller.db_initialiser import DBInitialiser


def test_migrate(database: Database):
    initialiaser = DBInitialiser(database, 'pytest', 'config/seed/simple.sql')
    initialiaser.run()

    migrator = DBMigrator(database, 'pytest', 'config/migrations')
    result = migrator.run_migrations()
    # assert result is True