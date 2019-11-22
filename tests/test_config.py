import os

xml_version = "3.8"
results_path = os.getcwd() #temp path for testing- base to results on L drive
db_path = os.getcwd() #point to final location of Mo's database
db_name = "SMP2v3 workflow tracker.xlsx" #set to final name for Mo's database
xsd = os.path.join(os.getcwd(), "SMP2XSD (Results) v3.8.xsd") #Set to where on shared drives this will be
xml_location = os.path.join(os.getcwd(), "XML_reporting") #Set to base location on shared drives for sending xml
pdf_location = os.path.join(os.getcwd(), "pdfs") #Set to base location on shared drives for storing pdf