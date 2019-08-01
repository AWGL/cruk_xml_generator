import os
from glob import glob
from openpyxl import load_workbook
from pandas import DataFrame
from itertools import islice

path = "/Users/sararey/Documents/cruk_reporting" #temp path for testing
worksheet_id = "19-5037" #temp for testing- obtain from ?- entry by scientist?


def locate_samples(path_to_project):
    samples_list = next(os.walk(path_to_project))[1] #directories
    return samples_list


def find_analysis_worksheet(path_to_analysis, ext):
    sample_name = os.path.basename(path_to_analysis)
    worksheet_name = glob(f"{os.path.join(path_to_analysis, '')}*{sample_name}*{ext}")
    return "".join(worksheet_name)


def load_analysis_worksheet(worksheet):
    print(worksheet)
    worksheet_sample = (os.path.basename(os.path.dirname(worksheet)))
    wb = load_workbook(filename=worksheet, data_only=True)
    report_tab = wb["Report"]
    data = report_tab.values
    cols = next(data)[15:] # Starting from column P of Excel workbook
    data = list(data)
    idx = [r[15] for r in data]
    data_subset = (islice(r, 15, None) for r in data)
    report_df = DataFrame(data_subset, index=idx, columns=cols)
    report_sample = list(set([r[0] for r in data]))
    if len(report_sample) != 1:
        raise Exception(f"More than or less than one sample on worksheet for sample {worksheet_sample}")
    if not check_correct_report(worksheet_sample, report_sample[0]):
        raise Exception(f"Wrong report. File for sample name {worksheet_sample}, but report tab for sample {report_sample}")
    return report_df


def check_correct_report(ws, rp):
    #Comp sample names from file and inside report tab
    return ws == rp.split("-")[-1]


def parse_report_data():
    #This might be better in writeout
    return None



def main():
    samples = locate_samples(os.path.join(path, worksheet_id))
    report = find_analysis_worksheet(os.path.join(path, worksheet_id, samples[0]), ".xlsx") # test for one sample initially
    load_analysis_worksheet(report)


if __name__ == '__main__':
    main()