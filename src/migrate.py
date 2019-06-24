#!/usr/bin/env python3
import sys
from controller.logging import get_logger
logger = get_logger('migrate')


import click

from model.database import Database
from controller.db_initialiser import DBInitialiser
from controller.db_migrator import DBMigrator


@click.group()
@click.option('--db-host', default="localhost", help='Database server hostname')
@click.option('--db-port', default=3306, help='Database server port')
@click.option('--db-password', default=None, help='Database server password')
@click.option('--db-username', default="root", help='Database server username')
@click.pass_context
def cli(ctx, db_host, db_port, db_password, db_username):
    try:
        logger.info(f"Connecting to mysql database {db_username}@{db_host}:{db_port}")
        db = Database(host=db_host, port=db_port, username=db_username, password=db_password)
        logger.info("Connected to database successfully.")
        ctx.obj = db
    except Exception as e:
        click.echo("Unable to connect to the database")
        click.echo(e)
        sys.exit(1)

@click.command()
@click.option('--schema-name', default=None, help='Target schema name')
@click.option('--seed-file', default=None, help='Path to seed file')
@click.option('--drop', is_flag=True, default=False)
@click.pass_obj
def init(db, schema_name, seed_file, drop):

    if schema_name is None:
        logger.error("--schema-name is required")
        sys.exit(1)
    if seed_file is None:
        logger.error("--seed-file is required")
        sys.exit(1)

    initialiser = DBInitialiser(db, schema_name, seed_file)

    if drop:
        initialiser.drop()

    initialiser.run()

@click.command()
@click.option('--schema-name', default=None, help='Target schema name')
@click.option('--migrations', default=None, help='Path to migrations files')
@click.pass_obj
def migrate(db, schema_name, migrations):
    if schema_name is None:
        logger.error("--schema-name is required")
        sys.exit(1)

    if migrations is None:
        logger.error("--migrations is required")
        sys.exit(1)

    migrator = DBMigrator(db, schema_name, migrations)
    result = migrator.run_migrations()
    sys.exit(0 if result else 1)

@click.command()
def drop():
    click.echo('Dropping the database')

cli.add_command(init)
cli.add_command(drop)
cli.add_command(migrate)


if __name__ == '__main__':
    cli()
