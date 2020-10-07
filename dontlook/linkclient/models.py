"""Database models"""
import psycopg2
from psycopg2.extras import RealDictCursor


class DatabaseConnection:
    """Connect to the database"""
    def __init__(self):

        try:
            self.conn = psycopg2.connect(host=os.environ.get("DB_HOST"),
                                            database=os.environ.get("DB_DATABASE"),
                                            user=os.environ.get("DB_USER"),
                                            password=os.environ.get("DB_PASSWORD"),
                                            port=os.environ.get("DB_PORT"))
                                        
            self.cur = self.conn.cursor(cursor_factory=RealDictCursor)
            self.conn.autocommit = True
            print ('Database connection to successfuly created')

        except psycopg2.DatabaseError as dberror:
            print (dberror)

    def drop_tables(self):
        """drop tables if exist"""
        self.cur.execute("DROP TABLE IF EXISTS parcels, users CASCADE")

database = DatabaseConnection()
database.drop_tables()
