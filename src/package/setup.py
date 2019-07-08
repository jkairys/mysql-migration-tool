import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="migration_tool",
    version="0.0.1",
    author="Jethro Kairys",
    author_email="jethro.kairys@gmail.com",
    description="A database schema migration tool for MYSQL",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # url="file://",
    # url="https://github.com/jkairys/db-migration-tool",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)