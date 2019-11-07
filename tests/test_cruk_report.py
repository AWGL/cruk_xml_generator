import unittest
from report_cruk import *


class TestCrukReportInput(unittest.TestCase):
    def setUp(self): #-> None:
        self.rc = ReportCruk(True)

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
    def test_worksheet_input_empty(self):
        self.worksheet_input_passed("")

    def test_worksheet_input_space(self):
        self.worksheet_input_passed(" ")

    def test_worksheet_input_incorrect(self):
        self.worksheet_input_passed("19000")

    #def test_worksheet_


    '''
    def test_empty_worksheet_input_passed_sample(self):
        with self.assertRaises(ValueError) as e:
            self.rc.status = "s"
            self.rc.sample = "19M"
            self.rc.worksheet == ""
            self.rc.report_cruk()
        self.assertEqual("Worksheet id incorrectly entered. Worksheet id was entered as . "
                                "Worksheets should start with two numbers then a dash e.g. 19-XXXX",
                            str(e.exception))

    def test_empty_worksheet_input_failed_sample(self):
        # This should throw at the authoriser check step as there is no check for empty worksheet, but authoriser
        # is not set
        with self.assertRaises(ValueError) as e:
            self.rc.status = "f"
            self.rc.sample = "19M"
            self.rc.worksheet == ""
            self.rc.report_cruk()
        self.assertEqual("Authoriser  is not on the list of permitted authorisers for CRUK",
                            str(e.exception))

    def test_empty_worksheet_input_withdrawn_sample(self):
        # This should throw at the authoriser check step as there is no check for empty worksheet, but authoriser
        # is not set
        with self.assertRaises(ValueError) as e:
            self.rc.status = "w"
            self.rc.sample = "19M"
            self.rc.worksheet == ""
            self.rc.report_cruk()
        self.assertEqual("Authoriser  is not on the list of permitted authorisers for CRUK",
                            str(e.exception))

    def test_empty_authoriser_input_passed_sample(self):
        with self.assertRaises(PermissionError) as e:
            self.rc.status = "s"
            self.rc.sample = "19M"
            self.rc.worksheet = "19-"
            self.rc.authoriser == ""
            self.rc.report_cruk()
        self.assertEqual("Authoriser  is not on the list of permitted authorisers for CRUK",
                            str(e.exception))

    def test_empty_authoriser_input_failed_sample(self):
        with self.assertRaises(PermissionError) as e:
            self.rc.status = "f"
            self.rc.sample = "19M"
            self.rc.worksheet = "19-"
            self.rc.authoriser == ""
            self.rc.report_cruk()
        self.assertEqual("Authoriser  is not on the list of permitted authorisers for CRUK",
                            str(e.exception))

    def test_empty_authoriser_input_withdrawn_sample(self):
        with self.assertRaises(PermissionError) as e:
            self.rc.status = "w"
            self.rc.sample = "19M"
            self.rc.worksheet = "19-"
            self.rc.authoriser == ""
            self.rc.report_cruk()
        self.assertEqual("Authoriser  is not on the list of permitted authorisers for CRUK",
                            str(e.exception))
    '''
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
            self.rc.worksheet == worksheet
            self.rc.report_cruk()
        self.assertEqual("Worksheet id incorrectly entered. Worksheet id was entered as . "
                         "Worksheets should start with two numbers then a dash e.g. 19-XXXX",
                         str(e.exception))

    def worksheet_input_failed(self):
        return None

    def worksheet_input_withdrawn(self):
        return None


class TestCrukReport(unittest.TestCase):

    def setUp(self): #-> None:
        self.rc = ReportCruk(True)


    # Tests for data parsed out into dictionary


    # Tests for XML generated
    def pass_xml_test(self):
        '''
        Test if newly generated xml for a sample which passed QC and was sequenced matches an existing xml
        :return:
        '''

        # Load in template xml


        # Load in generated xml


        return None

    def fail_xml_test(self):
        return None

    def withdrawn_xml_test(self):
        return None


    # Check PDF is correctly named



if __name__ == '__main__':
    unittest.main()

