import pytest
from package.migration_tool.model.database import Database
from package.migration_tool.controller.schema_controller import SchemaController
import os

from package.migration_tool.controller.logging import get_logger
logger = get_logger(level='DEBUG')

@pytest.fixture(scope='session', autouse=True)
def mysql_params():
    return {
        'host': os.getenv('MYSQL_HOST', 'mysql'),
        'port': os.getenv('MYSQL_PORT', 3306),
        'username': os.getenv('MYSQL_USERNAME', 'root'),
        'password': os.getenv('MYSQL_PASSWORD', 'welcome1')
    }


@pytest.fixture(scope='session', autouse=True)
def database(mysql_params: dict):
    db = Database(
        host=mysql_params['host'],
        port=mysql_params['port'],
        username=mysql_params['username'],
        password=mysql_params['password']
    )
    assert db.connected()
    return db


@pytest.fixture(scope='session', autouse=True)
def schema(database: Database):
    return SchemaController(db=database, schema_name='pytest')