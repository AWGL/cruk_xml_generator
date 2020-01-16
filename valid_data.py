"""'
Contains dictionaries for look-up to required output for XML
"""


ch_dict = {"Birmingham": "1 - Birmingham", "Cardiff": "2 - Cardiff", "Cambridge": "3 - Cambridge",
           "Edinburgh": "4 - Edinburgh", "Glasgow": "5 - Glasgow", "Leeds": "6 - Leeds",
           "Manchester": "7 - Manchester", "Royal Marsden": "8 - Royal Marsden",
           "Barts & Brighton": "9 - Barts & Brighton", "Belfast": "10 - Belfast", "Imperial": "11 - Imperial",
           "KCL": "12 - KCL", "Leicester": "13 - Leicester", "Newcastle": "14 - Newcastle",
           "Oxford": "15 - Oxford", "Sheffield": "16 - Sheffield", "Southampton": "17 - Southampton",
           "UCL": "18 - UCL", "Maidstone": "19 - Maidstone", "Devon and Exeter": "20 - Devon and Exeter",
           "Liverpool": "21 - Liverpool", "Bristol": "22 - Bristol", "Colchester": "23 - Colchester",
           "Aberdeen": "24 - Aberdeen", "1": "1 - Birmingham", "2": "2 - Cardiff",
           "3": "3 - Cambridge", "4": "4 - Edinburgh", "5": "5 - Glasgow",
           "6": "6 - Leeds", "7": "7 - Manchester", "8": "8 - Royal Marsden",
           "9": "9 - Barts & Brighton", "10": "10 - Belfast",
           "11": "11 - Imperial", "12": "12 - KCL", "13": "13 - Leicester",
           "14": "14 - Newcastle", "15": "15 - Oxford", "16": "16 - Sheffield",
           "17": "17 - Southampton", "18": "18 - UCL", "19": "19 - Maidstone",
           "20": "20 - Devon and Exeter", "21": "21 - Liverpool",
           "22": "22 - Bristol", "23": "23 - Colchester", "24": "24 - Aberdeen"}

st_dict = {"1-blood": "1", "3-tissue-resection": "3", "8-tissue-bronchoscopicbiopsy": "8",
           "9-tissue-ctguidedbiopsy": "9", "10-tissue-surgicalbiopsy": "10", "11-tissue-otherbiopsy": "11",
           "12-cytologycellblock-ebus/eusfna": "12", "13-cytologycellblock-bronchoscopicwashing": "13",
           "14-cytologycellblock-ctguided": "14", "15-cytologycellblock-effusion": "15",
           "16-cytologycellblock-other": "16", "17-extracteddna": "17", "17-dna": "17"}

tumour_type_dict = {"1 - Breast": "1", "2 - Colorectal": "2", "3 - Lung": "3", "4 - Melanoma": "4", "5 - Ovarian": "5",
                    "6 - Prostate": "6"}

genes_dict = {"BRAF": "1", "ALK": "4", "PIK3CA": "5", "PTEN": "6", "PTEN LOH": "7", "TP53": "8", "KIT": "9",
              "NRAS": "10", "DDR2": "11", "TMPRSS2-ERG": "12", "EGFR": "13", "KRAS": "14", "AKT1": "15", "CCND1": "16",
              "CDK4": "17", "CDKN2A": "18", "CDKN2B": "19", "FGFR1": "20", "FGFR2": "21", "FGFR3": "22", "HER2": "23",
              "ERBB2": "23", "JAK2": "24", "KDR": "25", "MET": "26", "NF1": "27", "P16": "28", "PDL-1": "29",
              "RB1": "30", "RET": "31", "ROS1": "32", "STAT3": "33", "STK11/LKB1": "34", "STK11": "34", "LKB1": "34",
              "TSC1": "35", "TSC2": "36", "HRAS": "37", "CCND2": "38", "CCND3": "39", "CCNE1": "40", "CDK2": "41",
              "NTRK1": "42", "BRCA1": "43", "BRCA2": "44", "ATM": "45", "BRIP1": "46", "PALB2": "47", "RAD51C": "48",
              "BARD1": "49", "CDK12": "50", "CHEK1": "51", "CHEK2": "52", "FANCL": "53", "PPP2R2A": "54",
              "RAD51B": "55", "RAD51D": "56", "RAD54L": "57", "ARID1A": "58"}

test_status_dict = {"Success": "1", "Partial Fail": "2", "Complete Fail": "3", "Not Tested": "4"}

gene_scope_dict = {"AKT1": "ENST00000349310:Exons 3-15", "ALK": "ENST00000389048:Exons 1-29",
                   "BRAF": "ENST00000288602:Exons1-18", "CCND1": "ENST00000227507:Exons1-5",
                   "CCND2": "ENST00000261254:Exons1-5", "CCND3": "ENST00000372991:Exons1-5",
                   "CCNE1": "ENST00000262643:Exons2-11", "CDK4": "ENST00000257904:Exons2-7",
                   "CDKN2A": "ENST00000304494:Exons1-3", "EGFR": "ENST00000275493:Exons1-28",
                   "ERBB2": "ENST00000269571:Exons1-27", "FGFR2": "ENST00000358487:Exons2-18",
                   "FGFR3": "ENST00000440486:Exons2-18", "HRAS": "ENST00000397596:Exons2-5",
                   "KRAS": "ENST00000311936:Exons2-5", "MET": "ENST00000318493:Exons2-21",
                   "NF1": "ENST00000358273:Exons1-18,19,20,22-58", "NRAS": "ENST00000369535:Exons2-5",
                   "NTRK1": "ENST00000392302:Exons1-17", "PIK3CA": "ENST00000263967:Exons2-21",
                   "PTEN": "ENST00000371953:Exons1-9", "RB1": "ENST00000267163:Exons1-27",
                   "RET": "ENST00000355710:Exons1-20", "ROS1": "ENST00000368508:Exons1-43",
                   "STK11": "ENST00000326873:Exons1-9", "TSC1": "ENST00000298552:Exons3-23",
                   "TSC2": "ENST00000219476:Exons2-42","ARID1A": "ENST00000324856:Exons1-20",
                   "ATM": "ENST00000278616:Exons2-63", "BARD1": "ENST00000260947:Exons1-11",
                   "BRCA1": "ENST00000357654:Exons2-23", "BRCA2": "ENST00000380152:Exons2-27",
                   "BRIP1": "ENST00000259008:Exons2-20", "CDK12": "ENST00000447079:Exons1-14",
                   "CHEK1": "ENST00000438015:Exons2-13", "CHEK2": "ENST00000328354:Exons2-15",
                   "FANCL": "ENST00000233741:Exons1-14", "PALB2": "ENST00000261584:Exons1-13",
                   "PPP2R2A": "ENST00000380737:Exons1-10", "RAD51B": "ENST00000487270:Exons2-11",
                   "RAD51C": "ENST00000337432:Exons1-9", "RAD51D": "ENST00000345365:Exons1-10",
                   "RAD54L": "ENST00000371975:Exons1-18"}

output_xml_directory_name = {"1 - Birmingham": "Birmingham", "2 - Cardiff": "Cardiff",
           "3 - Cambridge": "Cambridge", "4 - Edinburgh": "Edinburgh", "5 - Glasgow": "Glasgow",
           "6 - Leeds": "Leeds", "7 - Manchester": "Manchester", "8 - Royal Marsden": "Marsden",
           "9 - Barts & Brighton": "BARTS", "10 - Belfast": "Belfast",
           "11 - Imperial": "Imperial", "12 - KCL": "KCL", "13 - Leicester": "Leicester",
           "14 - Newcastle": "Newcastle", "15 - Oxford": "Oxford", "16 - Sheffield": "Sheffield",
           "17 - Southampton": "Southampton", "18 - UCL": "UCL", "19 - Maidstone": "Maidstone",
           "20 - Devon and Exeter": "Exeter", "21 - Liverpool": "Liverpool",
           "22 - Bristol": "Bristol", "23 - Colchester": "Colchester", "24 - Aberdeen": "Aberdeen"}




















