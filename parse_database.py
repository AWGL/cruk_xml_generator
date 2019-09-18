from openpyxl import load_workbook
import xlrd
from pandas import DataFrame

class ParseDatabase:

    def __init__(self, database):
        self.database_name = database

    def open_database(self):
        db_wb = xlrd.open_workbook(filename=self.database_name)
        db = db_wb.sheet_by_name("Incoming Nextera")
        return db

    def database_as_dataframe(self, db):
        db_df = DataFrame(db) #TODO
        print(db_df)
        return None

    def get_sample_data(self, db, sample):
        for row_index, dna_id in enumerate(db.col_values(colx=3)):
            if dna_id == sample:
                print(row_index)
        return None

