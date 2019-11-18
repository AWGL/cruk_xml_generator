import os
from glob import glob
from openpyxl import load_workbook
from pandas import DataFrame
from itertools import islice


def find_analysis_worksheet(path_to_analysis, ext):
    sample_name = os.path.basename(path_to_analysis)
    if not os.path.exists(path_to_analysis):
        raise Exception(f"Path {path_to_analysis} not found. Check worksheet id is correct")
    # Use ~ to exclude the temporary file created when an Excel file is open
    worksheet_name = glob(f"{os.path.join(path_to_analysis, '')}[!^~]*{sample_name}*{ext}")
    if len(worksheet_name) > 1:
        raise Exception(f"More than one Excel file matches sample name {sample_name}. They are {worksheet_name}")
    return "".join(worksheet_name)


def load_analysis_worksheet(worksheet):
    worksheet_sample = (os.path.basename(os.path.dirname(worksheet)))
    wb = load_workbook(filename=worksheet, data_only=True)
    report_tab = wb["Report"]
    data = report_tab.values
    data = list(data)
    report_samples = [r[0] for r in data]
    # Ensure that the formulae in the Excel spreadsheet have been evaluated by checking that the sample identifiers
    # are not all None
    if not any(report_samples):
        raise Exception(f" Excel formulae have not been evaluated. Open and save worksheet in Excel.")
    # Check the sample numbers match on outside and inside of report file
    # First entry is DNA sample, second is RNA sample. Naming pattern is projectid-sampleid.
    if not worksheet_sample == report_samples[1].split("-")[-1]:
        raise Exception(f"Wrong report. File for DNA sample name {worksheet_sample}, but report tab for "
                        f"DNA sample {report_samples[1]}")
    return wb


def report_table(wb):
    report_tab = wb["Report"]
    data = report_tab.values
    # Starting from column D (4) of Excel workbook- known a priori
    cols = next(data)[4:]
    data = list(data)
    idx = [r[4] for r in data]
    data_subset = (islice(r, 4, None) for r in data)
    report_df = DataFrame(data_subset, index=idx, columns=cols)
    return report_df


def checker_table(wb):
    checker_tab = wb["Patient Summary"]
    data = checker_tab.values
    patient_df = DataFrame(data)
    return patient_df


def get_first_checker(df):
    first_checker = df.iloc[3][5]
    return first_checker


def get_second_checker(df):
    second_checker = df.iloc[4][5]
    return second_checker


def report_samples(wb):
    report_tab = wb["Report"]
    data = report_tab.values
    data = list(data)
    report_samples = [r[0] for r in data]
    # Remove None values from list of samples analysed on this report
    report_samples = list(filter(None, report_samples))
    # Remove header 'LABNO'
    return report_samples[1:]


def get_genes(df):
    genes = df['GENE']
    return genes


def get_gene_number(gene):
    from valid_data import genes_dict
    gene_num = genes_dict.get(gene)
    return gene_num


def get_gene_data(gene, df):
    gene_data = df.loc[gene]
    return gene_data


def get_test_scope(gene_data):
    test_scope = gene_data.get("SCOPE")
    return test_scope


def get_test_result(gene_data):
    test_result = gene_data.get("RESULT")
    return test_result


def get_test_report(gene_data):
    test_report = gene_data.get("REPORT")
    return test_report


def get_test_status(gene_data):
    from valid_data import test_status_dict
    test_status = None
    gene_status = gene_data.get("STATUS")
    if gene_status == "Success":
        test_status = test_status_dict.get("Success")
    if gene_status == "Failure":
        test_status = test_status_dict.get("Complete Fail")
    return test_status


def get_comments(gene_data):
    comment = gene_data.get("COMMENT")
    if comment is None or comment.isspace() or len(comment) == 0 or comment == "NaN":
        comments = "These results are intended for research purposes."
    else:
        comments = f"These results are intended for research purposes. {comment}."
    return comments

