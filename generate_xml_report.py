import os
from lxml import etree as ET

output_path = "/Users/sararey/Documents/cruk_reporting/xml_report" #temp path for testing"
output_file_name = "test.xml" #should be in the format date_hospitalorgcode_patientid_sampleid

def load_existing_xml(xml_file):
    tree = ET.parse(xml_file)
    root= tree.getroot()
    print(root.tag) # XML rooted in this tag
    print(root.attrib) # obtain attributes of root
    for child in root:
        print(child.tag, child.attrib)
        for c in child:
            print(c.tag)
    #[print(elem.tag, elem.attrib) for elem in root.iter()]
    for sample in root.iter('smpSample'):
        print(sample.text)
    print(ET.tostring(root, encoding="UTF-8"))


def generate_xml(info_dict):
    # for testing
    clinical_hub_name = "2 - Cardiff"
    tech_hub_name = "2 - Cardiff"

    # Code
    NS_XSI = "{http://www.w3.org/2001/XMLSchema-instance}"
    root = ET.Element("smpSample")
    root.set(NS_XSI + "noNamespaceSchemaLocation",
             'http://extranet.cancerresearchuk.org/stratmed/Shared%20Documents/smSampleXSDSchema%20V2.3.xsd')

    clinical_hub = ET.SubElement(root, "smClinicalHub", name=clinical_hub_name)
    patient = ET.SubElement(clinical_hub, "patient")
    ET.SubElement(patient, "organisationCode")
    ET.SubElement(patient, "localPatientIdentifier")
    ET.SubElement(patient, "localPatientIdentifier2")

    sample = ET.SubElement(root, "sample")
    clin_hub_elems = ET.SubElement(sample, "clinicalHubElements")
    ET.SubElement(clin_hub_elems, "sourceSampleIdentifier")
    ET.SubElement(clin_hub_elems, "typeOfSample")
    morph_snomed =  ET.SubElement(clin_hub_elems, "morphologySnomed")
    morph_snomed.text = ET.CDATA("NA")
    ET.SubElement(clin_hub_elems, "tumourType")
    ET.SubElement(clin_hub_elems, "dateSampleSent")
    tech_hub_elems = ET.SubElement(sample, "technologyHubElements")
    ET.SubElement(tech_hub_elems, "dateSampleReceived")
    ET.SubElement(tech_hub_elems, "labSampleIdentifier")
    ET.SubElement(tech_hub_elems, "reportReleaseDate")
    banked_vol = ET.SubElement(tech_hub_elems, "volumeBankedNucleicAcid")
    banked_vol.text = ET.CDATA("0")
    conc_banked = ET.SubElement(tech_hub_elems, "concentrationBankedNucleicAcid")
    conc_banked.text = ET.CDATA("0")
    banked_loc = ET.SubElement(tech_hub_elems, "concentrationBankedNucleicAcid")
    banked_loc.text = ET.CDATA("location")
    banked_id = ET.SubElement(tech_hub_elems, "bankedNucleicAcididentifier")
    banked_id.text = ET.CDATA("LabNo")

    tech_hub = ET.SubElement(root, "smTechnologyHub", name=tech_hub_name)
    test_res = ET.SubElement(tech_hub, "testResults")
    # the below for all genes
    test = ET.SubElement(test_res, "test")
    ET.SubElement(test, "gene")
    test_method = ET.SubElement(test, "methodOfTest")
    test_method.text = ET.CDATA("Num")
    test_scope = ET.SubElement(test, "scopeOfTest")
    test_scope.text = ET.CDATA("Exon")
    ET.SubElement(test, "dateTestResultsReleased")
    test_result = ET.SubElement(test, "testResult")
    test_result.text = ET.CDATA("No variant detected")
    test_report = ET.SubElement(test, "testReport")
    test_report.text = ET.CDATA("High confidence")
    ET.SubElement(test, "testStatus")
    comments = ET.SubElement(test, "comments")
    comments.text = ET.CDATA("These results are intended for research purposes only.")

    edited_tree = ET.ElementTree(root)
    return edited_tree


def write_xml(element_tree, output_xml):
    element_tree.write(output_xml)


def main():
    parsed_data = None #TODO create dictionary of required data parsed from data sources
    load_existing_xml(os.path.join("/Users/sararey/Documents/cruk_reporting/", "20190730 RVFAR-W014779Y-H19G5842 A1.xml"))
    tree = generate_xml(parsed_data)
    write_xml(tree, os.path.join(output_path, output_file_name))
    load_existing_xml(os.path.join(output_path, output_file_name))


if __name__ == '__main__':
    main()