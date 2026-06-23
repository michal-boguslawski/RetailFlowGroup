# infrastructure/postgres/session.py
from contextlib import contextmanager
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

from infrastructure.config.settings import PostgresSettings


def create_engine_from_settings(settings: PostgresSettings | None = None) -> Engine:
    s = settings or PostgresSettings()
    engine = create_engine(
        s.url,
    )
    return engine


def create_session_factory(settings: PostgresSettings | None = None) -> sessionmaker:
    engine = create_engine_from_settings(settings)
    return sessionmaker(bind=engine, expire_on_commit=False)


@contextmanager
def get_session(factory: sessionmaker) -> Generator[Session, None, None]:
    session = factory()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
