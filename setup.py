from setuptools import setup, find_packages

VERSION = "0.0.4"
DESCRIPTION = "CRUD operations on nested SQLAlchemy ORM-models using Pydantic"

with open("README.md", "r") as file:
    LONG_DESCRIPTION = file.read()

# Setting up
setup(
    name="sqlalchemy-pydantic-orm",
    version=VERSION,
    url="https://github.com/Wouterkoorn/sqlalchemy-pydantic-orm",
    author="wkoorn (Wouter Koorn)",
    author_email="<wouter.koorn@student.hu.nl>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    package_dir={"": "sqlalchemy_pydantic_orm"},
    install_requires=[
        "pydantic ~= 1.8.1",
        "sqlalchemy ~= 1.4.11"
    ],
    extra_require={
        "dev": [
            "pytest >= 6.2.3",
            "pdoc3 >= 0.9.2",
            # "mypy >= 0.812"
        ]
    },
    keywords=[
        "python", "pydantic", "sqlalchemy", "ORM", "nested", "nesting", "CRUD"
    ],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: The Unlicense (Unlicense)",
        "Natural Language :: English",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Database",
        "Topic :: Database :: Database Engines/Servers",
        "Topic :: Software Development :: Version Control :: Git",
        "Topic :: Software Development :: Testing :: Unit",
        "Typing :: Typed",
    ]
)
