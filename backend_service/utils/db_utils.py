import sqlite3

class DatabaseUtils:

    def __init__(self, database_name='common_db.db'):
        self.database_name = database_name
    
    def fetch_data(self, query):
        '''
        For select queries. Fetches data from the database and returns as a list of rows
        '''
        with sqlite3.connect(self.database_name) as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
        return rows
    
    def update_data(self, query):
        '''
        For all table modification queries which make changes to the database
        '''
        with sqlite3.connect(self.database_name) as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()
    
