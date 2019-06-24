from model.database import Database
from controller.schema_controller import SchemaController
import logging
from model.sql_file import SQLFile
logger = logging.getLogger("migrate.db-initialise")


class DBInitialiser:
    _database = None

    def __init__(self, database: Database, schema_name, seed_file):
        self._database = database
        self._schema = SchemaController(db=database, schema_name=schema_name)
        self._seed_file = seed_file

    def run(self):
        logger.info(f"Checking if schema exists '{self._schema.name()}'")
        exists = self._schema.exists()

        # Create schema if it doesn't already exist
        if not exists:
            logger.info(f"Schema does not exist - initialising '{self._schema.name()}' from seed {self._seed_file}")
            self._schema.create()
        else:
            logger.info(f"Schema '{self._schema.name()}' already exists")
            return

        # Use schema
        self._schema.use()

        # load the seed file
        sql_file = SQLFile(self._seed_file)

        logger.info(f"Executing {len(sql_file.statements)} statements in seed file")
        for s in sql_file.statements:
            self._database.execute(s)

        self._database.commit()

        logger.info("Seed file execution complete.")

        # Determine the version of the schema
        version = self._schema.version()
        logger.info(f"Deployed schema '{self._schema.name()}' is currently at version '{version}'")

        return version


    # drop existing schema
    def drop(self):
        logger.warning(f"Dropping schema '{self._schema.name()}'")
        self._schema.drop()
        self._database.commit()