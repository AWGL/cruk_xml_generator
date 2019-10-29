import os

xml_version = "3.8"
results_path =  # Location of analysed results
db_path =  # Point to final location of Excel database
db_name = # Set to final name for Excel database
xsd =  # Set to where on shared drives this will be
xml_location = # Set to base location on shared drives for sending xml
pdf_location =  # Set to base location on shared drives for storing pdf

# Global variables
test_method = "19"
# List of fields that do not require data for the xml and can contain no data
can_be_null = ["local_patient_id_2", "comments"]
allowed_authorisers = [""]
sample_status = {"w": "withdrawn", "f": "failed", "s": "sequenced"}