from setuptools import setup, find_packages

VERSION = "0.0.1"
DESCRIPTION = "CRUD operations on nested SQLAlchemy ORM models using Pydantic"
LONG_DESCRIPTION = "TODO"

# Setting up
setup(
    name="sqlalchemy-pydantic-orm",
    version=VERSION,
    author="wkoorn (Wouter Koorn)",
    author_email="<wouter.koorn@student.hu.nl>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=["pydantic", "sqlalchemy"],
    keywords=[
        "python", "pydantic", "sqlalchemy", "ORM", "nested", "nesting", "CRUD"
    ],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
