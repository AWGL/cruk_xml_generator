
class ValidData:

    def __init__(self):
        self.p = None

    def valid_clinical_hub(self):
        valid = ["1 - Birmingham", "2 - Cardiff", "3 - Cambridge", "4 - Edinburgh", "5 - Glasgow", "6 - Leeds",
                    "7 - Manchester", "8 - Royal Marsden", "9 – Barts & Brighton", "10 – Belfast", "11 – Imperial",
                    "12 - KCL", "13 – Leicester", "14 – Newcastle", "15 – Oxford", "16 – Sheffield", "17 – Southampton",
                    "18 - UCL"]
        return valid

    def valid_gender(self):
        valid = ["0 - Not Known", "1 - Male", "2 - Female", "9 - Not Specified" ]
        return valid

    def valid_ethinicity(self):
        valid = ["A - White British", "B - White Irish", "C - Any other White background",
                    "D - White and Black Caribbean", "E - White and Black African", "F - White and Asian",
                    "G - Any other mixed background", "H - Indian", "J - Pakistani", "K - Bangladeshi",
                    "L - Any other Asian background", "M - Caribbean", "N - African", "P - Any other Black background",
                    "R - Chinese", "S - Any other ethnic group", "Z - Not stated", "99 - Not known"]
        return valid

    def valid_smoking(self):
        valid = ["1 - Current smoker", "2 - Ex smoker", "3 - Non-smoker - history unknown", "4 - Never smoked",
                    "Z - Not Stated (PERSON asked but declined to provide a response)", "9 - Unknown"]
        return valid

    def valid_therapy(self):
        valid = ["01 - Surgery", "02 - Anti-cancer drug regimen (Cytotoxic Chemotherapy)",
                    "03 - Anti-cancer drug regimen (Hormone Therapy)", "04 - Chemoradiotherapy",
                    "05 - Teletherapy (Beam Radiation excluding Proton Therapy)", "06 - Brachytherapy",
                    "07 - Specialist Palliative Care",
                    "08 - Active Monitoring (excluding non-specialist Palliative Care)",
                    "09 - Non-specialist Palliative Care (excluding Active Monitoring)",
                    "10 - Radio Frequency Ablation (RFA)", "11 - High Intensity Focussed Ultrasound (HIFU)",
                    "12 - Cryotherapy", "13 - Proton Therapy", "14 - Anti-cancer drug regimen (other)",
                    "15 - Anti-cancer drug regimen (Immunotherapy)",
                    "16 - Light Therapy (including Photodynamic Therapy and Psoralen and Ultra Violet A (PUVA) Therapy)",
                    "17 - Hyperbaric Oxygen Therapy", "19 - Radioisotope Therapy (including Radioiodine)",
                    "20 - Laser Treatment (including Argon Beam therapy)",
                    "21 - Biological Therapies (excluding Immunotherapy)", "22 - Radiosurgery", "97 - Other Treatment",
                    "98 - All treatment declined", "99 - No treatment"]
        return valid

    def valid_performance(self):
        valid = ["0 - Able to carry out all normal activity without restriction",
                    "1 - Restricted in physically strenuous activity, but able to walk and do light work",
                    "2 - Able to walk and capable of all self care, but unable to carry out any work. Up and about more than 50% of waking hours",
                    "3 - Capable of only limited self care, confined to bed or chair more than 50% of waking hours",
                    "4 - Completely disabled. Cannot carry on any self care. Totally confined to bed or chair",
                    "9 - Not recorded"]
        return valid

    def valid_sample_source(self):
        valid = ["1 - Primary tumour", "2 - Metastatic site – lymph node", "3 - Metastatic site – other"]
        return valid

    def valid_sample_type(self):
        valid = ["1 - Blood", "3 - Tissue- Resection", "8 - Tissue- Bronchoscopic biopsy",
                    "9 - Tissue- CT guided biopsy", "10 - Tissue- Surgical biopsy", "11 - Tissue- Other biopsy",
                    "12 - Cytology cell block- EBUS/EUS FNA", "13 - Cytology cell block- Bronchoscopic washing",
                    "14 - Cytology cell block- CT guided", "15 - Cytology cell block- Effusion",
                    "16 - Cytology cell block- Other", "17 - Extracted DNA"]
        return valid

    def valid_sample_procedure(self):
        valid = ["1 - CT guided biopsy", "2 - US guided biopsy", "3 - Surgical lung biopsy", "4 - Surgical resection",
                    "5 - EBUS", "6 - EUS", "7 - Other biopsy", "8 - Other FNA cytology"]
        return valid

    def valid_sample_biopsy(self):
        valid = ["0 - unknown", "1 - Diagnositc biopsy", "2 - Repeat biopsy due to sample test failure",
                    "3 - Repeat biopsy due to lack of sample after local testing",
                    "4 - Mandatory repeat biopsy after targeted first line therapy",
                    "5 - Repeat biopsy due to non actionable mutation in diagnostic biopsy",
                    "6 - Voluntary repeat biopsy after first line therapy",
                    "7 - Voluntary repeat biopsy after targetted therapy"]
        return valid

    def valid_sample_date(self):
        #TODO implement this- format YYYY-MM-DD
        return None

    def valid_tumour_type(self):
        valid = [Value List:
 - "1 - Breast"
 - "2 - Colorectal"
 - "3 - Lung"
 - "4 - Melanoma"
 - "5 - Ovarian"
 - "6 - Prostate"
 - "7 - Other" ]
        return valid

    def valid_pathology_t_cat(self):
        Value
        List
        IF
        date
        sample
        taken is before
        1 / 1 / 2018(TNM7):
        0 - unknown
        TX - Primary
        tumour
        cannot
        be
        assessed
        T0 - No
        evidence
        of
        primary
        tumour
        Tis - Carcinoma in situ
        T1a - Tumour ≤20
        mm
        diameter
        T1b - Tumour > 20–≤30
        mm
        T2 - Tumour >= 20
        mm
        from the carina, invades
        visceral
        pleura, partial
        atelectasis
        T2a - > 30–≤50
        mm
        T2b - > 50–≤70
        mm
        T3 - > 70
        mm;
        involvement
        of
        parietal
        pleura, mediastinal
        pleura, chest
        wall, pericardium or
        diaphragm;
        tumour
        within
        20
        mm
        of
        the
        carina;
        atelectasis / obstructive
        pneumonitis
        involving
        whole
        lung;
        separate
        nodule(s) in the
        same
        lobe
        T4 - Involvement
        of
        great
        vessels, mediastinum, carina, trachea, oesophagus, vertebra, or heart
        Separate
        tumour
        nodule(s) in different
        ipsilateral
        lobe
        9 -
        not applicable

        Value
        List
        OTHERWISE
        ie if date
        sample
        taken is on or after
        1 / 1 / 2018(TNM8):
        0 - Unknown
        TX - Primary
        tumour
        cannot
        be
        assessed
        T0 - No
        evidence
        of
        primary
        tumour
        Tis - Carcinoma in situ
        T1a - Tumour <= 10
        mm
        T1b - Tumour > 10–=20
        mm
        T1c - Tumour > 20–=30
        mm
        T1mi - Minimally
        invasive
        adenocarcinoma
        T2 - > 30–=50
        mm
        T2a - > 30–=40
        mm
        T2b - > 40–=50
        mm
        T3 - > 50–=70
        mm
        T4 - > 70
        mm
        9 - Not
        applicable

    def valid_pathology_n_cat(self):
        valid = [Value List:
0 - unknown
NX - Regional lymph nodes cannot be assessed
N0 - No regional node involvement
N1 - Ipsilateral hilar/intrapulmonary nodes (node stations 10–14)
N2 - Ipsilateral mediastinal nodes (node stations 1–9)
N3 - Contralateral mediastinal, hilar, ipsilateral or contralateral scalene, supraclavicular nodes
9 - not applicable]
        return valid

        def valid_pathology_m_cat(self):
            valid = [Value List IF date sample taken is before 1/1/2018 (TNM7):
0 - unknown
M0 - No distant metastasis
M1 - Distant metastasis
M1a - Separate tumour nodule(s) in a contralateral lobe; pleural nodules or malignant pleural or
pericardial effusion.
M1b - Distant metastasis
9 - not applicable

Value List OTHERWISE ie if date sample taken is on or after 1/1/2018 (TNM8):
0 - Unknown
M0 - No distant metastasis
M1 - Distant metastasis
M1a - Separate tumour nodule(s) in a contralateral lobe; pleural nodules or malignant pleural or pericardial effusion
M1b - Single extrathoracic metastasis in a single organ and involvement of a single distant (non-regional) lymph node
M1c - Multiple extrathoracic metastases in one or several organs
9 - Not applicable]
            return valid




















