import xlrd
import pandas as pd


class ParseDatabase:

    def __init__(self, database):
        self.database_name = database

    def open_database(self, worksheet):
        db_wb = xlrd.open_workbook(filename=self.database_name)
        db = db_wb.sheet_by_name(worksheet)
        return db

    def open_database_as_dataframe(self, sheet, header=0): # Column headers are 1st row. Data starts after this.
        db_df = pd.read_excel(self.database_name, sheet_name=sheet, header=header)
        return db_df

    def create_dataframe_of_samples(self, df, samples):
        samples_search = df.loc[df['Lab ID - DNA'].isin(samples)]
        return samples_search

    def get_sample(self, df, sample):
        # Locate sample and return dataframe for that sample (only do this lookup once per sample)
        sample = df.loc[df['Lab ID - DNA'] == sample]
        return sample

    def get_cruk_sample_id(self, df):
        # return cruk sample id as a series, convert to string and take value part excluding row number
        cruk_sample_id = " ".join(df["CRUK sample ID"].to_string().split()[1:])
        return cruk_sample_id

    def get_clinical_hub(self, df):
        from valid_data import ch_dict
        # return clinical hub as a series, convert to string and take value part excluding row number
        ch = " ".join(df['Source Clinical Hub'].to_string().split()[1:])
        # Don't use get as we want a key error if value is not found as is not a clinical hub
        ch_formatted = ch_dict[ch]
        return ch_formatted

    def get_org_code(self, df):
        # return organisation code as a series, convert to string and take value part excluding row number
        org_code = " ".join(df['Hospital Org Code'].to_string().split()[1:])
        return org_code

    def get_patient_id(self, df):
        # return patient identifier as a series, convert to string and take value part excluding row number
        pat_id = " ".join(df['Local patient ID'].to_string().split()[1:])
        return pat_id

    def get_patient_id_2(self, df):
        # return second patient identifier as a series, convert to string and take value part excluding row number
        pat_id_2 = " ".join(df['Local patient ID 2'].to_string().split()[1:])
        return pat_id_2

    def get_source_sample_id(self, df):
        # return source sample identifier as a series, convert to string and take value part excluding row number
        source_id = " ".join(df['Source Sample ID'].to_string().split()[1:])
        return source_id

    def get_sample_type(self, df):
        from valid_data import st_dict
        # return sample type as a series, convert to string and take value part excluding row number
        sample_type = " ".join(df['Sample type'].to_string().split()[1:])
        # Remove spaces from key and make lowercase to make consistent then lookup
        sample_type = sample_type.replace(" ", "").lower()
        # Don't use get as we want a key error if value is not found as is not a sample type
        st_formatted = st_dict[sample_type]
        return st_formatted

    def get_tumour_type(self, df):
        from valid_data import tumour_type_dict
        # return tumour type as a series, convert to string and take value part excluding row number
        tumour_type = " ".join(df['Tumour type'].to_string().split()[1:])
        # Don't use get as we want a key error if value is not found as is not a tumour type
        tumour_type_formatted = tumour_type_dict[tumour_type]
        return tumour_type_formatted

    def get_snomed(self, df):
        snomed_code = " ".join(df['SNOMED'].to_string().split()[1:])
        if snomed_code is None or snomed_code.isspace() or len(snomed_code) == 0 or snomed_code == "NaN":
            snomed_code = "N/A"
        return snomed_code

    def get_date_sample_sent(self, df):
        # return date (without time) received as a series, convert to string and take value part excluding row number
        sent_date = df['Date sample received'].dt.date.to_string()
        # split date to remove row number
        sent_date = " ".join(sent_date.split()[1:])
        return sent_date

    def get_date_sample_received(self, df):
        # return date (without time) received as a series, convert to string and take value part excluding row number
        received_date = df['Date sample sent'].dt.date.to_string()
        # split date to remove row number
        received_date = " ".join(received_date.split()[1:])
        return received_date

    def get_lab_id(self, df):
        # return DNA identifier as a series, convert to string and take value part excluding row number
        lab_id = " ".join(df['Lab ID - DNA'].to_string().split()[1:])
        lab_id = lab_id.upper() # Handle the case where M may be entered into database as lower case m
        return lab_id

    def get_report_release_date(self, df):
        # return date (without time) received as a series, convert to string and take value part excluding row number
        try:
            release_date = df['date reported'].dt.date.to_string()
        except:
            raise Exception(f"No date reported found in Excel database or date reported in incorrect format")
        # split date to remove row number
        release_date = " ".join(release_date.split()[1:])
        return release_date

    def get_vol_banked_dna(self, df):
        # return vol of banked nucleic acid as a series, convert to string and take value part excluding row number
        vol = " ".join(df['DNA Volume (µL)'].to_string().split()[1:])
        # Where there is no concentration as no nucleic acid was banked, enter 0
        if vol == "" or vol == " " or vol == "NaN":
            vol = "0"
        return vol

    def get_conc_banked_dna(self, df):
        # return conc of banked nucleic acid as a series, convert to string and take value part excluding row number
        conc = " ".join(df['Final FFPE DNA conc for NGS'].to_string().split()[1:])
        # Where there is no concentration as no nucleic acid was banked, enter 0
        if conc == "" or conc == " " or conc == "NaN":
            conc = "0"
        return conc

    def get_vol_banked_rna(self, df):
        # return vol of banked nucleic acid as a series, convert to string and take value part excluding row number
        vol = " ".join(df['RNA Volume (µL)'].to_string().split()[1:])
        # Where there is no concentration as no nucleic acid was banked, enter 0
        if vol == "" or vol == " " or vol == "NaN":
            vol = "0"
        return vol

    def get_conc_banked_rna(self, df):
        # return conc of banked nucleic acid as a series, convert to string and take value part excluding row number
        conc = " ".join(df['Final FFPE RNA conc for NGS'].to_string().split()[1:])
        # Where there is no concentration as no nucleic acid was banked, enter 0
        if conc == "" or conc == " " or conc == "NaN":
            conc = "0"
        return conc


