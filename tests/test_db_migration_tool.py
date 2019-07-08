from src.package.migration_tool.controller.schema_controller import SchemaController
from src.package.migration_tool.controller.db_migration_tool import MigrationTool

def test_db_migration_tool(mysql_params: dict):
    mt = MigrationTool(
        host=mysql_params['host'],
        port=mysql_params['port'],
        username=mysql_params['username'],
        password=mysql_params['password'],
        schema_name='pytest',
        seed_file='config/seed/simple.sql',
        migrations='config/migrations'
    )

    if mt._schema.exists():
        mt.drop()

    mt.update(to_version='3.1.16')
    assert mt._schema.version() == '3.1.16'

    mt.update(to_version='3.1.50')
    assert mt._schema.version() == '3.1.50'