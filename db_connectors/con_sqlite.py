import os
import sqlite3 as lite


class sqliteConnector:

    def __init__(self, database_path):
        self.database_path = database_path

    def init_database(self):
        """
        Prepares a sqlite3 database for data set storage. If the file specified in database_path doesn't exist a new
        sqlite3 database with table 'Data' will be created. Otherwise the existing database is used to store additional
        data sets.

        :return: None
        """
        table_data_exists = False
        if os.path.isfile(self.database_path):
            print("Using existing database to store results.")
        try:
            dbcon = lite.connect(self.database_path)
            dbcur = dbcon.cursor()
            dbcur.execute("SELECT Count(*) FROM Data")
            print("%s entries in this database so far." % str(dbcur.fetchone()[0]))
            table_data_exists = True
        except lite.OperationalError:
            print("[W] Table \'Data\' not found in database!")

        if not table_data_exists:   # If the database doesn't exist, we'll create it.
            print("Creating new table \'Data\' in database \'%s\' to store data!" % self.database_path)
            dbcon = lite.connect(self.database_path)
            dbcur = dbcon.cursor()
            dbcur.execute('CREATE TABLE Data (ID INTEGER PRIMARY KEY ASC, Sample text, Classification text, \
Classification_Description text)')

    def dataset_exists(self, dataset):
        """
        Check if dataset was already submitted into database.

        :param dataset: A dataset dict consisting of sample filename, sample classification and classification
                        description.
        :return:        True if the data set is already present in database, False otherwise.
        """
        # The nice thing about using the SQL DB is that I can just have it make
        # a query to make a duplicate check. This can likely be done better but
        # it's "good enough" for now.
        output = False
        con = lite.connect(self.database_path)
        cur = con.cursor()

        if not output:
            # check sample
            qstring = "SELECT * FROM Data WHERE Sample IS ?"
            cur.execute(qstring, (dataset[0],))
            if cur.fetchone() is not None:  # We should only have to pull one.
                output = True

        return output

    def insert_dataset(self, dataset):
        """
        Insert a dataset into the database.

        :param dataset: A dataset dict consisting of sample filename, sample classification and classification
                        description.
        :return:        None
        """
        # Just a simple function to write the results to the database.
        con = lite.connect(self.database_path)
        qstring = "INSERT INTO Data VALUES(NULL, ?, ?, ?)"
        with con:
            cur = con.cursor()
            cur.execute(qstring, (dataset[0], dataset[1], dataset[2]))
