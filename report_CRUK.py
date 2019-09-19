import os
from datetime import datetime
from reporter import locate_samples
from parse_report import ParseReport
from parse_database import ParseDatabase
from generate_xml_report import GenerateXml
from is_valid import IsValid

path = "/Users/sararey/Documents/cruk_reporting" #temp path for testing
db_name = "LUNG sample tracking_Nextera.xls" #temp for testing
worksheet_id = "19-5037" #temp for testing- obtain from ?- entry by scientist?


def main():
    sample_dict = {}

    # Obtain today's date
    current_date = datetime.today().strftime('%Y-%m-%d')

    # Identify samples with data generated on this worksheet id- relies on directories created one for each sample
    samples = locate_samples(os.path.join(path, worksheet_id))

    # Dataframe extract from sample tracking spreadsheet containing data for samples of interest only
    database_parser = ParseDatabase(os.path.join(path, db_name))
    dataframe = database_parser.open_database_as_dataframe()
    samples_dataframe = database_parser.create_dataframe_of_samples(dataframe, samples)

    # Populate information dictionary from sample tracking spreadsheet- per sample
    for sample in samples:
        # Create dictionary of information
        info_dict = {}
        # Extract sample data from dataframe once
        sample_data = database_parser.get_sample(samples_dataframe, sample)
        info_dict["clinical_hub"] = database_parser.get_clinical_hub(sample_data)
        info_dict["org_code"] = None
        info_dict["local_patient_id"] = database_parser.get_patient_id(sample_data)
        info_dict["source_id"] = database_parser.get_source_sample_id(sample_data)
        info_dict["sample_type"] = database_parser.get_sample_type(sample_data)
        info_dict["tumour_type"] = None
        info_dict["morphology_snomed"] = None
        info_dict["date_sample_sent"] = None
        info_dict["date_sample_received"] = database_parser.get_date_sample_received(sample_data)
        info_dict["lab_id"] = database_parser.get_lab_id(sample_data)
        info_dict["release_date"] = current_date
        info_dict["vol_banked"] = None
        info_dict["conc_banked"] = database_parser.get_conc_banked(sample_data)
        info_dict["tech_hub"] = "2 - Cardiff"

        # Parse data from Excel report generated- per sample
        report_parser = ParseReport(worksheet_id)
        spreadsheet = report_parser.find_analysis_worksheet(os.path.join(path, worksheet_id, samples[0]), ".xlsx") #TODO test for one sample initially
        worksheet = report_parser.load_analysis_worksheet(spreadsheet)
        worksheet_data_frame = report_parser.report_table(worksheet)
        print(worksheet_data_frame)


        # Populate information dictionary from Excel report- per sample
        # Check whether there is RNA data in the report or the report is DNA only
        analysed_samples = report_parser.report_samples(worksheet)
        #TODO IMPLEMENT THIS TO HANDLE BOTH CASES- anticipate will be identical with potential extra step for RNA
        if 0 in analysed_samples:
            "DNA pathway"
        elif len(analysed_samples) == 2:
            "RNA pathway"
        else:
            raise Exception(f"Could not determine if report worksheet {worksheet_id}-{sample} analysed for DNA or both \
            DNA and RNA.")

        # Loop over genes (for each sample)
        genes = report_parser.get_genes(worksheet_data_frame)
        for gene in genes:
            gene_dict = {}
            print(gene)
            gene_dict["gene"] = gene
            gene_dict["test_method"] = "19 - Illumina NGS TST170 Panel 43 of 170"

        info_dict["genes"] = gene_dict
        # Add information dictionary to sample dictionary
        sample_dict[sample] = info_dict
    print(samples)
    print(sample_dict)





    '''
    write_xml = GenerateXml(information_dictionary)
    print(write_xml.data_import())  # TODO Use this imported data to populate xml
    parsed_data = None  # TODO create dictionary of required data parsed from data sources
    write_xml.load_existing_xml(
        os.path.join("/Users/sararey/Documents/cruk_reporting/", "20190730 RVFAR-W014779Y-H19G5842 A1.xml"))
    tree = write_xml.generate_xml(parsed_data)
    write_xml.load_existing_xml(os.path.join(write_xml.output_path, write_xml.output_file_name))
    '''
    # Test validity
    #check_validity = IsValid(tree)
    #check_validity.itera() TODO Decide on best solution for this later




if __name__ == '__main__':
        main()
