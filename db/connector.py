import json
import os
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, scoped_session
from typing import Optional, List, Any


class DatabaseConnectionError(Exception):
    pass


class DBConnector:
    def __init__(self, config_path: str = 'config.json'):
        with open(config_path, 'r') as f:
            config = json.load(f)
        self.db_user = config["DB_USER"]
        self.db_password = config["DB_PASSWORD"]
        self.db_host = config["DB_HOST"]
        self.db_name = config["DB_NAME"]
        self.connection_string = f'mysql+pymysql://{self.db_user}:{self.db_password}@{self.db_host}/{self.db_name}'
        self.engine: Engine = create_engine(self.connection_string)
        self.session_factory = sessionmaker(bind=self.engine)
        self.Session = scoped_session(self.session_factory)

    def connect(self):
        try:
            self.engine.connect()
            print("Connected to the database")
        except Exception as e:
            raise DatabaseConnectionError(
                f"Failed to connect to the database: {e}")

    def disconnect(self):
        self.Session.remove()
        print("Disconnected from the database")

    def execute_query(self, query: str, params: Optional[dict] = None) -> None:
        session = self.Session()
        try:
            session.execute(text(query), params)
            session.commit()
        except Exception as e:
            session.rollback()
            raise DatabaseConnectionError(f"Query execution failed: {e}")
        finally:
            session.close()

    def fetch_query(self, query: str, params: Optional[dict] = None) -> List[Any]:
        session = self.Session()
        try:
            result = session.execute(text(query), params).fetchall()
            return [dict(row) for row in result]
        except Exception as e:
            raise DatabaseConnectionError(f"Query fetch failed: {e}")
        finally:
            session.close()
