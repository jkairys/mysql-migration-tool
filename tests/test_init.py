from controller.db_initialiser import DBInitialiser
from model.database import Database


def test_initialise(database: Database):
    initialiser = DBInitialiser(database=database, schema_name='pytest', seed_file='config/seed/simple.sql')

    # Drop schema if it exists
    initialiser.drop()

    # Apply initialisation
    version = initialiser.run()
    assert version is None

    # Drop schema
    initialiser.drop()