import xlrd
import pandas as pd

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
        ch = " ".join(sample_df['CH'].to_string().split()[1:])
        # Don't use get as we want a key error if value is not found as is not a clinical hub
        ch_formatted = ch_dict[ch]
        return ch_formatted

    def get_patient_id(self, sample_df):
        # return patient identifier as a series, convert to string and take value part excluding row number
        pat_id = " ".join(sample_df['Forename'].to_string().split()[1:])
        return pat_id

    def get_source_sample_id(self, sample_df):
        # return source sample identifier as a series, convert to string and take value part excluding row number
        source_id = " ".join(sample_df['Surname-Now block ID'].to_string().split()[1:])
        return source_id

    def get_sample_type(self, sample_df):
        from valid_data import st_dict
        # return sample type as a series, convert to string and take value part excluding row number
        # Excel sheet formatted oddly- should be Sample type
        sample_type = " ".join(sample_df['Unnamed: 15'].to_string().split()[1:])
        # Remove spaces from key and make lowercase to make consistent then lookup
        sample_type = sample_type.replace(" ", "").lower()
        # Don't use get as we want a key error if value is not found as is not a clinical hub
        st_formatted = st_dict[sample_type]
        return st_formatted

    def get_date_sample_received(self, sample_df):
        # return date (without time) received as a series, convert to string and take value part excluding row number
        received_date = sample_df['Date received (put date of last sample from blood/FFPE)'].dt.date.to_string()
        # split date to remove row number
        received_date = " ".join(received_date.split()[1:])
        return received_date

    def get_lab_id(self, sample_df):
        # return DNA identifier as a series, convert to string and take value part excluding row number
        lab_id = " ".join(sample_df['FFPE DNA Number'].to_string().split()[1:])
        return lab_id

    def get_conc_banked(self, sample_df):
        # return conc of banked nucleic acid as a series, convert to string and take value part excluding row number
        conc = " ".join(sample_df['Final FFPE conc for NGS'].to_string().split()[1:])
        # Where there is no concentration as no nucleic acid was banked, enter 0
        if conc == "" or conc == " ":
            conc = 0
        return conc






    # Legacy functions
    def index_samples_df(self, df):
        return df.set_index('FFPE DNA Number')

    def get_sample_data_old(self, db, sample):
        for row_index, dna_id in enumerate(db.col_values(colx=3)):
            if dna_id == sample:
                print(row_index)
        return None

