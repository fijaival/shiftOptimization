from .error import InvalidAPIUsage
from sqlalchemy.exc import IntegrityError
from extensions import db_session
from contextlib import contextmanager


@contextmanager
def session_scope():
    session = db_session()
    try:
        yield session  # with asでsessionを渡す
        session.commit()
    except IntegrityError as e:
        print(e)
        print("-------")
        print(e.orig)
        session.rollback()
        if 'Duplicate' in str(e.orig):
            raise InvalidAPIUsage("An error ocurred due to duplicate data", 400)
        elif 'cannot be null' in str(e.orig):
            raise InvalidAPIUsage("An error occurred due to foreign key constraints", 400)
        elif 'foreign key constraint' in str(e.orig):
            raise InvalidAPIUsage("An error occurred due to foreign key constraints", 400)
        else:
            raise InvalidAPIUsage("An error occurred while saving the instance", 500)
    except Exception as e:
        message = "An error occurred while saving the instance"
        if e.args:
            message = e.args[0]
        print(message)
        session.rollback()
        raise InvalidAPIUsage(message, 500)
    finally:
        session.close()
