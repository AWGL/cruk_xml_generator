import logging
import re
from valid_data import ValidData
from t import valid_clinical_hub

class IsValid:
    def __init__(self, input):
        self. input = input
        self.data = ValidData()

    def select_field(self):
        return None


    def clinical_hub(self):
        ValidData.valid_clinical_hub(0)
        #if val in
        valid = None
        if valid:
            logging.info("smClinicalHub OK")
        else:
            raise Exception
        return None

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
        if len(str(abs(self.input))) > 5:
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
        if len(str(abs(self.input))) > 20:
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
        if not isinstance(self.input, str):
            raise Exception("sample/clinicalHubElements/dateSampleTaken is not a string")
        if len(str(abs(self.input))) > 20:
            raise Exception("sample/clinicalHubElements/dateSampleTaken is longer than 20 characters")
        return None






















