from package.migration_tool.controller.schema_controller import SchemaController
from package.migration_tool.controller.db_initialiser import DBInitialiser
from package.migration_tool.model.database import Database


def test_initialise(database: Database, schema: SchemaController):
    initialiser = DBInitialiser(schema=schema, seed_file='config/seed/simple.sql')

    # Drop schema if it exists
    if schema.exists():
        initialiser.drop()

    # Apply initialisation
    version = initialiser.run()
    assert version is None

    # Drop schema
    initialiser.drop()