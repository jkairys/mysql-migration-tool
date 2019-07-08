from package.migration_tool.model.database import Database
from package.migration_tool.controller.schema_controller import SchemaController
from package.migration_tool.controller.db_migrator import DBMigrator
from package.migration_tool.controller.db_initialiser import DBInitialiser


def test_migrate(database: Database, schema: SchemaController):
    initialiaser = DBInitialiser(schema=schema, seed_file='config/seed/simple.sql')
    initialiaser.run()

    migrator = DBMigrator(schema=schema, migrations='config/migrations')
    migrator.run_migrations(to_version='3.1.16')
    assert schema.version() == '3.1.16'

    migrator.run_migrations(to_version='3.1.50')
    assert schema.version() == '3.1.50'
    # assert result is True