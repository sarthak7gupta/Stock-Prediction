from os import makedirs

from sqlalchemy_utils import create_database, database_exists

from config import Config
from database.Model import Base
from db_helper import db_uri, get_engine
from log_helper import logging

paths = Config.PATHS
logger = logging.getLogger("default")

if __name__ == "__main__":
    logger.info("Starting Setup")

    for set_key, paths_set in paths.items():
        for path in paths_set.values():
            logger.info(f"Creating {path}")
            makedirs(path, exist_ok=True)

    try:
        engine = get_engine(db_uri)
        if not database_exists(db_uri):
            logger.info("Creating Database")
            create_database(db_uri)

        else:
            logger.info("Database exists")

        logger.info("Creating DB tables.")
        Base.metadata.create_all(engine)

    except Exception as e:
        logger.error(f"Couldn't create DB tables. {e}")

    logger.info("Finished Setup")
