import re
import logging
logger = logging.getLogger("migrate.sql-file")
import os

class SQLFile:
    path = None
    statements = None

    def __init__(self, path):
        self.path = path
        content = self.load_content(self.path)
        self.statements = self.parse_content(content)

    def version_from_name(self):
        return os.path.basename(self.path).replace('.sql', '')

    @staticmethod
    def load_content(path):
        with open(path) as f:
            lines = f.readlines()

        # r"(?i)^.*interfaceOpDataFile.*$",
        # "interfaceOpDataFile %s" % fileIn,
        # line
        return "\n".join(lines)

    @staticmethod
    def parse_content(content: str):
        # Remove multiline comments
        content = re.sub(r"/\*.*?\*/", "", content, flags=re.DOTALL)
        # Remove single line comments
        content_no_comments = re.sub(r"\-\-.*?\n", "", content).strip()

        # TODO: handle cases where ";\n" appears within the query
        #       seems unlikely, it'd probably have to be escaped, like "\\n;" or something

        if len(content_no_comments) and content_no_comments[-1] == ";":
            content_no_comments = f"{content_no_comments}\n"

        raw_statements = [s for s in content_no_comments.split(";\n") if len(s.strip()) > 0]

        logger.debug(f"SQL file contains {len(raw_statements)} statements.")
        return raw_statements