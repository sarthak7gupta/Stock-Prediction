from contextlib import contextmanager
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.engine import url
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.orm.session import Session

from config import Config
from log_helper import logging

logger = logging.getLogger("default")
sql_config = Config.SQLALCHEMY
db_uri = url.URL(**sql_config)

_autocommit = False
_autoflush = True


def get_engine(db_uri) -> Engine:
    return create_engine(db_uri)


def get_session(db_uri, autocommit, autoflush) -> Session:
    engine = get_engine(db_uri)
    Session = scoped_session(sessionmaker(bind=engine, autocommit=autocommit, autoflush=autoflush))
    return Session()


@contextmanager
def session_scope(
    db_uri=db_uri, autocommit=_autocommit, autoflush=_autoflush
) -> Generator[Session, None, None]:
    session = get_session(db_uri, autocommit, autoflush)

    try:
        yield session
        if not autocommit:
            session.commit()

    except Exception as e:
        session.rollback()
        logger.error(f"DB error {e}")
        raise e

    finally:
        session.close()


# def get_or_create(session, model, params, **kwargs):
#     instance = session.query(model).filter_by(params).first()
#     if not instance:
#         session.add(model(**kwargs))
#         session.commit()
#     return instance
