import os
from glob import glob
from openpyxl import load_workbook
from pandas import DataFrame
from itertools import islice


class ParseReport:

    def __init__(self, worksheet_id):
        self.worksheet_id = worksheet_id


    def locate_samples(self, path_to_project):
        samples_list = next(os.walk(path_to_project))[1] #directories
        return samples_list


    def find_analysis_worksheet(self, path_to_analysis, ext):
        sample_name = os.path.basename(path_to_analysis)
        worksheet_name = glob(f"{os.path.join(path_to_analysis, '')}*{sample_name}*{ext}")
        if len(worksheet_name) > 1:
            raise Exception(f"More than one Excel file matches sample name {sample_name}. They are {worksheet_name}")
        return "".join(worksheet_name)


    def load_analysis_worksheet(self, worksheet):
        print(worksheet)
        worksheet_sample = (os.path.basename(os.path.dirname(worksheet)))
        wb = load_workbook(filename=worksheet, data_only=True)
        report_tab = wb["Report"]
        data = report_tab.values
        # Starting from column P of Excel workbook- known a priori
        cols = next(data)[15:] #TODO update these values for new app output
        data = list(data)
        idx = [r[15] for r in data]
        data_subset = (islice(r, 15, None) for r in data)
        report_df = DataFrame(data_subset, index=idx, columns=cols)
        report_sample = list(set([r[0] for r in data]))
        # Check that the data extracted from the report pertains to one sample only
        if len(report_sample) != 1:
            raise Exception(f"More than or less than one sample on worksheet for sample {worksheet_sample}")
        # check the sample numbers match on outside and inside of report file- TODO Check this naming new format
        if not worksheet_sample == report_sample[0].split("_")[-1].split("-")[-1]:
            raise Exception(f"Wrong report. File for sample name {worksheet_sample}, but report tab for sample {report_sample}")
        return report_df


    def parse_report_data(self):
        #This might be better in writeout
        return None

