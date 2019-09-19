import os
from glob import glob
from openpyxl import load_workbook
from pandas import DataFrame
from itertools import islice


class ParseReport:

    def __init__(self, worksheet_id):
        self.worksheet_id = worksheet_id


    def find_analysis_worksheet(self, path_to_analysis, ext):
        sample_name = os.path.basename(path_to_analysis)
        worksheet_name = glob(f"{os.path.join(path_to_analysis, '')}*{sample_name}*{ext}")
        if len(worksheet_name) > 1:
            raise Exception(f"More than one Excel file matches sample name {sample_name}. They are {worksheet_name}")
        return "".join(worksheet_name)

    def load_analysis_worksheet(self, worksheet):
        worksheet_sample = (os.path.basename(os.path.dirname(worksheet)))
        wb = load_workbook(filename=worksheet, data_only=True)
        report_tab = wb["Report"]
        data = report_tab.values
        data = list(data)
        report_samples = [r[0] for r in data]
        # Ensure that the formulae in the Excel spreadsheet have been evaluated by checking that the sample identifiers
        # are not all None
        if not any(report_samples):
            raise Exception(f"Formulae have not been evaluated. Open and save worksheet in Excel.")
        # Check the sample numbers match on outside and inside of report file
        # First entry is DNA sample, second is RNA sample. Naming pattern is projectid-sampleid.
        if not worksheet_sample == report_samples[1].split("-")[-1]:
            raise Exception(f"Wrong report. File for DNA sample name {worksheet_sample}, but report tab for \
                DNA sample {report_samples}")
        return wb

    def report_table(self, wb):
        report_tab = wb["Report"]
        data = report_tab.values
        # Starting from column D (4) of Excel workbook- known a priori
        cols = next(data)[4:]
        data = list(data)
        idx = [r[4] for r in data]
        data_subset = (islice(r, 4, None) for r in data)
        report_df = DataFrame(data_subset, index=idx, columns=cols)
        return (report_df)

    def report_samples(self, wb):
        report_tab = wb["Report"]
        data = report_tab.values
        data = list(data)
        report_samples = [r[0] for r in data]
        # Remove None values from list of samples analysed on this report
        report_samples = list(filter(None, report_samples))
        # Remove header 'LABNO'
        return report_samples[1:]

    def get_genes(self, df):
        genes = df['GENE']
        return genes

    def parse_report_data(self):
        #This might be better in writeout
        return None

