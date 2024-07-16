import pytest
from factory.alchemy import SQLAlchemyModelFactory
from api.v1.models import Qualification
from factory import Faker, Sequence, SubFactory, Iterator, SelfAttribute


@pytest.fixture
def qualification_factory(session):
    class QualificationFactory(SQLAlchemyModelFactory):
        class Meta:
            model = Qualification
            sqlalchemy_session = session

        qualification_id = Sequence(lambda n: n+1)
        name = Sequence(lambda n: f'name_{n}')
        created_at = Faker('date_time_this_decade')
        updated_at = Faker('date_time_this_decade')
    return QualificationFactory
