import pytest
from factory.alchemy import SQLAlchemyModelFactory
from api.v1.models import Constraint
from factory import Faker, Sequence, SubFactory, Iterator, SelfAttribute


@pytest.fixture
def constraint_factory(session):
    class ConstraintFactory(SQLAlchemyModelFactory):
        class Meta:
            model = Constraint
            sqlalchemy_session = session

        constraint_id = Sequence(lambda n: n+1)
        name = Sequence(lambda n: f'name_{n}')
        created_at = Faker('date_time_this_decade')
        updated_at = Faker('date_time_this_decade')
    return ConstraintFactory
