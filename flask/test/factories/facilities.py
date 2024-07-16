import pytest
from factory.alchemy import SQLAlchemyModelFactory
from factory import Faker, Sequence, SubFactory, Iterator, SelfAttribute
from api.v1.models import Facility
import factory


@pytest.fixture
def facility_factory(session):
    class FacilityFactory(SQLAlchemyModelFactory):
        class Meta:
            model = Facility
            sqlalchemy_session = session

        facility_id = Sequence(lambda n: n+1)
        name = Sequence(lambda n: f'name_{n}')
        created_at = Faker('date_time_this_decade')
        updated_at = Faker('date_time_this_decade')
    return FacilityFactory
