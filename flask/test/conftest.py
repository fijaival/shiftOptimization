import os
import pytest
from api import create_app
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from contextlib import contextmanager
from extensions import Base
from pytest_sqlalchemy_mock.base import *
from dotenv import load_dotenv

load_dotenv('.env.test', override=True)


@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })

    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


@pytest.fixture(scope="session")
def engine():
    TEST_DATABASE_URL = 'mysql+pymysql://{user}:{password}@{host}:{PORT}/{db_name}?charset=utf8'.format(**{
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'host':     os.getenv('DB_HOST'),
        'PORT':    os.getenv('DB_PORT'),
        'db_name': os.getenv('DB_NAME'),
    })
    print(TEST_DATABASE_URL)
    return create_engine(TEST_DATABASE_URL)


@pytest.fixture(scope="session")
def connection(engine):
    connection = engine.connect()
    yield connection
    connection.close()


@pytest.fixture(scope="session")
def setup_db(connection):
    Base.metadata.create_all(bind=connection)
    yield
    Base.metadata.drop_all(bind=connection)


@pytest.fixture(scope="function")
def session(connection, setup_db):
    session_factory = sessionmaker(bind=connection)
    Session = scoped_session(session_factory)
    session = Session()

    yield session

    session.close()


@contextmanager
def mock_session_scope(session):
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e


def pytest_runtest_setup(item):
    small_only = item.config.getoption('--small-only', default=False)
    small = item.get_closest_marker('small')

    if small_only and not small:
        pytest.skip('Skip medium/large test')


@pytest.fixture(scope="function")
def sqlalchemy_declarative_base():
    return Base


@pytest.fixture(scope="function")
def sqlalchemy_mock_config():
    return [("constraints", [
        {
            "constraint_id": 12,
            "name": "Constraint_1"
        },
        {
            "constraint_id": 22,
            "name": "Constraint_2"
        }
    ]),
        ("facilities", [
            {"facility_id": 1,
             "name": "facility_1"},
            {"facility_id": 2,
             "name": "facility_2"}
        ])]
