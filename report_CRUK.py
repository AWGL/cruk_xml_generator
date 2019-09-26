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


def main():
    sample_dict = {}

    # Obtain today's date
    current_date = datetime.today().strftime('%Y-%m-%d')

    # Identify samples with data generated on this worksheet id- relies on directories created one for each sample
    samples = locate_samples(os.path.join(path, worksheet_id))

    # Dataframe extract from sample tracking spreadsheet containing data for samples of interest only
    database_parser = ParseDatabase(os.path.join(path, db_name))
    all_dataframe = database_parser.open_database_as_dataframe("New database incoming")
    # Dataframe extract from sample tracking spreadsheet- sequenced samples only
    sequencing_dataframe = database_parser.open_database_as_dataframe("New database workflow")

    # Populate information dictionary from sample tracking spreadsheet- per sample
    for sample in samples:
        # Create dictionary of information
        info_dict = {}
        # Extract sample data from dataframe once
        sample_data = database_parser.get_sample(all_dataframe, sample)
        sample_sequencing_data = database_parser.get_sample(sequencing_dataframe, sample)
        # If sample is not in the Excel database, do not continue as data for this sample will be missing
        if sample_data.empty:
            raise Exception(f"Sample {sample} not found in database {db_name}. Required data will be missing from xml.")
        info_dict["cruk_sample_id"] = database_parser.get_cruk_sample_id(sample_data)
        info_dict["clinical_hub"] = database_parser.get_clinical_hub(sample_data)
        info_dict["org_code"] = database_parser.get_org_code(sample_data)
        info_dict["local_patient_id"] = database_parser.get_patient_id(sample_data)
        info_dict["local_patient_id_2"] = database_parser.get_patient_id_2(sample_data)
        info_dict["source_id"] = database_parser.get_source_sample_id(sample_data)
        info_dict["sample_type"] = database_parser.get_sample_type(sample_data)
        info_dict["tumour_type"] = database_parser.get_tumour_type(sample_data)
        info_dict["morphology_snomed"] = "N/A" #TODO- see email for confirmation from other THs
        info_dict["date_sample_sent"] = database_parser.get_date_sample_received(sample_data)
        info_dict["date_sample_received"] = database_parser.get_date_sample_received(sample_data)
        info_dict["lab_id"] = database_parser.get_lab_id(sample_data)
        info_dict["release_date"] = database_parser.get_report_release_date(sample_sequencing_data)
        info_dict["vol_banked"] = database_parser.get_vol_banked_dna(sample_sequencing_data) #Note that this is DNA only
        info_dict["conc_banked"] = database_parser.get_conc_banked_dna(sample_data) #Note that this is DNA only
        info_dict["banked_loc"] = "Rm2.14 DNA bank_4oC" # Hardcoded
        info_dict["banked_id"] = database_parser.get_lab_id(sample_data)
        info_dict["tech_hub"] = "2 - Cardiff"

        # Parse data from Excel report generated- per sample
        report_parser = ParseReport(worksheet_id)
        #TODO Add exception handling for a missing Excel file
        spreadsheet = report_parser.find_analysis_worksheet(os.path.join(path, worksheet_id, sample), ".xlsx")
        worksheet = report_parser.load_analysis_worksheet(spreadsheet)
        worksheet_data_frame = report_parser.report_table(worksheet)

        #TODO Obtain the reporter and authoriser details from the report
        #TODO temp variables for writing out pdf
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
            gene_data_dict["test_method"] = "19" # Note Hardcoded for TST170 interim informatics solution
            gene_data = report_parser.get_gene_data(gene, worksheet_data_frame)
            gene_data_dict["test_scope"] = report_parser.get_test_scope(gene_data)
            gene_data_dict["test_results_date"] = current_date
            gene_data_dict["test_results"] = report_parser.get_test_result(gene_data)
            gene_data_dict["test_report"] = report_parser.get_test_report(gene_data)
            gene_data_dict["test_status"] = report_parser.get_test_status(gene_data)
            gene_data_dict["comments"] = report_parser.get_comments(gene_data)
            gene_dict[gene] = gene_data_dict
        info_dict["genes"] = gene_dict
        # Add information dictionary to sample dictionary
        sample_dict[sample] = info_dict
        # TODO ONE SAMPLE ONLY FOR TESTING DUE TO AVAILABILITY OF DATA
        print(sample_dict)
        break

    #TODO next, work at this level
    #print(samples)
    #print(sample_dict)

    # Create write out once per sample
    for sample in samples:
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
        # TODO ONE SAMPLE ONLY FOR TESTING DUE TO AVAILABILITY OF DATA
        break


if __name__ == '__main__':
        main()
