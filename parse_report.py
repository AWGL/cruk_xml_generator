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

    def get_gene_number(self, gene):
        from valid_data import genes_dict
        gene_num = genes_dict.get(gene)
        return gene_num

    def get_gene_data(self, gene, df):
        gene_data = df.loc[gene]
        return gene_data

    def get_test_scope(self, gene_data):
        test_scope = gene_data.get("SCOPE")
        return test_scope

    def get_test_result(self, gene_data):
        test_result = gene_data.get("RESULT")
        return test_result

    def get_test_report(self, gene_data):
        test_report = gene_data.get("REPORT")
        return test_report

    def get_test_status(self, gene_data):
        from valid_data import test_status_dict
        test_status = None
        gene_status = gene_data.get("STATUS")
        if gene_status == "Success":
            test_status = test_status_dict.get("Success")
        if gene_status == "Failure":
            test_status = test_status_dict.get("Complete Fail") #TODO awaiting response re difference between 2 and 3
        return test_status

    def get_comments(self, gene_data):
        if gene_data.get("COMMENTS") is None or gene_data.get("COMMENTS").isspace():
            comments = "These results are intended for research purposes."
        else:
            comments = f"These results are intended for research purposes. {gene_data.get('COMMENTS')}."
        return comments

    def parse_report_data(self): #TODO ??
        #This might be better in writeout
        return None

