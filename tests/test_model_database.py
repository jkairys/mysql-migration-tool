from package.migration_tool.model.database import Database


def test_connect(database: Database):
    assert database.connected() is True