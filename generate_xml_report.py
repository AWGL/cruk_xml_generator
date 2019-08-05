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
    sample = ET.SubElement(root, "smClinicalHub")
    clin_hub_elems = ET.SubElement(sample, "clinicalHubElements")
    ET.SubElement(clin_hub_elems, "sourceSampleIdentifier")
    ET.SubElement(clin_hub_elems, "typeOfSample")
    morph_snomed =  ET.SubElement(clin_hub_elems, "morphologySnomed")
    morph_snomed.text = ET.CDATA("stuff")

    ET.SubElement(clin_hub_elems, "tumourType")
    ET.SubElement(clin_hub_elems, "dateSampleSent")
    tech_hub_elems = ET.SubElement(sample, "technologyHubElements")


    tech_hub = ET.SubElement(root, "smClinicalHub", name=tech_hub_name)


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