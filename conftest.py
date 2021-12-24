from shutil import copy
import pytest
from financial_app import app
from config import basedir


@pytest.fixture
def client(tmpdir):
    copy(f"{basedir}/app.db", tmpdir.dirpath())
    temp_db_file = f"sqlite:///{tmpdir.dirpath()}/app.db"
    app.config.from_object("config.TestingConfig")
    app.config["SQLALCHEMY_DATABASE_URI"] = temp_db_file

    with app.test_client() as client:
        yield client
