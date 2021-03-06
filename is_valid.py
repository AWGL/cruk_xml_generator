from lxml import etree as ET
from os import path as op


class IsValid(object):

    def __init__(self, check_xml, xsd):
        self.xsd = xsd
        self.check_xml = check_xml

    def validate_xml_format(self):
        try:
            ET.parse(self.check_xml)
        except ET.XMLSyntaxError as e:
            raise Exception(f"The xml is incorrectly formatted, error: {e}")
        except OSError as e:
            raise Exception(f"The file {self.check_xml} could not be loaded, error {e}")
        file_name = op.basename(self.check_xml)
        return f"XML file {file_name} in valid XML format"

    def validate_xml_schema(self):
        try:
            xml_validation = ET.parse(self.xsd)
        except OSError as err:
            raise Exception(f"XSD XML schema file could not be loaded, error {err}")
        xml_validation_schema = ET.XMLSchema(xml_validation)
        try:
            loaded_check_xml = ET.parse(self.check_xml)
        except OSError as err:
            raise Exception(f"The file {self.check_xml} could not be loaded, error {err}")
        xml_validation_schema.assertValid(loaded_check_xml)
        file_name = op.basename(self.check_xml)
        xsd_name = op.basename(self.xsd)
        return f"XML file {file_name} validated against schema"






















