from .schema_controller import SchemaController
from ..model.migration_file import MigrationFile
import logging
logger = logging.getLogger("migrate.db-migrator")


class DBMigrator:

    _schema: SchemaController = None

    def __init__(self, schema: SchemaController, migrations: str):
        self._schema = schema
        self._migrations = MigrationFile.discover(migrations)

    def run_migrations(self, to_version=None):
        logger.info("Checking if schema exists")
        exists = self._schema.exists()

        # Exit if schema it doesn't already exist
        if not exists:
            logger.error(f"Schema {self._schema.name()} does not exist!")
            return

        # Use schema
        self._schema.use()

        # Determine the version of the schema
        version = self._schema.version()
        logger.info(f"Version of {self._schema.name()}: {version}")

        # Apply migrations
        results = dict()
        failed = False
        for m in self._migrations:
            if (
                (not m.version.is_greater_than(version))
                or failed
                or (to_version is not None and m.version.is_greater_than(to_version))
            ):
                results[str(m.version)] = "SKIP"
                continue

            (result, error) = self.run_migration(m)
            failed = failed or not result
            results[str(m.version)] = {
                "result": "PASS" if result else "FAIL",
                "error": error
            }

        for v, result in results.items():
            logger.info(f"{v}: {result}")

        return not failed

    def run_migration(self, migration):
        logger.info(f"Applying {migration.version}")

        try:
            for s in migration.sql_file.statements:
                self._schema.execute(s)

            self._schema.set_version(migration.version)
            return True, None
        except Exception as e:
            logger.exception(f"Error running {migration.path} - ")
            return False, str(e)
