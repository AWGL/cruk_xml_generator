import os
from datetime import datetime
from reporter import locate_samples
from parse_report import ParseReport
from parse_database import ParseDatabase
from generate_xml_report import GenerateXml
from is_valid import IsValid

path = "/Users/sararey/Documents/cruk_reporting" #temp path for testing
#db_name = "LUNG sample tracking_Nextera.xls" #temp for testing
db_name = "New database.xlsx"
worksheet_id = "19-9999" #temp for testing- obtain from ?- entry by scientist?
xsd = "/Users/sararey/Documents/cruk_reporting/info/SMP2XSD (Results) v3.8.xsd"
test_method = "19"


def data_always_required(database_parser, sample):
    '''
    Data required for every sample regardless of overall pass/fail status
    :return:
    '''

    info_dict = {}
    # Dataframe extract from sample tracking spreadsheet containing data for sample of interest only
    all_dataframe = database_parser.open_database_as_dataframe("New database incoming")
    # Extract sample data from dataframe once
    sample_data = database_parser.get_sample(all_dataframe, sample)

    # If sample is not in the Excel database, do not continue as data for this sample will be missing
    if sample_data.empty:
        raise Exception(f"Sample {sample} not found in database {db_name}. Required data is missing.")
    info_dict["cruk_sample_id"] = database_parser.get_cruk_sample_id(sample_data)
    info_dict["clinical_hub"] = database_parser.get_clinical_hub(sample_data)
    info_dict["org_code"] = database_parser.get_org_code(sample_data)
    info_dict["local_patient_id"] = database_parser.get_patient_id(sample_data)
    info_dict["local_patient_id_2"] = database_parser.get_patient_id_2(sample_data)
    info_dict["source_id"] = database_parser.get_source_sample_id(sample_data)
    info_dict["sample_type"] = database_parser.get_sample_type(sample_data)
    info_dict["tumour_type"] = database_parser.get_tumour_type(sample_data)
    info_dict["morphology_snomed"] = "N/A"  # TODO- see email for confirmation from other THs
    info_dict["date_sample_sent"] = database_parser.get_date_sample_received(sample_data)
    info_dict["date_sample_received"] = database_parser.get_date_sample_received(sample_data)
    info_dict["lab_id"] = database_parser.get_lab_id(sample_data)
    info_dict["conc_banked"] = database_parser.get_conc_banked_dna(sample_data) #Note that this is DNA only
    info_dict["banked_loc"] = "Rm2.14 DNA bank_4oC" # Hardcoded
    info_dict["banked_id"] = database_parser.get_lab_id(sample_data)
    info_dict["tech_hub"] = "2 - Cardiff"
    return info_dict

def passed_data(database_parser, sample, info_dict):
    '''
    Data which can be extracted only for samples which were sequenced and analysed
    :return:
    '''
    # Dataframe extract from sample tracking spreadsheet- sequenced samples only
    sequencing_dataframe = database_parser.open_database_as_dataframe("New database workflow")
    # Extract sample data from dataframe once
    sample_sequencing_data = database_parser.get_sample(sequencing_dataframe, sample)
    info_dict["vol_banked"] = database_parser.get_vol_banked_dna(sample_sequencing_data)  # Note that this is DNA only
    info_dict["release_date"] = database_parser.get_report_release_date(sample_sequencing_data)

    # Parse data from Excel report generated- per sample
    report_parser = ParseReport(worksheet_id)
    # TODO Add exception handling for a missing Excel file
    spreadsheet = report_parser.find_analysis_worksheet(os.path.join(path, worksheet_id, sample), ".xlsx")
    worksheet = report_parser.load_analysis_worksheet(spreadsheet)
    worksheet_data_frame = report_parser.report_table(worksheet)

    # TODO Obtain the reporter and authoriser details from the report
    # TODO temp variables for writing out pdf
    info_dict["reported_by_1"] = "sr"
    info_dict["date_reported_1"] = "09/10/2019"
    info_dict["reported_by_2"] = "smr"
    info_dict["date_reported_2"] = "10/10/2019"
    info_dict["authorised by"] = "smrw"
    info_dict["date_authorised"] = "11/10/2019"

    # Populate information dictionary from Excel report- per sample
    # Loop over genes (for each sample)
    genes = report_parser.get_genes(worksheet_data_frame)
    gene_dict = {}
    for gene in genes:
        gene_data_dict = {}
        gene_data_dict["gene"] = report_parser.get_gene_number(gene)
        gene_data_dict["test_method"] = test_method  # Note Hardcoded for TST170 interim informatics solution
        gene_data = report_parser.get_gene_data(gene, worksheet_data_frame)
        gene_data_dict["test_scope"] = report_parser.get_test_scope(gene_data)
        gene_data_dict["test_results_date"] = datetime.today().strftime('%Y-%m-%d')
        gene_data_dict["test_results"] = report_parser.get_test_result(gene_data)
        gene_data_dict["test_report"] = report_parser.get_test_report(gene_data)
        gene_data_dict["test_status"] = report_parser.get_test_status(gene_data)
        gene_data_dict["comments"] = report_parser.get_comments(gene_data)
        gene_dict[gene] = gene_data_dict
    info_dict["genes"] = gene_dict
    return info_dict

def qc_fail_data(info_dict):
    '''
    Data for samples which failed QC prior to sequencing
    :return:
    '''
    from valid_data import test_status_dict
    from valid_data import gene_scope_dict
    from valid_data import genes_dict
    tested = "Not tested"
    info_dict["vol_banked"] = "0.0"
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
    :return:
    '''
    from valid_data import test_status_dict
    from valid_data import gene_scope_dict
    from valid_data import genes_dict
    tested = "Not tested"
    info_dict["vol_banked"] = "0.0"
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


def main():
    # TODO determine how to tell if passed or failed sample
    status = "withdrawn"

    #TODO Temp variable
    # Identify samples with data generated on this worksheet id- relies on directories created one for each sample
    samples = locate_samples(os.path.join(path, worksheet_id))
    sample = samples[0]

    # Create dictionary to hold information
    sample_dict = {}

    # Obtain data that is available for every sample regardless of workflow status
    # Populate information dictionary from sample tracking spreadsheet
    database_parser = ParseDatabase(os.path.join(path, db_name))
    info_dict = data_always_required(database_parser, sample)

    if status == "passed":
        info_dict = passed_data(database_parser, sample, info_dict)
    elif status == "failed":
        info_dict = qc_fail_data(info_dict)
    elif status == "withdrawn":
        info_dict = removed_from_trial_data(info_dict)


    # Add information dictionary to sample dictionary
    sample_dict[sample] = info_dict
    print(sample_dict)

    # Create write out
    write_xml = GenerateXml(sample_dict.get(sample))
    tree = write_xml.generate_xml()
    formatted_date = datetime.today().strftime('%Y%m%d')
    output_xml = f"{formatted_date} {sample_dict.get(sample).get('cruk_sample_id')}.xml"
    write_xml.write_xml(os.path.join(write_xml.output_path, output_xml), tree)
    write_xml.load_existing_xml(os.path.join(write_xml.output_path, output_xml))

    # Test validity
    check_validity = IsValid(os.path.join(write_xml.output_path, output_xml), xsd)
    print(check_validity.validate_xml_format())
    print(check_validity.validate_xml_schema())

    # Generate pdf report
    import generate_report
    print(generate_report)

if __name__ == '__main__':
        main()
