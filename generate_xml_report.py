import os
from lxml import etree as ET


#TODO check validation with lxml

class GenerateXml:

    def __init__(self, info_dict):
        self.version = "3.8"
        self.input_path = "/Users/sararey/Documents/cruk_reporting/" #temp path for testing"
        self.output_path = "/Users/sararey/Documents/cruk_reporting/xml_report"  # temp path for testing"
        self.info_dict = info_dict


    def load_existing_xml(self, xml_file):
        tree = ET.parse(xml_file)
        root= tree.getroot()
        #print(root.tag) # XML rooted in this tag
        #print(root.attrib) # obtain attributes of root
        #for child in root:
            #print(child.tag, child.attrib)
            #for c in child:
                #print(c.tag)
        #[print(elem.tag, elem.attrib) for elem in root.iter()]
        #for sample in root.iter('smpSample'):
            #print(sample.text)
        #print(ET.tostring(root, encoding="UTF-8"))


    def generate_xml(self):
        NS_XSI = "{http://www.w3.org/2001/XMLSchema-instance}"
        root = ET.Element("smpSample")
        root.set(NS_XSI + "noNamespaceSchemaLocation",
                'http://extranet.cancerresearchuk.org/stratmed/Shared%20Documents/smSampleXSDSchema%20V2.3.xsd') #TODO Check this link correct

        ET.SubElement(root, "smVersion", smVersion=self.version)
        clinical_hub = ET.SubElement(root, "smClinicalHub", name=self.info_dict.get('clinical_hub'))
        patient = ET.SubElement(clinical_hub, "patient")
        org_code = ET.SubElement(patient, "organisationCode")
        org_code.text = self.info_dict.get('org_code')
        loc_pat_id = ET.SubElement(patient, "localPatientIdentifier")
        loc_pat_id.text = self.info_dict.get('local_patient_id')
        loc_pat_id_2 = ET.SubElement(patient, "localPatientIdentifier2")
        loc_pat_id_2.text = self.info_dict.get('local_patient_id_2')
        sample = ET.SubElement(root, "sample")
        clin_hub_elems = ET.SubElement(sample, "clinicalHubElements")
        source_id = ET.SubElement(clin_hub_elems, "sourceSampleIdentifier")
        source_id.text = self.info_dict.get('source_id')
        sample_type = ET.SubElement(clin_hub_elems, "typeOfSample")
        sample_type.text = self.info_dict.get('sample_type')
        morph_snomed =  ET.SubElement(clin_hub_elems, "morphologySnomed")
        morph_snomed.text = ET.CDATA(self.info_dict.get('morphology_snomed'))
        tum_type = ET.SubElement(clin_hub_elems, "tumourType")
        tum_type.text = self.info_dict.get('tumour_type')
        sample_sent_date = ET.SubElement(clin_hub_elems, "dateSampleSent")
        sample_sent_date.text = self.info_dict.get('date_sample_sent')
        tech_hub_elems = ET.SubElement(sample, "technologyHubElements")
        ET.SubElement(tech_hub_elems, "dateSampleReceived")
        lab_id = ET.SubElement(tech_hub_elems, "labSampleIdentifier")
        lab_id.text = self.info_dict.get('lab_id')
        release_date = ET.SubElement(tech_hub_elems, "reportReleaseDate")
        release_date.text = self.info_dict.get('release_date')
        banked_vol = ET.SubElement(tech_hub_elems, "volumeBankedNucleicAcid")
        banked_vol.text = ET.CDATA(self.info_dict.get('vol_banked'))
        conc_banked = ET.SubElement(tech_hub_elems, "concentrationBankedNucleicAcid")
        conc_banked.text = ET.CDATA(self.info_dict.get('conc_banked'))
        banked_loc = ET.SubElement(tech_hub_elems, "concentrationBankedNucleicAcid")
        banked_loc.text = ET.CDATA(self.info_dict.get('banked_loc'))
        banked_id = ET.SubElement(tech_hub_elems, "bankedNucleicAcididentifier")
        banked_id.text = ET.CDATA(self.info_dict.get('banked_id'))
        tech_hub = ET.SubElement(root, "smTechnologyHub", name=self.info_dict.get('tech_hub'))
        test_res = ET.SubElement(tech_hub, "testResults")
        # the below for all genes
        genes = self.info_dict.get("genes")
        for g, g_data in genes.items():
            test = ET.SubElement(test_res, "test")
            gene = ET.SubElement(test, "gene")
            gene.text = g_data.get('gene')
            test_method = ET.SubElement(test, "methodOfTest")
            test_method.text = ET.CDATA(g_data.get('test_method'))
            test_scope = ET.SubElement(test, "scopeOfTest")
            test_scope.text = ET.CDATA(g_data.get('test_scope'))
            release_test_date = ET.SubElement(test, "dateTestResultsReleased")
            release_test_date.text = g_data.get('test_results_date')
            test_result = ET.SubElement(test, "testResult")
            test_result.text = ET.CDATA(g_data.get('test_results'))
            test_report = ET.SubElement(test, "testReport")
            test_report.text = ET.CDATA(g_data.get('test_report'))
            test_status = ET.SubElement(test, "testStatus")
            test_status.text = g_data.get('test_status')
            comments = ET.SubElement(test, "comments")
            comments.text = ET.CDATA(g_data.get('comments'))
        edited_tree = ET.ElementTree(root)
        return edited_tree


    def write_xml(self, output_file_name, element_tree):
        output_xml = os.path.join(self.output_path, output_file_name)
        element_tree.write(output_xml, pretty_print=True)

    def validate_xml(self):
        return None

