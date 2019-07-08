from ..model.sql_file import SQLFile
from .schema_controller import SchemaController
import logging
logger = logging.getLogger("migrate.db-initialise")


class DBInitialiser:
    _schema: SchemaController = None

    def __init__(self, schema: SchemaController, seed_file):
        self._schema = schema
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
            self._schema.execute(s)

        self._schema.commit()

        logger.info("Seed file execution complete.")

        # Determine the version of the schema
        version = self._schema.version()

        if version is None:
            initial_version = sql_file.version_from_name()
            logger.info(f'Setting initial version to {initial_version} based on seed file name')
            self._schema.set_version(initial_version)
            # get updated version from db
            version = self._schema.version()

        logger.info(f"Deployed schema '{self._schema.name()}' is currently at version '{version}'")

        return version

    # drop existing schema
    def drop(self):
        logger.warning(f"Dropping schema '{self._schema.name()}'")
        self._schema.drop()
        self._schema.commit()