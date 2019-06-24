import pytest
from model.database import Database
import os

from controller.logging import get_logger
logger = get_logger(level='DEBUG')

@pytest.fixture(scope='session', autouse=True)
def database():
    os.getenv('MYSQL_HOST', 'mysql')
    os.getenv('MYSQL_PORT', 3306)
    os.getenv('MYSQL_USERNAME', 'root')
    os.getenv('MYSQL_PASSWORD', 'welcome1')
    return Database(
        host=os.getenv('MYSQL_HOST', 'mysql'),
        port=os.getenv('MYSQL_PORT', 3306),
        username=os.getenv('MYSQL_USERNAME', 'root'),
        password=os.getenv('MYSQL_PASSWORD', 'welcome1')
    )