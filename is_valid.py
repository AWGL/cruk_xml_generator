from lxml import etree as ET
import logging

class IsValid(object):

    def __init__(self, input, validate_dict=None):
        self.validate_dict = {"smClinicalHub":"clinical_hub", "organisationCode":"org_code"}
        self.input = input
        #self.field = None
        #print(ET.tostring(self.input, encoding="UTF-8"))
        #print(self.input.find(".//smClinicalHub"))

    def itera(self):
        for elem in self.input.iter():
            print(elem.tag)
            method_name = self.validate_dict.get(elem.tag, "Not in dict")
            print(method_name)
            print(self.select_method(method_name))

    def select_method(self, method_name):
        method = getattr(self, method_name, lambda: "Not found")
        #field = self.input.find(f".//{to_find}")
        #print(field)
        return method() #self.field

    def clinical_hub(self):
        from valid_data import valid_clinical_hub as validate
        #selected = self.select_field("smClinicalHub")
        print("testing")
        #print(selected)
        #valid = self.field in validate
        valid = True
        if valid:
            logging.info("smClinicalHub OK")
        else:
            raise Exception
        return "executed clinical_hub"

    def org_code(self):
        if not isinstance(self.input ,str):
            raise Exception("smClinicalHub/patient/organisationCode is not a string")
        if len(self.input) > 5:
            raise Exception("smClinicalHub/patient/organisationCode is longer than 5 characters")
        return None

    def loc_pat_id(self):
        if not isinstance(self.input ,str):
            raise Exception("smClinicalHub/patient/localPatientIdentifier is not a string")
        if len(self.input) > 10:
            raise Exception("smClinicalHub/patient/localPatientIdentifier is longer than 10 characters")
        return None

    def onc_initials(self):
        # Optional for TH
        if not isinstance(self.input, str):
            raise Exception("smClinicalHub/patient/treatingOncologistInitials is not a string")
        if len(self.input) > 3:
            raise Exception("smClinicalHub/patient/treatingOncologistInitials is longer than 3 characters")
        return None

    def age_attendance(self):
        # Optional for TH
        if not isinstance(self.input, int):
            raise Exception("smClinicalHub/patient/ageAtAttendance is not a string")
        if len(str(abs(self.input))) > 3:
            raise Exception("smClinicalHub/patient/ageAtAttendance is longer than 3 digits")
        return None

    def current_gender(self):
        # Optional for TH
        ValidData.valid_gender(0)
        #if val in
        valid = None
        if valid:
            logging.info("smClinicalHub/patient/genderCode OK")
        else:
            raise Exception
        return None

    def ethnic_category(self):
        # Optional for TH
        ValidData.valid_ethinicity(0)
        #if val in
        valid = None
        if valid:
            logging.info("smClinicalHub/patient/ethnicCategory OK")
        else:
            raise Exception
        return None

    def smoking(self):
        # Optional for TH
        ValidData.valid_smoking(0)
        #if val in
        valid = None
        if valid:
            logging.info("smClinicalHub/patient/smokingStatus OK")
        else:
            raise Exception
        return None

    def prior_therapy_num(self):
        # Optional for TH
        if not isinstance(self.input, str):
            raise Exception("smClinicalHub/patient/noOfPriorLinesTherapy is not a string")
        if len(self.input) > 5:
            raise Exception("smClinicalHub/patient/noOfPriorLinesTherapy is longer than 5 characters")
        return None

    def treatment_modality(self):
        # Optional for TH
        ValidData.valid_therapy(0)
        #if val in
        valid = None
        if valid:
            logging.info("smClinicalHub/patient/cancerTreatmentModality OK")
        else:
            raise Exception
        return None

    def perf_status(self):
        # Optional for TH
        ValidData.valid_performance(0)
        # if val in
        valid = None
        if valid:
            logging.info("smClinicalHub/patient/performanceStatus OK")
        else:
            raise Exception
        return None

    def sample_id(self):
        if not isinstance(self.input, str):
            raise Exception("sample/clinicalHubElements/sourceSampleIdentifier is not a string")
        if len(self.input) > 20:
            raise Exception("sample/clinicalHubElements/sourceSampleIdentifier is longer than 20 characters")
        return None

    def sample_source(self):
        ValidData.valid_sample_source(0)
        # if val in
        valid = None
        if valid:
            logging.info("sample/clinicalHubElements/originOfSample OK")
        else:
            raise Exception
        return None

    def sample_type(self):
        ValidData.valid_sample_type(0)
        # if val in
        valid = None
        if valid:
            logging.info("sample/clinicalHubElements/typeOfSample OK")
        else:
            raise Exception
        return None

    def sample_procedure(self):
        # Optional for TH
        ValidData.valid_sample_type(0)
        # if val in
        valid = None
        if valid:
            logging.info("sample/clinicalHubElements/procedureToObtainSample OK")
        else:
            raise Exception
        return None

    def sample_biopsy(self):
        # Optional for TH
        ValidData.valid_sample_biopsy(0)
        # if val in
        valid = None
        if valid:
            logging.info("sample/clinicalHubElements/typeOfBiopsy OK")
        else:
            raise Exception
        return None

    def sample_date(self):
        # Optional for TH
        ValidData.valid_date(0)
        # if val in
        valid = None
        if valid:
            logging.info("sample/clinicalHubElements/dateSampleTaken OK")
        else:
            raise Exception
        return None

    def tumour_type(self):
        ValidData.valid_tumour_type(0)
        # if val in
        valid = None
        if valid:
            logging.info("sample/clinicalHubElements/tumourType OK")
        else:
            raise Exception
        return None

    def morphology_snomed(self):
        if not isinstance(self.input, ET.CDATA):
            raise Exception("sample/clinicalHubElements/morphologySnomed is not a string")
        if len(self.input) > 18: #TODO fix this line to work with CDATA
            raise Exception("sample/clinicalHubElements/morphologySnomed is longer than 18 characters")
        return None

    def pathology_t_cat(self):
        # Optional for TH
        ValidData.valid_pathology_t_cat(0)
        # if val in
        valid = None
        if valid:
            logging.info("sample/clinicalHubElements/pathologyTCategory OK")
        else:
            raise Exception
        return None

    def pathology_n_cat(self):
        # Optional for TH
        ValidData.valid_pathology_n_cat(0)
        # if val in
        valid = None
        if valid:
            logging.info("sample/clinicalHubElements/pathologyNCategory OK")
        else:
            raise Exception
        return None

    def pathology_m_cat(self):
        # Optional for TH
        ValidData.valid_pathology_m_cat(0)
        # if val in
        valid = None
        if valid:
            logging.info("sample/clinicalHubElements/pathologyMCategory OK")
        else:
            raise Exception
        return None

    def tnm_stage_grouping(self):
        # Optional for TH
        if not isinstance(self.input, str):
            raise Exception("sample/clinicalHubElements/integratedTNMStageGrouping is not a string")
        if len(self.input) > 5:
            raise Exception("sample/clinicalHubElements/integratedTNMStageGrouping is longer than 5 characters")
        return None

    def alk_status(self):
        # Optional for TH
        ValidData.valid_alk_status(0)
        # if val in
        valid = None
        if valid:
            logging.info("sample/clinicalHubElements/alkStatus OK")
        else:
            raise Exception
        return None

    def egfr_status(self):
        # Optional for TH
        ValidData.valid_egfr_status(0)
        # if val in
        valid = None
        if valid:
            logging.info("sample/clinicalHubElements/egfrStatus OK")
        else:
            raise Exception
        return None

    def alk_fish_status(self):
        # Optional for TH
        ValidData.valid_alk_fish_status(0)
        # if val in
        valid = None
        if valid:
            logging.info("sample/clinicalHubElements/alkFishStatus OK")
        else:
            raise Exception
        return None

    def kras_status(self):
        # Optional for TH
        ValidData.valid_kras_status(0)
        # if val in
        valid = None
        if valid:
            logging.info("sample/clinicalHubElements/krasStatus OK")
        else:
            raise Exception
        return None

    def sample_sent_date(self):
        ValidData.valid_date(0)
        # if val in
        valid = None
        if valid:
            logging.info("sample/clinicalHubElements/dateSampleSent OK")
        else:
            raise Exception
        return None

    def sample_received_date(self):
        ValidData.valid_date(0)
        # if val in
        valid = None
        if valid:
            logging.info("sample/clinicalHubElements/dateSampleReceived OK")
        else:
            raise Exception
        return None

    def lab_id(self):
        if not isinstance(self.input, str):
            raise Exception("sample/smClinicalHub/labSampleIdentifier is not a string")
        return None

    def report_release_date(self):
        #TODO get date of xml generation as that is this date
        ValidData.valid_date(0)
        # if val in
        valid = None
        if valid:
            logging.info("sample/technologyHubElements/reportReleaseDate OK")
        else:
            raise Exception
        return None

    def vol_banked_nuc_acid(self):
        if not isinstance(self.input, ET.CDATA):
            raise Exception("sample/technologyHubElements/volumeBankedNucleicAcid is not correctly formatted as CDATA")
        if self.input != 0: # Zero is permitted for samples not banked #TODO fix this line to work with CDATA
            try:
                len_list = self.input.split(".")  #TODO fix this line to work with CDATA
            except:
                raise Exception(f"Unexpected format for sample/technologyHubElements/volumeBankedNucleicAcid \
                                 {self.input}. Should contain a . or be 0")
            if len(len_list[0]) > 3: #TODO fix this line to work with CDATA
                raise Exception("sample/technologyHubElements/volumeBankedNucleicAcid integer part is longer than 3 \
                                 digits")
            if len(len_list[1]) > 4:
                raise Exception("sample/technologyHubElements/volumeBankedNucleicAcid decimal part is longer than 4 \
                                 digits")
        return None

    def conc_banked_nuc_acid(self):
        if not isinstance(self.input, str):
            raise Exception("sample/technologyHubElements/concentrationBankedNucleicAcid is not a string")
        if self.input != 0: # Zero is permitted for samples not banked
            try:
                len_list = self.input.split(".")
            except:
                raise Exception(f"Unexpected format for sample/technologyHubElements/volumeBankedNucleicAcid \
                                 {self.input}. Should contain a . or be 0")
            if len(len_list[0]) > 3:
                raise Exception("sample/technologyHubElements/concentrationBankedNucleicAcid integer part is longer \
                                 than 3 digits")
            if len(len_list[1]) > 4:
                raise Exception("sample/technologyHubElements/concentrationBankedNucleicAcid decimal part is longer \
                                than 4 digits")
        return None

    def loc_banked_nuc_acid(self):
        # Optional for TH
        #TODO Check is the same as the technology hub name
        if not isinstance(self.input, str):
            raise Exception("sample/technologyHubElements/bankedNucleicAcidLocation is not a string")
        if len(self.input) > 50:
            raise Exception("sample/technologyHubElements/bankedNucleicAcidLocation is longer than 50 characters")
        return None

    def id_banked_nuc_acid(self):
        # Optional for TH
        if not isinstance(self.input, str):
            raise Exception("sample/technologyHubElements/bankedNucleicAcidIdentifier is not a string")
        if len(self.input) > 10:
            raise Exception("sample/technologyHubElements/bankedNucleicAcidIdentifier is longer than 10 characters")
        return None

    def tech_hub(self):
        #TODO Need to access the attribute from within this element to check
        #TODO NB XSD type is string and no value list has been enforced
        ValidData.valid_tech_hub(0)
        # if val in
        valid = None
        if valid:
            logging.info("smTechnologyHub OK")
        else:
            raise Exception
        return None

    def gene(self):
        ValidData.valid_gene(0)
        # if val in
        valid = None
        if valid:
            logging.info("smTechnologyHub/testResults/test/gene OK")
        else:
            raise Exception
        return None

    def method(self):
        ValidData.valid_method(0)
        # if val in
        valid = None
        if valid:
            logging.info("smTechnologyHub/testResults/test/methodOfTest OK")
        else:
            raise Exception
        return None

    def scope(self):
        if not isinstance(self.input, ET.CDATA):
            raise Exception("smTechnologyHub/testResults/test/scopeOfTest is not correctly formatted as CDATA")
        if len(self.input) > 200:  # TODO fix this line to work with CDATA
            raise Exception("smTechnologyHub/testResults/test/scopeOfTest is longer than 200 characters")
        return None

    def test_results_date(self):
        # TODO If all test results released this date should be set to same as report release date
        ValidData.valid_date(0)
        # if val in
        valid = None
        if valid:
            logging.info("smTechnologyHub/testResults/test/dateTestResultsReleased OK")
        else:
            raise Exception
        return None

    def test_results(self):
        #TODO Multiple mutations should be separated by a semicolon
        if not isinstance(self.input, ET.CDATA):
            raise Exception("smTechnologyHub/testResults/test/testResult is not correctly formatted as CDATA")
        if len(self.input) > 600:  # TODO fix this line to work with CDATA
            raise Exception("smTechnologyHub/testResults/test/testResult is longer than 600 characters")
        return None

    def test_report(self):
        if not isinstance(self.input, ET.CDATA):
            raise Exception("smTechnologyHub/testResults/test/testReport is not correctly formatted as CDATA")
        if len(self.input) > 600:  # TODO fix this line to work with CDATA
            raise Exception("smTechnologyHub/testResults/test/testReport is longer than 600 characters")
        return None

    def test_status(self):
        ValidData.valid_test_status(0)
        # if val in
        valid = None
        if valid:
            logging.info("smTechnologyHub/testResults/test/dateTestResultsReleased OK")
        else:
            raise Exception
        return None

    def comments(self):
        if not isinstance(self.input, ET.CDATA):
            raise Exception("smTechnologyHub/testResults/test/comments is not correctly formatted as CDATA")
        if len(self.input) > 600:  # TODO fix this line to work with CDATA
            raise Exception("smTechnologyHub/testResults/test/comments is longer than 600 characters")
        return None






















