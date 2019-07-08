from .db_initialiser import DBInitialiser
from .db_migrator import DBMigrator
from .schema_controller import SchemaController
from ..model.database import Database


class MigrationTool:
    _migrator = None
    _initialiser = None
    _database = None
    _schema = None
    # _db_host = None
    # _db_port = None
    # _db_username = None
    # _db_password = None
    # _db_schema = None

    def __init__(self, host, port, username, password, schema_name, seed_file, migrations):
        # self._db_host = host
        # self._db_port = port
        # self._db_username = username
        # self._db_password = password
        # self._db_schema = schema
        self._database = Database(
            host=host,
            port=port,
            username=username,
            password=password,
        )

        self._schema = SchemaController(db=self._database, schema_name=schema_name)

        self._initialiser = DBInitialiser(
            schema=self._schema,
            seed_file=seed_file
        )

        self._migrator = DBMigrator(
            schema=self._schema,
            migrations=migrations
        )

    def schema_exists(self):
        return self._schema.exists()

    def drop(self):
        self._schema.drop()

    def update(self, to_version=None):
        self._initialiser.run()
        self._migrator.run_migrations(to_version)