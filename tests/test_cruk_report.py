import unittest
from report_cruk import *
from tests.test_config import *


class TestCrukReportInput(unittest.TestCase):
    def setUp(self): #-> None:
        self.rc = ReportCruk(True)
        self.rc.log = logging.getLogger()

    # Test status input
    def test_status_input_empty(self):
        self.status_input("")

    def test_status_input_space(self):
        self.status_input(" ")

    def test_status_input_incorrect(self):
        self.status_input("g")

    # Test sample input
    def test_sample_input_empty(self):
        self.sample_input("")

    def test_sample_input_space(self):
        self.sample_input(" ")

    # Test worksheet input
    def test_passed_worksheet_input_empty(self):
        self.worksheet_input_passed("")

    def test_passed_worksheet_input_space(self):
        self.worksheet_input_passed(" ")

    def test_passed_worksheet_input_incorrect(self):
        self.worksheet_input_passed("19000")

    def test_worksheet_failed_input_empty(self):
        self.worksheet_input_failed("")

    def test_worksheet_failed_input_space(self):
        self.worksheet_input_failed(" ")

    def test_worksheet_failed_input_incorrect(self):
        self.worksheet_input_failed("19000")

    def test_worksheet_withdrawn_input_empty(self):
        self.worksheet_input_withdrawn("")

    def test_worksheet_withdrawn_input_space(self):
        self.worksheet_input_withdrawn(" ")

    def test_worksheet_withdrawn_input_incorrect(self):
        self.worksheet_input_withdrawn("19000")

    def test_authoriser_empty(self):
        self.authoriser("")

    def test_authoriser_space(self):
        self.authoriser(" ")

    def test_authoriser_incorrect(self):
        self.authoriser("some")

    # Functions to call
    def status_input(self, status):
        with self.assertRaises(ValueError) as e:
            self.rc.status = status
            self.rc.report_cruk()
            print(status)
        self.assertEqual(f"Invalid status for generating this report. Options are w, f or s. {status} was entered",
                         str(e.exception))

    def sample_input(self, sample):
        with self.assertRaises(ValueError) as e:
            self.rc.status = "s"
            self.rc.sample = sample
            self.rc.report_cruk()
        self.assertEqual(f"Sample id incorrectly entered. Sample id was entered as {sample}",
                         str(e.exception))

    def worksheet_input_passed(self, worksheet):
        with self.assertRaises(ValueError) as e:
            self.rc.status = "s"
            self.rc.sample = "19M"
            self.rc.worksheet = worksheet
            self.rc.report_cruk()
        self.assertEqual(f"Worksheet id incorrectly entered. Worksheet id was entered as {worksheet}. "
                         "Worksheets should start with two numbers then a dash e.g. 19-XXXX",
                         str(e.exception))

    def worksheet_input_failed(self, worksheet):
        with self.assertRaises(PermissionError) as e:
            self.rc.status = "f"
            self.rc.sample = "19M"
            self.rc.worksheet = worksheet
            self.rc.report_cruk()
        self.assertEqual("Authoriser  is not on the list of permitted authorisers for CRUK",
                            str(e.exception))

    def worksheet_input_withdrawn(self, worksheet):
        with self.assertRaises(PermissionError) as e:
            self.rc.status = "w"
            self.rc.sample = "19M"
            self.rc.worksheet = worksheet
            self.rc.report_cruk()
        self.assertEqual("Authoriser  is not on the list of permitted authorisers for CRUK",
                            str(e.exception))

    def authoriser(self, authoriser):
        with self.assertRaises(PermissionError) as e:
            self.rc.status = "s"
            self.rc.sample = "19M"
            self.rc.worksheet = "19-0"
            self.rc.authoriser = authoriser
            self.rc.report_cruk()
        self.assertEqual(f"Authoriser {authoriser} is not on the list of permitted authorisers for CRUK",
                            str(e.exception))


class TestCrukReport(unittest.TestCase):

    def setUp(self): #-> None:
        self.rc = ReportCruk(True)
        self.rc.log = logging.getLogger()
        self.rc.status = "s"
        self.rc.worksheet = "19-9999"
        self.rc.authoriser = "mjm"
        self.rc.xml_version = xml_version
        self.rc.db_path = db_path
        self.rc.db_name = db_name
        self.rc.xsd = xsd
        self.rc.xml_location = xml_location
        self.rc.pdf_location = pdf_location
        self.rc.results_path = results_path

    def test_no_clin_hub_directory(self):
        # Test to ensure error thrown when a destination directory does not exist for this clinical hub yet
        with self.assertRaises(FileNotFoundError) as e:
            self.rc.sample = "19M6"
            self.rc.report_cruk()
        self.assertEqual(f"XML is not found in correct location for sending to CRUK. File copy "
                         f"operation has not been successful", str(e.exception))

    def test_wrong_id_in_report(self):
        with self.assertRaises(Exception) as e:
            self.rc.sample = "19M9"
            self.rc.report_cruk()
        self.assertEqual(f"Wrong report. File for DNA sample name {self.rc.sample}"
                         f", but report tab for DNA sample SMP2-19M99", str(e.exception))

    def test_sample_not_in_db(self):
        with self.assertRaises(Exception) as e:
            self.rc.sample = "19M90"
            self.rc.report_cruk()
        self.assertEqual(f"Sample {self.rc.sample} not found in database SMP2v3 workflow tracker.xlsx. "
                         f"Required data to generate will be missing", str(e.exception))

    def test_sample_not_in_kpi_tab(self):
        '''
        test volume is correctly returned as zero for samples that do not have an entry in the kpi tab
        '''
        self.rc.sample = "19M7"
        self.rc.report_cruk()
        self.assertEqual(self.rc.info_dict.get('vol_banked'), "0")

    def test_incorrect_sample_type_name(self):
        with self.assertRaises(Exception) as e:
            self.rc.sample = "19M5"
            self.rc.report_cruk()
        self.assertEqual("KeyError('9-tissue-bronchoscopicbiopsy')", str(e.exception))




    # Tests for data parsed out into dictionary


    # Tests for XML generated
    def pass_xml_test(self):
        '''
        Test if newly generated xml for a sample which passed QC and was sequenced matches an existing xml
        :return:
        '''

        # Load in template xml


        # Load in generated xml


        return "hello"

    def fail_xml_test(self):
        return None

    def withdrawn_xml_test(self):
        return None


    # Check PDF is correctly named



if __name__ == '__main__':
    unittest.main()

