"""Database models"""
import os
import psycopg2
from psycopg2.extras import RealDictCursor
import logging


logger = logging.getLogger(__name__)


class MayanDatabaseConnection:
    """Connect to the database"""
    def __init__(self):

        try:
            self.conn = psycopg2.connect(host=os.environ.get("MAYAN_DB_HOST"),
                                            database=os.environ.get("MAYAN_DB_NAME"),
                                            user=os.environ.get("MAYAN_DB_USER"),
                                            password=os.environ.get("MAYAN_DB_PASSWORD"),
                                            port=os.environ.get("MAYAN_DB_PORT"))
                                        
            self.cur = self.conn.cursor(cursor_factory=RealDictCursor)
            self.conn.autocommit = True
            logger.info('Mayan Database connection successfuly created')

        except psycopg2.DatabaseError as dberror:
            logger.critical(dberror)

    # def drop_tables(self):
    #     """drop tables if exist"""
    #     self.cur.execute("DROP TABLE IF EXISTS parcels, users CASCADE")

# database = DatabaseConnection()
# database.drop_tables()
