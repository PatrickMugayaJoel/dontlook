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

    def clear_test_tables(self, metatype_id, document_id):
        if os.environ.get("MAYAN_DATABASE_DB") == "test":
            try:
                self.cur.execute(f"DELETE FROM metadata_documentmetadata WHERE metadata_type_id={int(metatype_id)} AND document_id={int(document_id)}")
                self.cur.execute("TRUNCATE TABLE cabinets_cabinet RESTART IDENTITY CASCADE")
                return True
            except Exception as ex:
                print(f"clear_test_tables SQL query failed.")
                print_a_log(ex)

    def insert_metadata(self, data):

        try:
            self.cur.execute(
                f"""
                INSERT INTO metadata_documentmetadata (value, document_id, metadata_type_id)
                VALUES ('{data["value"]}', {data["document_id"]}, {data["metatype_id"]});
                """
            )
            return True
        except Exception as ex:
            print_a_log(ex)

    def update_metadata(self, data):

        try:
            self.cur.execute(
                f"""
                UPDATE metadata_documentmetadata
                SET value = '{data["value"]}'
                WHERE document_id = {data["document_id"]}
                AND metadata_type_id = {data["metatype_id"]}
                """
            )
            print("Query finished well: ", os.environ.get("MAYAN_DB_HOST"), os.environ.get("MAYAN_DATABASE_DB"))
            return True
        except Exception as ex:
            print_a_log(ex)

    def get_cabinet_by_label(self, label):

        try:
            self.cur.execute(
                f"""
                SELECT * FROM public.cabinets_cabinet WHERE label='{label}';
                """
            )
            return self.cur.fetchone()
        except Exception as ex:
            print(f"get_cabinet_by_label SQL query failed. label => {label}")
            print_a_log(ex)

    def get_metatype_by_name(self, name):

        try:
            self.cur.execute(
                f"""
                SELECT * FROM metadata_metadatatype WHERE name='{name}';
                """
            )
            return self.cur.fetchone()
        except Exception as ex:
            print(f"get_metatype_by_name SQL query failed.")
            print_a_log(ex)

    def check_added_metadata(self, metatype_id, document_id):
        if os.environ.get("MAYAN_DATABASE_DB") == "test":
            try:
                self.cur.execute(f"SELECT * FROM metadata_documentmetadata WHERE metadata_type_id={int(metatype_id)} AND document_id={int(document_id)}")
                return self.cur.fetchall()
            except Exception as ex:
                print(f"check_added_metadata SQL query failed.")
                print_a_log(ex)
