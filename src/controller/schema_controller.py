from model.database_schema import DatabaseSchema
import logging
logger = logging.getLogger("migrate.schema-controller")


class SchemaController:
    schema = None
    db = None

    def __init__(self, db, schema_name):
        self.db = db
        self.schema = DatabaseSchema(schema_name)

    def name(self):
        return self.schema.name

    def exists(self):
        logger.info(f"Checking if schema exists: {self.schema.name}")
        sql = (
            "select count(distinct schema_name) n "
            "from information_schema.schemata "
            "where schema_name = %(schema_name)s"
        )
        result = self.db.query(sql, {'schema_name': self.schema.name})
        if result[0]["n"] > 0:
            return True
        else:
            return False

    def create(self):
        logger.info(f"Creating schema: {self.schema.name}")
        self.db.execute(f"create database {self.schema.name}")

    def drop(self):
        logger.info(f"Dropping schema: {self.schema.name}")
        self.db.execute(f"drop database {self.schema.name}")

    def use(self):
        self.db.execute(f"use {self.schema.name}")

    def version(self):
        try:
            result = self.db.query('select version from schema_version limit 1')
        except Exception as e:
            logger.warning(f'Schema {self.schema.name} does not have a schema_version table - creating one')
            self.create_version_table()
            result = []

        if len(result):
            return result[0]['version']
        else:
            logger.warning(f'Schema {self.schema.name} has an empty schema_version table.')
            return None

    def create_version_table(self):
        self.db.execute(
            f"CREATE TABLE `{self.schema.name}`.`schema_version` (`version` VARCHAR(32) NOT NULL)"
        )

    def set_version(self, version):
        self.db.execute('delete from schema_version')
        self.db.execute(f'insert into schema_version (version) values ("{version}")')
        self.db.commit()
