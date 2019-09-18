import os
from parse_report import ParseReport
from parse_database import ParseDatabase
from generate_xml_report import GenerateXml
from is_valid import IsValid

path = "/Users/sararey/Documents/cruk_reporting" #temp path for testing
db_name = "LUNG sample tracking_Nextera.xls" #temp for testing
worksheet_id = "19-5037" #temp for testing- obtain from ?- entry by scientist?


def main():
    information_dictionary = {} #TODO generate this


    # Parse data from Excel report generated per sample
    report_parser = ParseReport(worksheet_id)
    samples = report_parser.locate_samples(os.path.join(path, worksheet_id))
    report = report_parser.find_analysis_worksheet(os.path.join(path, worksheet_id, samples[0]), ".xlsx") # test for one sample initially
    worksheet_data_frame = report_parser.load_analysis_worksheet(report)
    #print(worksheet_data_frame)

    print(samples)
    database_parser = ParseDatabase(os.path.join(path, db_name))
    database = database_parser.open_database()
    #TODO Obtain database as pandas dataframe for easier manipulation
    dataframe = database_parser.database_as_dataframe(database)
    database_parser.get_sample_data(database, samples[0]) # test for one sample initially



    write_xml = GenerateXml(information_dictionary)
    print(write_xml.data_import())  # TODO Use this imported data to populate xml
    parsed_data = None  # TODO create dictionary of required data parsed from data sources
    write_xml.load_existing_xml(
        os.path.join("/Users/sararey/Documents/cruk_reporting/", "20190730 RVFAR-W014779Y-H19G5842 A1.xml"))
    tree = write_xml.generate_xml(parsed_data)
    write_xml.load_existing_xml(os.path.join(write_xml.output_path, write_xml.output_file_name))

    # Test validity
    #check_validity = IsValid(tree)
    #check_validity.itera() TODO Decide on best solution for this later




if __name__ == '__main__':
        main()
