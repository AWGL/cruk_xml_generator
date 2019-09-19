from openpyxl import load_workbook
import xlrd
import pandas as pd
from pandas import DataFrame

class ParseDatabase:

    def __init__(self, database):
        self.database_name = database

    def open_database(self):
        db_wb = xlrd.open_workbook(filename=self.database_name)
        db = db_wb.sheet_by_name("Incoming Nextera")
        return db

    def open_database_as_dataframe(self):
        db_df = pd.read_excel(self.database_name, header=2) # Column headers are 3rd row. Data starts after this.
        return db_df

    def create_dataframe_of_samples(self, df, samples):
        samples_search = df.loc[df['FFPE DNA Number'].isin(samples)]
        return samples_search

    def get_sample(self, df, sample):
        # Locate sample and return dataframe for that sample (only do this lookup once per sample)
        sample = df.loc[df['FFPE DNA Number'] == sample]
        return sample

    def get_clinical_hub(self, sample_df):
        from valid_data import ch_dict
        # return clinical hub as a series, convert to string and take value part excluding row number
        ch = sample_df["CH"].to_string().split()[1]
        # Don't use get as we want a key error if value is not found as is not a clinical hub
        ch_formatted = ch_dict[ch]
        return ch_formatted

    def get_patient_id(self, sample_df):
        pat_id = sample_df["Forename"].to_string().split()[1]
        return pat_id

    def get_source_sample_id(self, sample_df):
        source_id = sample_df["Surname-Now block ID"].to_string().split()[1]
        return source_id

    def get_sample_type(self, sample_df):
        sample_type = sample_df["Sample type"].to_string().split()[1]
        return sample_type

    def index_samples_df(self, df):
        return df.set_index('FFPE DNA Number')

    def get_sample_data_old(self, db, sample):
        for row_index, dna_id in enumerate(db.col_values(colx=3)):
            if dna_id == sample:
                print(row_index)
        return None

