"""Database models"""
import os
import psycopg2
import logging
from psycopg2.extras import RealDictCursor


logger = logging.getLogger(__name__)

def print_a_log(msg):
	print(f"\nError: {msg}")
	logger.critical(f'\n\n{msg}\n\n')

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
            logger.info('Mayan Database connection successfully created')

        except psycopg2.DatabaseError as dberror:
            print_a_log(dberror)

    def get_doc_id_by_policy_no(self, policy_number):

        try:
            self.cur.execute(
                f"""
                SELECT document_id FROM metadata_documentmetadata WHERE value='{policy_number}';
                """
            )
            return self.cur.fetchone()
        except Exception as ex:
            print_a_log(ex)

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
            print_a_log(ex)

    def get_cabinet_by_label(self, label):

        print(f"labeling: {label}")
        try:
            self.cur.execute(
                f"""
                SELECT * FROM public.cabinets_cabinet WHERE label='{label}';
                """
            )
            return self.cur.fetchone()
        except Exception as ex:
            print(f"failing: {label}")
            print_a_log(ex)
