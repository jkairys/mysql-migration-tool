import os
import glob
import logging
from model.sql_file import SQLFile
import functools

logger = logging.getLogger('migrate.migration-file')


class SemVer:
    major: int = None
    minor: int = None
    patch: int = None

    def __init__(self, major, minor, patch):
        self.major = int(major)
        self.minor = int(minor)
        self.patch = int(patch)

    @classmethod
    def from_string(cls, v):
        components = v.split(".")
        if len(components) != 3:
            raise ValueError(f"Invalid semantic version {v}")
        try:
            major = int(components[0])
            minor = int(components[1])
            patch = int(components[2])
        except Exception as e:
            raise ValueError(f"Invalid semantic version {v}")

        return cls(major, minor, patch)

    def __repr__(self):
        return f"{self.major}.{self.minor}.{self.patch}"

    def is_greater_than(self, other):

        if other is None:
            return True

        if type(other) is str:
            other = SemVer.from_string(other)

        # self.major must be >= other.major
        if self.major > other.major:
            return True

        # self.minor must be >= other.minor
        if self.major == other.major and self.minor > other.minor:
            return True

        # self.patch must be > other.patch
        if self.major == other.major and self.minor == other.minor and self.patch > other.patch:
            return True

        return False


class MigrationFile:
    path = None
    version = None

    def __init__(self, path):
        self.path = path
        self.version = self.get_version_from_path(path)
        self.sql_file = SQLFile(path)

    @staticmethod
    def get_version_from_path(path):
        base = os.path.basename(path)
        components = os.path.basename(path).replace(".sql", "").split(".")
        if len(components) != 3:
            logger.warning(f"{os.path.realpath(path)} has an invalid filename for a migration - ignoring this file.")
            return None
        return SemVer(components[0], components[1], components[2])


    @staticmethod
    def discover(path):
        if path[:-1] == "/" and len(path) > 1:
            path = path[:-1]
        # files = os.listdir(path)
        logger.info(f'Looking for migration files in {path}')
        files = glob.glob(f"{path}/*.sql")
        all_migrations = [MigrationFile(f) for f in files]
        valid_migrations = [f for f in all_migrations if f.version is not None]
        logger.info(f'Found {len(valid_migrations)} valid migration files')

        # now we need to sort them
        valid_migrations = sorted(valid_migrations, key=functools.cmp_to_key(lambda x, y: 1 if x.version.is_greater_than(y.version) else -1), reverse=False)

        return valid_migrations
