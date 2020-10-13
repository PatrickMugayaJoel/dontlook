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
                                            database=os.environ.get("MAYAN_DATABASE_DB"),
                                            user=os.environ.get("MAYAN_DATABASE_USER"),
                                            password=os.environ.get("MAYAN_DATABASE_PASSWORD"),
                                            port=os.environ.get("MAYAN_DB_PORT"))
                                        
            self.cur = self.conn.cursor(cursor_factory=RealDictCursor)
            self.conn.autocommit = True
            logger.info('Mayan Database connection successfuly created')

        except psycopg2.DatabaseError as dberror:
            logger.critical(dberror)

    def get_doc_id_by_policy_no(self, policy_number):

        try:
            self.cur.execute(
                f"""
                SELECT document_id FROM metadata_documentmetadata WHERE value='{policy_number}';
                """
            )
            return self.cur.fetchone()
        except Exception as ex:
            print(f"\nError: {ex}")
            logger.critical(f'\n\n{ex}\n\n')

    def insert_metadata_by_policy_no(self, data):

        try:
            self.cur.execute(
                f"""
                INSERT INTO metadata_documentmetadata (value, document_id, metadata_type_id)
                VALUES ('{data["client_id"]}', {data["document_id"]}, {data["metatype_id"]});
                """
            )
            return True
        except Exception as ex:
            print(f"\nError: {ex}")
            logger.critical(f'\n\n{ex}\n\n')
