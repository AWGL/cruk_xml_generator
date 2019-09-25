import datetime
import logging

ch_dict = {"Birmingham": "1 - Birmingham", "Cardiff":"2 - Cardiff", "Cambridge":"3 - Cambridge",
                "Edinburgh":"4 - Edinburgh", "Glasgow":"5 - Glasgow", "Leeds":"6 - Leeds",
                "Manchester":"7 - Manchester", "Royal Marsden":"8 - Royal Marsden",
                "Barts & Brighton":"9 – Barts & Brighton", "Belfast":"10 – Belfast", "Imperial":"11 – Imperial",
                "KCL":"12 - KCL", "Leicester":"13 – Leicester", "Newcastle":"14 – Newcastle",
                "Oxford":"15 – Oxford", "Sheffield":"16 – Sheffield", "Southampton":"17 – Southampton",
                "UCL":"18 - UCL", "Maidstone":"19 - Maidstone", "Devon and Exeter":"20 - Devon and Exeter",
                "Liverpool":"21 - Liverpool", "Bristol":"22 - Bristol", "Colchester":"23 - Colchester",
                "Aberdeen":"24 - Aberdeen", "1 - Birmingham": "1 - Birmingham", "2 - Cardiff":"2 - Cardiff",
                "3 - Cambridge":"3 - Cambridge", "4 - Edinburgh":"4 - Edinburgh", "5 - Glasgow":"5 - Glasgow",
                "6 - Leeds":"6 - Leeds", "7 - Manchester":"7 - Manchester", "8 - Royal Marsden":"8 - Royal Marsden",
                "9 - Barts & Brighton":"9 – Barts & Brighton", "10 - Belfast":"10 – Belfast",
                "11 - Imperial":"11 – Imperial", "12 - KCL":"12 - KCL", "13 - Leicester":"13 – Leicester",
                "14 - Newcastle":"14 – Newcastle", "15 - Oxford":"15 – Oxford", "16 - Sheffield":"16 – Sheffield",
                "17 - Southampton":"17 – Southampton", "18 - UCL":"18 - UCL", "19 - Maidstone":"19 - Maidstone",
                "20 - Devon and Exeter":"20 - Devon and Exeter", "21 - Liverpool":"21 - Liverpool",
                "22 - Bristol":"22 - Bristol", "23 - Colchester":"23 - Colchester", "24 - Aberdeen":"24 - Aberdeen"}

st_dict = {"blood":"1", "tissue-resection":"3", "tissue-bronchoscopicbiopsy":"8", "tissue-ctguidedbiopsy":"9",
            "tissue-surgicalbiopsy":"10", "tissue-otherbiopsy":"11", "cytologycellblock-ebus/eusfna":"12",
            "cytologycellblock-bronchoscopicwashing":"13", "cytologycellblock-ctguided":"14",
            "cytologycellblock-effusion":"15", "cytologycellblock-other":"16", "extracteddna":"17", "dna":"17"}

tumour_type_dict = {"Breast":"1", "Colorectal":"2", "Lung":"3", "Melanoma":"4", "Ovarian":"5", "Prostate":"6"}

genes_dict = {"BRAF":"1", "ALK": "4", "PIK3CA":"5", "PTEN":"6", "PTEN LOH":"7", "TP53":"8", "KIT":"9", "NRAS":"10",
         "DDR2":"11", "TMPRSS2-ERG":"12", "EGFR":"13", "KRAS":"14", "AKT1":"15", "CCND1":"16", "CDK4":"17",
         "CDKN2A":"18", "CDKN2B":"19", "FGFR1":"20", "FGFR2":"21", "FGFR3":"22", "HER2":"23", "JAK2":"24",
         "KDR":"25", "MET":"26", "NF1":"27", "P16":"28", "PDL-1":"29", "RB1":"30", "RET":"31", "ROS1":"32",
         "STAT3":"33", "STK11/LKB1":"34", "STK11":"34", "LKB1":"34", "TSC1":"35", "TSC2":"36", "HRAS":"37",
         "CCND2":"38", "CCND3":"39", "CCNE1":"40", "CDK2":"41", "NTRK1":"42", "BRCA1":"43", "BRCA2":"44",
         "ATM":"45", "BRIP1":"46", "PALB2":"47", "RAD51C":"48", "BARD1":"49", "CDK12":"50", "CHEK1":"51",
         "CHEK2":"52", "FANCL":"53", "PPP2R2A":"54", "RAD51B":"55", "RAD51D":"56", "RAD54L":"57", "ARID1A":"58"}

test_status_dict = {"Success":"1", "Partial Fail": "2", "Complete Fail":"3", "Not tested":"4"}


def valid_clinical_hub():
    valid = ch_dict.values()
    return valid

def valid_gender():
    valid = ["0 - Not Known", "1 - Male", "2 - Female", "9 - Not Specified" ]
    return valid

def valid_ethinicity():
    valid = ["A - White British", "B - White Irish", "C - Any other White background",
                "D - White and Black Caribbean", "E - White and Black African", "F - White and Asian",
                "G - Any other mixed background", "H - Indian", "J - Pakistani", "K - Bangladeshi",
                "L - Any other Asian background", "M - Caribbean", "N - African", "P - Any other Black background",
                "R - Chinese", "S - Any other ethnic group", "Z - Not stated", "99 - Not known"]
    return valid

def valid_smoking():
    valid = ["1 - Current smoker", "2 - Ex smoker", "3 - Non-smoker - history unknown", "4 - Never smoked",
                    "Z - Not Stated (PERSON asked but declined to provide a response)", "9 - Unknown"]
    return valid

def valid_therapy():
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

def valid_performance():
    valid = ["0 - Able to carry out all normal activity without restriction",
                "1 - Restricted in physically strenuous activity, but able to walk and do light work",
                "2 - Able to walk and capable of all self care, but unable to carry out any work. Up and about more \
                 than 50% of waking hours",
                "3 - Capable of only limited self care, confined to bed or chair more than 50% of waking hours",
                "4 - Completely disabled. Cannot carry on any self care. Totally confined to bed or chair",
                "9 - Not recorded"]
    return valid

def valid_sample_source():
    valid = ["1 - Primary tumour", "2 - Metastatic site – lymph node", "3 - Metastatic site – other"]
    return valid

def valid_sample_type():
    valid = st_dict.values()
    return valid

def valid_sample_procedure():
    valid = ["1 - CT guided biopsy", "2 - US guided biopsy", "3 - Surgical lung biopsy", "4 - Surgical resection",
                "5 - EBUS", "6 - EUS", "7 - Other biopsy", "8 - Other FNA cytology"]
    return valid

def valid_sample_biopsy():
    valid = ["0 - unknown", "1 - Diagnositc biopsy", "2 - Repeat biopsy due to sample test failure",
                "3 - Repeat biopsy due to lack of sample after local testing",
                "4 - Mandatory repeat biopsy after targeted first line therapy",
                "5 - Repeat biopsy due to non actionable mutation in diagnostic biopsy",
                "6 - Voluntary repeat biopsy after first line therapy",
                "7 - Voluntary repeat biopsy after targetted therapy"]
    return valid

def valid_date(the_date):
    try:
        if the_date != datetime.datetime.strptime(the_date, '%Y-%m-%d').strftime('%Y-%m-%d'):
            raise ValueError
    except ValueError:
        raise Exception(f"Incorrectly formatted date, {the_date} not formatted as YYYY-MM-DD")
    return True

def valid_tumour_type():
    valid = tumour_type_dict.values()
    return valid

def valid_pathology_t_cat(sample_date):
    if sample_date < "1/1/2018":
        valid = ["0 - unknown", "TX - Primary tumour cannot be assessed", "T0 - No evidence of primary tumour",
                     "Tis - Carcinoma in situ", "T1a - Tumour ≤20 mm diameter", "T1b - Tumour > 20–≤30 mm",
                     "T2 - Tumour >= 20 mm from the carina, invades visceral pleura, partial atelectasis",
                     "T2a - > 30–≤50 mm", "T2b - > 50–≤70 mm", "T3 - > 70 mm; involvement of parietal pleura, \
                      mediastinal pleura, chest wall, pericardium or diaphragm; tumour within 20 mm of the carina; \
                      atelectasis / obstructive pneumonitis involving whole lung; separate nodule(s) in the same lobe",
                     "T4 - Involvement of great vessels, mediastinum, carina, trachea, oesophagus, vertebra, or heart \
                      Separate tumour nodule(s) in different ipsilateral lobe", "9 - not applicable"]
    elif sample_date >= "1/1/2018":
        valid = ["0 - Unknown", "TX - Primary tumour cannot be assessed", "T0 - No evidence of primary tumour",
                     "Tis - Carcinoma in situ", "T1a - Tumour <= 10 mm", "T1b - Tumour > 10–=20 mm",
                     "T1c - Tumour > 20–=30 mm", "T1mi - Minimally invasive adenocarcinoma", "T2 - > 30–=50 mm",
                     "T2a - > 30–=40 mm", "T2b - > 40–=50 mm", "T3 - > 50–=70 mm", "T4 - > 70 mm", "9 - Not applicable"]
    else:
        raise Exception(f"Date {sample_date} is not in valid format")
    return valid

def valid_pathology_n_cat():
    valid = ["0 - unknown", "NX - Regional lymph nodes cannot be assessed", "N0 - No regional node involvement",
                 "N1 - Ipsilateral hilar/intrapulmonary nodes (node stations 10–14)",
                 "N2 - Ipsilateral mediastinal nodes (node stations 1–9)",
                 "N3 - Contralateral mediastinal, hilar, ipsilateral or contralateral scalene, supraclavicular nodes",
                 "9 - not applicable"]
    return valid

def valid_pathology_m_cat(sample_date):
    if sample_date < "1/1/2018":
        valid = ["0 - unknown", "M0 - No distant metastasis", "M1 - Distant metastasis",
                     "M1a - Separate tumour nodule(s) in a contralateral lobe; pleural nodules or malignant \
                     pleural or pericardial effusion.", "M1b - Distant metastasis", "9 - not applicable"]
    elif sample_date >= "1/1/2018":
        valid = ["0 - Unknown", "M0 - No distant metastasis", "M1 - Distant metastasis",
                     "M1a - Separate tumour nodule(s) in a contralateral lobe; pleural nodules or malignant \
                     pleural or pericardial effusion", "M1b - Single extrathoracic metastasis in a single organ \
                     and involvement of a single distant (non-regional) lymph node", "M1c - Multiple extrathoracic \
                     metastases in one or several organs", "9 - Not applicable"]
    else:
        raise Exception(f"Date {sample_date} is not in valid format")
    return valid

def valid_alk_status():
    valid = ["P-positive", "N-negative", "E-equivocal", "X-not known", "Z-not performed",
                 "U-technically unsatisfactory"]
    return valid

def valid_egfr_status():
    valid = ["M-mutation detected", "N-no mutation detected", "X-not known", "F-test failure", "Z-not performed",
                 "Y-other result"]
    return valid

def valid_alk_fish_status():
    valid = ["R-rearrangement detected", "N-no rearrangement detected", "X-not known", "F-test failure",
                 "Z-not performed", "Y-other result"]
    return valid

def valid_kras_status():
    valid = ["M-mutation detected", "N-no mutation detected", "X-not known", "F-test failure", "Z-not performed",
                 "Y-other result"]
    return valid

def valid_tech_hub():
    valid = ["1 - Birmingham", "2 - Cardiff", "3 - Royal Marsden"]
    return valid

def valid_gene():
    valid = genes_dict.values()
    return valid

def valid_method():
    '''
    valid = ["1 - FISH", "2 - MICROSAT", "3 - RQ - PCR", "4 - SEQUENCING", "5 - DIRECT SEQUENCING",
                 "6 - PYROSEQUENCING", "7 - HRM-HIGH RESOLUTION MELT", "8 - ARMS", "9 - CE - SSCA", "10 - COBAS 4800",
                 "11 - SNAPSHOT", "12 - RT - PCR", "13 - FRAGMENT LENGTH", "14 - Other", "15 - Illumina NGS panel 1",
                 "16 - Illumina NGS panel 2", "17 - Illumina NGS panel 3", "18 - Illumina NGS panel 4",
                 "19 - Illumina NGS TST170 Panel 43 of 170", "20 - Illumina NGS TST170 Panel"]
    '''
    valid = ["1","2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19",
             "20"]
    return valid

def valid_test_status():
    valid = test_status_dict.values()
    return valid






















