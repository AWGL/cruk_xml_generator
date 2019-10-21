import os
import re
import shutil
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


def data_always_required(database_parser, sample):
    '''
    Data required for every sample regardless of overall pass/fail status
    :return: dictionary of data extracted from the Excel spreadsheet populated by data from the incoming XML
    '''
    info_dict = {}
    # Dataframe extract from sample tracking spreadsheet containing data for sample of interest only- Incoming tab
    all_dataframe = database_parser.open_database_as_dataframe("New database incoming")
    # Extract sample data from dataframe once
    sample_data = database_parser.get_sample(all_dataframe, sample)

    # Dataframe extract from sample tracking spreadsheet containing data for sample of interest only- KPI tab
    kpi_dataframe = database_parser.open_database_as_dataframe("KPI sheet")
    # Extract sample data from dataframe once
    kpi_sample_data = database_parser.get_sample(kpi_dataframe, sample)

    # If sample is not in the Excel database, do not continue as data for this sample will be missing
    if sample_data.empty:
        raise Exception(f"Sample {sample} not found in database {db_name}. Required data to generate will be missing.")
    info_dict["cruk_sample_id"] = database_parser.get_cruk_sample_id(sample_data)
    info_dict["clinical_hub"] = database_parser.get_clinical_hub(sample_data)
    info_dict["org_code"] = database_parser.get_org_code(sample_data)
    info_dict["local_patient_id"] = database_parser.get_patient_id(sample_data)
    info_dict["local_patient_id_2"] = database_parser.get_patient_id_2(sample_data)
    info_dict["source_id"] = database_parser.get_source_sample_id(sample_data)
    info_dict["sample_type"] = database_parser.get_sample_type(sample_data)
    info_dict["tumour_type"] = database_parser.get_tumour_type(sample_data)
    info_dict["morphology_snomed"] = database_parser.get_snomed(sample_data)
    info_dict["date_sample_sent"] = database_parser.get_date_sample_received(sample_data)
    info_dict["date_sample_received"] = database_parser.get_date_sample_received(sample_data)
    info_dict["lab_id"] = database_parser.get_lab_id(sample_data)
    info_dict["vol_banked"] = database_parser.get_vol_banked_dna(kpi_sample_data) # Note that this is DNA only
    info_dict["conc_banked"] = database_parser.get_conc_banked_dna(sample_data) # Note that this is DNA only
    info_dict["banked_loc"] = "Rm2.14 DNA bank_4oC" # Hardcoded
    info_dict["banked_id"] = database_parser.get_lab_id(sample_data)
    info_dict["tech_hub"] = "2 - Cardiff"
    info_dict["release_date"] = datetime.today().strftime('%d/%m/%Y')
    return info_dict


def passed_data(worksheet_id, sample, info_dict):
    '''
    Data which can be extracted only for samples which were sequenced and analysed
    :return: dictionary of data extracted from the report tab of the Excel spreadsheet generated by the CRUK BaseSpace
    workflow for samples that were sequenced
    '''

    # Parse data from Excel report generated- per sample
    # Obtain year part of worksheet and use to generate path to results file
    from config import results_path
    year = f"20{worksheet_id.split('-')[0]} Nextera Results"
    results_path = os.path.join(results_path, year)
    spreadsheet = parse_report.find_analysis_worksheet(os.path.join(results_path, worksheet_id, sample), ".xlsx")
    if not spreadsheet:
        raise FileNotFoundError(f"Results spreadsheet for sample {sample} could not be located. Check that Excel file "
                                f"generated by BaseSpace is in the correct location.")
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
    info_dict["reported_by_1"] = checker_1
    info_dict["date_reported_1"] = checker_1_date
    info_dict["reported_by_2"] = checker_2
    info_dict["date_reported_2"] = checker_2_date

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
    info_dict["genes"] = gene_dict
    return info_dict


def qc_fail_data(info_dict):
    '''
    Data for samples which failed QC prior to sequencing
    :return: dictionary of data for samples which failed QC prior to being sequenced
    '''
    from valid_data import test_status_dict
    from valid_data import gene_scope_dict
    from valid_data import genes_dict
    tested = "Not tested"
    info_dict["vol_banked"] = "0"
    info_dict["release_date"] = datetime.today().strftime('%Y-%m-%d')
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
    info_dict["genes"] = gene_dict
    return info_dict


def removed_from_trial_data(info_dict):
    '''
    Data for samples which were removed from the trial
    :return: dictionary of data for samples withdrawn from the trial
    '''
    from valid_data import test_status_dict
    from valid_data import gene_scope_dict
    from valid_data import genes_dict
    tested = "Not tested"
    info_dict["vol_banked"] = "0"
    info_dict["release_date"] = datetime.today().strftime('%Y-%m-%d')
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
    info_dict["genes"] = gene_dict
    return info_dict


def check_xml_data(sample_data):
    '''
    :param sample_data: dictionary containing the information which will be written out to the pdf and xml
    :return: string for logging indicating that all required data for the xml file is present in the input dictionary
    '''
    # Sample level
    for k, v in sample_data.items():
        try:
            if k not in can_be_null and (v == "NaN" or len(v) == 0 or v.isspace()):
                raise Exception(f"Required data for {k} is {v} and so is missing for sample "
                                f"{sample_data.get('lab_id')}.")
        except AttributeError:
            # Ignore that there is no isspace method for the dictionary and catch empty dictionary
            if not v:
                raise Exception(f"Required data for {k} is {v} (empty) and so is missing for sample "
                                f"{sample_data.get('lab_id')}.")
            pass
    # Gene level
    for k2, v2 in sample_data.get("genes").items():
        for k3, v3 in v2.items():
            if k3 not in can_be_null and (v3 == "NaN" or len(v3) == 0 or v3.isspace()):
                raise Exception(f"Required data for {k3} is set to '{v3}' in gene {k2} and so is missing for "
                                f"sample {sample_data.get('lab_id')}.")
    return "All required data for XML present"


def main():
    '''
    # Enter input and check it for sanity where possible
    status = input("Enter Status: options are w (withdrawn), f (failed) or s (sequenced):  ")
    status = status.lower().strip()
    if status not in sample_status:
        raise Exception(f"Invalid status for generating this report. Options are w, f or s. {status} was entered.")
    sample = input("Enter Sample: ")
    sample = sample.upper().strip() # Handle where sample number is entered with a lower case M and trailing spaces
    if len(sample.strip()) == 0:
        raise Exception(f"Sample id incorrectly entered. Sample id was entered as {sample}")
    # No worksheet for withdrawn and failed samples, only for samples which were put through sequencing
    worksheet = "N/A"
    if status == "s":
        worksheet = input("Enter Worksheet: ")
        worksheet = worksheet.strip() # Remove any trailing spaces
        if len(worksheet) == 0 or not re.match("\d\d-", worksheet):
            raise Exception(f"Worksheet id incorrectly entered. Worksheet id was entered as {worksheet}. Worksheets "
                            f"should start with two numbers then a dash e.g. 19-XXXX")
    authoriser = input("Enter Authoriser Initials: ")
    authoriser = authoriser.strip() # Remove any trailing spaces
    '''
    # Create dictionary to hold information extracted from sources
    sample_dict = {}

    #TODO temp variables
    status = "f"
    sample = "19M13875"
    worksheet = "19-9999"
    authoriser = "mjm"

    # Obtain data that is available for every sample regardless of workflow status
    # Populate information dictionary from sample tracking spreadsheet
    database_parser = ParseDatabase(os.path.join(db_path, db_name))
    info_dict = data_always_required(database_parser, sample)

    # Gather correct information depending on option selected by user input
    if status == "s":
        info_dict = passed_data(worksheet, sample, info_dict)
    elif status == "f":
        info_dict = qc_fail_data(info_dict)
    elif status == "w":
        info_dict = removed_from_trial_data(info_dict)

    # Add authoriser details to information dictionary- pre-check are in list of allowed authorisers
    if authoriser not in allowed_authorisers:
        raise PermissionError(f"Authoriser {authoriser} is not a permitted authoriser for CRUK. Please try again or "
                                f"see the bioinformatics team to arrange to have your initials added to the list of "
                                f"CRUK authorisers in this software.")
    info_dict["authorised_by"] = authoriser
    info_dict["date_authorised"] = datetime.today().strftime('%d/%m/%Y')

    # Add information dictionary to sample dictionary
    sample_dict[sample] = info_dict

    # Check all required fields populated for xml (data missing from pdf report, e.g. checker, can be seen)
    print(check_xml_data(sample_dict.get(sample)))

    # Obtain clinical hub name in format for output XML TODO check how these are entered and names of directories correspond
    clinical_hub = info_dict.get('clinical_hub').split("-")[1].strip()

    # Generate name for output xml
    formatted_date = datetime.today().strftime('%Y%m%d')
    output_xml = f"{formatted_date} {sample_dict.get(sample).get('cruk_sample_id')}.xml"
    # Check if troubleshooting xml file exists and is already open
    if os.path.exists(os.path.join(os.getcwd(), output_xml)):
        if not os.access(os.path.join(os.getcwd(), output_xml), os.W_OK):
            raise Exception(
                "Please check if XML file is already open. If it is open, please close it and run the software again")
    # Create and write out to xml
    write_xml = GenerateXml(sample_dict.get(sample), xml_version)
    tree = write_xml.generate_xml()
    write_xml.write_xml(os.path.join(os.getcwd(), output_xml), tree)

    # Generate name for output pdf
    output_pdf = f"{formatted_date} {sample_dict.get(sample).get('cruk_sample_id')}.pdf"
    # Check if troubleshooting pdf file exists and is already open
    if os.path.exists(os.path.join(os.getcwd(), output_pdf)):
        if not os.access(os.path.join(os.getcwd(), output_pdf), os.W_OK):
            raise Exception(
                "Please check if XML file is already open. If it is open, please close it and run the software again")
    # Generate pdf report of required data
    write_report = GenerateReport(os.path.join(os.getcwd(), output_pdf), sample_dict.get(sample), status)
    print(write_report.pdf_writer())

    # Test validity- will throw error if xml is not valid
    check_validity = IsValid(os.path.join(os.getcwd(), output_xml), xsd)
    print(check_validity.validate_xml_format())
    print(check_validity.validate_xml_schema())

    # Check existence of final output file and whether it can be written to
    # Remove pdf from output path if already there and move pdf
    if os.path.exists(os.path.join(pdf_location, output_pdf)):
        if not os.access(os.path.join(pdf_location, output_pdf), os.W_OK):
            raise Exception(
                "Please check if PDF file is already open. If it is open, please close it and run the software again")
        os.remove(os.path.join(pdf_location, output_pdf))
    shutil.move(os.path.join(os.getcwd(), output_pdf), pdf_location)
    # Remove xml from output path if already there and move xml
    if os.path.exists(os.path.join(xml_location, clinical_hub, output_xml)):
        if not os.access(os.path.join(xml_location, clinical_hub, output_xml), os.W_OK):
            raise Exception(
                "Please check if XML file is already open. If it is open, please close it and run the software again")
        os.remove(os.path.join(xml_location, clinical_hub, output_xml))
    shutil.move(os.path.join(os.getcwd(), output_xml), os.path.join(xml_location, clinical_hub))


if __name__ == '__main__':
    main()

