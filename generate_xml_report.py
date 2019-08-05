import os
import xml.etree.ElementTree as ET

output_path = "/Users/sararey/Documents/cruk_reporting/xml_report" #temp path for testing"
output_file_name = "test" #should be in the format date_hospitalorgcode_patientid_sampleid

def load_existing_xml(xml_file):
    tree = ET.parse(xml_file)
    root= tree.getroot()
    print(root.tag) # XML rooted in this tag
    print(root.attrib) # obtain attributes of root
    for child in root:
        print(child.tag, child.attrib)
    return None


def generate_xml():

    return None


def main():
    generate_xml()
    load_existing_xml(os.path.join("/Users/sararey/Documents/cruk_reporting/", "20190730 RVFAR-W014779Y-H19G5842 A1.xml"))


if __name__ == '__main__':
    main()