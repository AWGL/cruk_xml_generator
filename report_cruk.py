import tkinter as tk
from tkinter import ttk
import os
import logging
import re
import shutil
import sys
from datetime import datetime
import parse_report
from parse_database import ParseDatabase
from generate_xml_report import GenerateXml
from generate_report import GenerateReport
from is_valid import IsValid

#Common file paths and version
from config import xml_version
from config import db_path
from config import db_name
from config import xsd
from config import xml_location
from config import pdf_location

# Global variables
from config import test_method
from config import can_be_null
from config import allowed_authorisers
from config import sample_status


class ReportCruk:

    log_file = os.path.join(os.getcwd(), "cruk_report.log")
    
    # Remove old log file
    if os.path.exists(log_file):
        os.remove(log_file)

    def __init__(self, skip_gui=False):
        self.info_dict = {}
        self.status = ""
        self.sample = ""
        self.worksheet = ""
        self.authoriser = ""
        self.skip_gui = skip_gui
        if not self.skip_gui:
            # Root tkinter object created
            self.root = tk.Tk()
            self.root.grid()
            # Places popup roughly in middle of screen
            self.root.eval('tk::PlaceWindow %s center' % self.root.winfo_pathname(self.root.winfo_id()))
            self.root.wm_title("CRUK Generator")
            self.root.label = ttk.Label(text="Software is working. Please wait.")
            self.root.label.grid(column=0, row=0)

            # Initialise an instance of the module logger
            self.ml = ModuleLogger(self.root)
            self.log = self.ml.module_logger
            self.popup = self.ml.my_message

    def root_button_callback(self, event=None):
        self.root.destroy()

    def handle_exception(self, exc_type, exc_value, exc_traceback):
        # Debug is used as this type of error cannot be attempted to be passed to the popup as will happen with
        # use of critical or error level
        self.log.debug("An exception occurred", exc_info=(exc_type, exc_value, exc_traceback))
        # Pass write-out of error to popup
        self.log.critical(f"[CRITICAL ERROR]: {exc_value}. See bioinformatics team for support [CRITICAL ERROR]")
        self.log.critical("\n")
        self.log.critical("****[ERROR] PDF AND XML FILE HAVE NOT BEEN CORRECTLY GENERATED [ERROR]****")
        self.root.mainloop()

    def data_always_required(self, database_parser):
        '''
        Data required for every sample regardless of overall pass/fail status
        :return: dictionary of data extracted from the Excel spreadsheet populated by data from the incoming XML
        '''
        # Dataframe extract from sample tracking spreadsheet containing data for sample of interest only- Incoming tab
        all_dataframe = database_parser.open_database_as_dataframe("New database incoming")
        # Extract sample data from dataframe once
        sample_data = database_parser.get_sample(all_dataframe, self.sample)

        # Dataframe extract from sample tracking spreadsheet containing data for sample of interest only- KPI tab
        kpi_dataframe = database_parser.open_database_as_dataframe("KPI sheet")
        # Extract sample data from dataframe once
        kpi_sample_data = database_parser.get_sample(kpi_dataframe, self.sample)

        # If sample is not in the Excel database, do not continue as data for this sample will be missing
        if sample_data.empty:
            raise Exception(f"Sample {self.sample} not found in database {db_name}. "
                                 f"Required data to generate will be missing")
        self.info_dict["cruk_sample_id"] = database_parser.get_cruk_sample_id(sample_data)
        self.info_dict["clinical_hub"] = database_parser.get_clinical_hub(sample_data)
        self.info_dict["org_code"] = database_parser.get_org_code(sample_data)
        self.info_dict["local_patient_id"] = database_parser.get_patient_id(sample_data)
        self.info_dict["local_patient_id_2"] = database_parser.get_patient_id_2(sample_data)
        self.info_dict["source_id"] = database_parser.get_source_sample_id(sample_data)
        self.info_dict["sample_type"] = database_parser.get_sample_type(sample_data)
        self.info_dict["tumour_type"] = database_parser.get_tumour_type(sample_data)
        self.info_dict["morphology_snomed"] = database_parser.get_snomed(sample_data)
        self.info_dict["date_sample_sent"] = database_parser.get_date_sample_received(sample_data)
        self.info_dict["date_sample_received"] = database_parser.get_date_sample_received(sample_data)
        self.info_dict["lab_id"] = database_parser.get_lab_id(sample_data)
        self.info_dict["vol_banked"] = database_parser.get_vol_banked_dna(kpi_sample_data)  # Note that this is DNA only
        self.info_dict["conc_banked"] = database_parser.get_conc_banked_dna(sample_data)  # Note that this is DNA only
        self.info_dict["banked_loc"] = "Rm2.14 DNA bank_4oC"  # Hardcoded
        self.info_dict["banked_id"] = database_parser.get_lab_id(sample_data)
        self.info_dict["tech_hub"] = "2 - Cardiff"
        self.info_dict["release_date"] = datetime.today().strftime('%Y-%m-%d')
        # Add authoriser details to information dictionary
        self.info_dict["authorised_by"] = self.authoriser
        self.info_dict["date_authorised"] = datetime.today().strftime('%d/%m/%Y')

    def passed_data(self):
        '''
        Data which can be extracted only for samples which were sequenced and analysed
        :return: dictionary of data extracted from the report tab of the Excel spreadsheet generated by the CRUK BaseSpace
        workflow for samples that were sequenced
        '''

        # Parse data from Excel report generated- per sample
        # Obtain year part of worksheet and use to generate path to results file
        from config import results_path
        # Note that the year is not case insensitive and if the path has a different case for folder name file will
        # not be found
        year = f"20{self.worksheet.split('-')[0]}"
        results_path = os.path.join(results_path, year)
        spreadsheet = parse_report.find_analysis_worksheet(os.path.join(results_path, self.worksheet,
                                                                        self.sample), ".xlsx")
        if not spreadsheet:
            raise FileNotFoundError(f"Results spreadsheet for sample {self.sample} could not be located. "
                                    f"Check that Excel file generated by BaseSpace is in the correct location")
        worksheet = parse_report.load_analysis_worksheet(spreadsheet)
        # Extract data from report tab of Excel results
        worksheet_data_frame = parse_report.report_table(worksheet)
        # Extract data from report tab of Excel results
        patient_data_frame = parse_report.checker_table(worksheet)
        # Obtain the reporter and authoriser details from the report
        checker_1_field = parse_report.get_first_checker(patient_data_frame)
        checker_2_field = parse_report.get_second_checker(patient_data_frame)
        # Details are initials <space> date, split into initials and date for inputting into pdf report
        checker_1 = checker_1_field.split()[0]
        checker_1_date = checker_1_field.split()[1]
        checker_2 = checker_2_field.split()[0]
        checker_2_date = checker_2_field.split()[1]
        self.info_dict["reported_by_1"] = checker_1
        self.info_dict["date_reported_1"] = checker_1_date
        self.info_dict["reported_by_2"] = checker_2
        self.info_dict["date_reported_2"] = checker_2_date

        # Populate information dictionary from Excel report- per sample
        # Loop over genes (for each sample)
        genes = parse_report.get_genes(worksheet_data_frame)
        gene_dict = {}
        for gene in genes:
            gene_data_dict = {}
            gene_data_dict["gene"] = parse_report.get_gene_number(gene)
            gene_data_dict["test_method"] = test_method  # Note Hardcoded for TST170 interim informatics solution
            gene_data = parse_report.get_gene_data(gene, worksheet_data_frame)
            gene_data_dict["test_scope"] = parse_report.get_test_scope(gene_data)
            gene_data_dict["test_results_date"] = datetime.today().strftime('%Y-%m-%d')
            gene_data_dict["test_results"] = parse_report.get_test_result(gene_data)
            gene_data_dict["test_report"] = parse_report.get_test_report(gene_data)
            gene_data_dict["test_status"] = parse_report.get_test_status(gene_data)
            gene_data_dict["comments"] = parse_report.get_comments(gene_data)
            gene_dict[gene] = gene_data_dict
        self.info_dict["genes"] = gene_dict

    def qc_fail_data(self):
        '''
        Data for samples which failed QC prior to sequencing
        :return: dictionary of data for samples which failed QC prior to being sequenced
        '''
        from valid_data import test_status_dict
        from valid_data import gene_scope_dict
        from valid_data import genes_dict
        tested = "Not tested"
        gene_dict = {}
        for gene in gene_scope_dict.keys():
            gene_data_dict = {}
            gene_data_dict["gene"] = genes_dict.get(gene)
            gene_data_dict["test_method"] = test_method # Note Hardcoded for TST170 interim informatics solution
            gene_data_dict["test_scope"] = gene_scope_dict.get(gene)
            gene_data_dict["test_results_date"] = datetime.today().strftime('%Y-%m-%d')
            gene_data_dict["test_results"] = tested
            gene_data_dict["test_report"] = "Failed QC step- insufficient sample. Repeat sample requested if available."
            gene_data_dict["test_status"] = test_status_dict.get(tested)
            gene_data_dict["comments"] = ""
            gene_dict[gene] = gene_data_dict
        self.info_dict["genes"] = gene_dict

    def removed_from_trial_data(self):
        '''
        Data for samples which were removed from the trial
        :return: dictionary of data for samples withdrawn from the trial
        '''
        from valid_data import test_status_dict
        from valid_data import gene_scope_dict
        from valid_data import genes_dict
        tested = "Not tested"
        gene_dict = {}
        for gene in gene_scope_dict.keys():
            gene_data_dict = {}
            gene_data_dict["gene"] = genes_dict.get(gene)
            gene_data_dict["test_method"] = test_method  # Note Hardcoded for TST170 interim informatics solution
            gene_data_dict["test_scope"] = gene_scope_dict.get(gene)
            gene_data_dict["test_results_date"] = datetime.today().strftime('%Y-%m-%d')
            gene_data_dict["test_results"] = tested
            gene_data_dict["test_report"] = "Withdrawn at request of clinical hub."
            gene_data_dict["test_status"] = test_status_dict.get(tested)
            gene_data_dict["comments"] = ""
            gene_dict[gene] = gene_data_dict
        self.info_dict["genes"] = gene_dict

    def check_xml_data(self):
        '''
        :param sample_data: dictionary containing the information which will be written out to the pdf and xml
        :return: string for logging indicating that all required data for the xml file is present in the input
        dictionary
        '''
        # Sample level
        for k, v in self.info_dict.items():
            try:
                if k not in can_be_null and (v == "NaN" or len(v) == 0 or v.isspace()):
                    raise Exception(f"Required data for {k} is {v} and so is missing for sample "
                                    f"{self.info_dict.get('lab_id')}.")
            except AttributeError:
                # Ignore that there is no isspace method for the dictionary and catch empty dictionary
                if not v:
                    raise Exception(f"Required data for {k} is {v} (empty) and so is missing for sample "
                                    f"{self.info_dict.get('lab_id')}.")
                pass
        # Gene level
        for k2, v2 in self.info_dict.get("genes").items():
            for k3, v3 in v2.items():
                if k3 not in can_be_null and (v3 == "NaN" or len(v3) == 0 or v3.isspace()):
                    raise Exception(f"Required data for {k3} is set to '{v3}' in gene {k2} and so is missing for "
                                    f"sample {self.info_dict.get('lab_id')}.")
        return "All required data for XML present"

    def report_cruk(self):
        # Handle case where cancel has been pressed
        if not self.skip_gui:
            try:
                self.ml.data_entry.status
                self.ml.data_entry.sample
                self.ml.data_entry.authoriser
            except AttributeError as err:
                raise Exception("Data input was cancelled before all required data was entered")

            # Collect and sanitise input
            self.status = self.ml.data_entry.status
            self.status = self.status.lower().strip()
            self.sample = self.ml.data_entry.sample
            # Handle where sample number is entered with a lower case M and trailing spaces
            self.sample = self.sample.upper().strip()
            self.worksheet = self.ml.data_entry.worksheet
            self.worksheet = self.worksheet.strip()  # Remove any trailing spaces
            self.authoriser = self.ml.data_entry.authoriser
            self.authoriser = self.authoriser.strip()  # Remove any trailing spaces

        # Check input- NOTE THAT THIS requires data to be entered another way or will fail- for testing
        if self.status not in sample_status:
            raise ValueError(f"Invalid status for generating this report. Options are w, f or s. "
                             f"{self.status} was entered")
        if len(self.sample.strip()) == 0:
            raise ValueError(f"Sample id incorrectly entered. Sample id was entered as {self.sample}")
        if self.status == "s" and (len(self.worksheet) == 0 or not re.match("\d\d-", self.worksheet)):
            raise ValueError(f"Worksheet id incorrectly entered. Worksheet id was entered as {self.worksheet}. "
                             f"Worksheets should start with two numbers then a dash e.g. 19-XXXX")
        # Pre-check authoriser is in list of allowed authorisers
        if self.authoriser not in allowed_authorisers:
            raise PermissionError(f"Authoriser {self.authoriser} is not on the list of permitted "
                                  f"authorisers for CRUK")

        # Log sample that files are being generated for
        self.log.info(f"Generating XML and PDF report for sample {self.sample}")

        # Obtain data that is available for every sample regardless of workflow status
        # Populate information dictionary from sample tracking spreadsheet
        database_parser = ParseDatabase(os.path.join(db_path, db_name))
        info_dict = self.data_always_required(database_parser)

        # Gather correct information depending on option selected by user input
        if self.status == "s":
            self.passed_data()
        elif self.status == "f":
            self.qc_fail_data()
        elif self.status == "w":
            self.removed_from_trial_data()

        # Check all required fields populated for xml (data missing from pdf report, e.g. checker, can be seen)
        self.log.info(self.check_xml_data())

        # Obtain clinical hub name in format for output XML
        from valid_data import output_xml_directory_name
        # Name of directory for output XML
        clinical_hub = output_xml_directory_name[self.info_dict.get('clinical_hub')]

        # Generate name for output xml
        formatted_date = datetime.today().strftime('%Y%m%d')
        output_xml = f"{formatted_date} {self.info_dict.get('cruk_sample_id')}.xml"
        # Check if troubleshooting xml file exists and is already open
        if os.path.exists(os.path.join(os.getcwd(), output_xml)):
            if not os.access(os.path.join(os.getcwd(), output_xml), os.W_OK):
                raise IOError(
                    "Please check if XML file is already open. If it is open, please close it and run the software "
                    "again")
        # Create and write out to xml
        write_xml = GenerateXml(self.info_dict, xml_version)
        tree = write_xml.generate_xml()
        self.log.info(write_xml.write_xml(os.path.join(os.getcwd(), output_xml), tree))
        self.log.debug(f"XML file {output_xml} located at {os.getcwd()} generated")

        # Generate name for output pdf
        output_pdf = f"{formatted_date} {self.info_dict.get('cruk_sample_id')}.pdf"
        # Check if troubleshooting pdf file exists and is already open
        if os.path.exists(os.path.join(os.getcwd(), output_pdf)):
            if not os.access(os.path.join(os.getcwd(), output_pdf), os.W_OK):
                raise IOError(
                    "Please check if XML file is already open. If it is open, please close it and run the software "
                    "again")
        # Generate pdf report of required data
        write_report = GenerateReport(os.path.join(os.getcwd(), output_pdf), self.info_dict, self.status)
        self.log.info(write_report.generate_pdf())
        self.log.debug(f"PDF report {output_pdf} located at {os.getcwd()} generated")

        # Test validity- will throw error if xml is not valid
        check_validity = IsValid(os.path.join(os.getcwd(), output_xml), xsd)
        self.log.info(check_validity.validate_xml_format())
        self.log.info(check_validity.validate_xml_schema())
        self.log.debug(f"XML file {output_xml} validated against schema {xsd}")

        # Check existence of final output file and whether it can be written to
        # Remove pdf from output path if already there and move pdf
        if os.path.exists(os.path.join(pdf_location, output_pdf)):
            if not os.access(os.path.join(pdf_location, output_pdf), os.W_OK):
                raise IOError(
                    "Please check if PDF file is already open. If it is open, please close it and run the software "
                    "again")
            os.remove(os.path.join(pdf_location, output_pdf))
        shutil.move(os.path.join(os.getcwd(), output_pdf), pdf_location)
        # Remove xml from output path if already there and move xml
        if os.path.exists(os.path.join(xml_location, clinical_hub, output_xml)):
            if not os.access(os.path.join(xml_location, clinical_hub, output_xml), os.W_OK):
                raise IOError(
                        "Please check if XML file is already open. If it is open, please close it and run the software "
                        "again")
            os.remove(os.path.join(xml_location, clinical_hub, output_xml))
        shutil.move(os.path.join(os.getcwd(), output_xml), os.path.join(xml_location, clinical_hub))

        # Check XML file has copied correctly
        self.log.debug(f"Expected location of XML {output_xml} to send to CRUK is "
                       f"{os.path.join(xml_location, clinical_hub)}")
        if not os.path.exists(os.path.join(xml_location, clinical_hub, output_xml)):
            raise FileNotFoundError(f"XML is not found in correct location for sending to CRUK. File copy "
                                    f"operation has not been successful")

        self.log.info(f"XML file copied to directory for sending to CRUK")

        # Start popup- on button click close popup
        self.root.mainloop()


class ModuleLogger:

    def __init__(self, parent_window):
        # Create pop-up box for entering data
        from message_box import MyEntryWindow
        self.data_entry = MyEntryWindow(parent_window)

        # Create log file pop-up box
        from message_box import MessageBox, MyHandlerText
        self.my_message = MessageBox(parent_window)
        self.module_logger = logging.getLogger(__name__)
        self.module_logger.setLevel(logging.DEBUG)

        # Create handler to route messages to popup
        gui_handler = MyHandlerText(self.my_message.popup_text)
        gui_handler.setLevel(logging.INFO)
        self.module_logger.addHandler(gui_handler)

        # Create handler to route messages to file
        file_handler = logging.FileHandler(os.path.join(os.getcwd(), ReportCruk.log_file))
        file_handler.setLevel(logging.DEBUG)
        self.module_logger.addHandler(file_handler)


def debug(report_cruk_object, status, sample, auth, worksheet=None):
    report_cruk_object.status = status
    report_cruk_object.sample = sample
    report_cruk_object.authoriser = auth
    report_cruk_object.worksheet = worksheet
    report_cruk_object.log = logging.getLogger()
    return report_cruk_object


def main():
    rc = ReportCruk(True)
    sys.excepthook = rc.handle_exception
    # To allow debugging
    rc = debug(rc, "f", "19M5", "mjm")
    rc.report_cruk()


if __name__ == '__main__':
    main()


