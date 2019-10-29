# CRUK XML and PDF Generator
***
## Introduction
Tool to generate an XML report of the CRUK analysis output for sending to CRUK. 

Also makes a PDF document of the results with the details of the checkers and authoriser.
***
## Installation
This software uses Python 3.7.

It has dependencies which are recommended to be installed using a Conda environment. 
Install Conda:

```
https://docs.conda.io/projects/conda/en/latest/user-guide/install/download.html
```

Clone the repository:

```
git clone https://github.com/AWGL/cruk_xml_generator
```

Create Conda environment:

```
conda env create cruk_report_env.yml
```

Set up the config file to point to the correct locations on the local computer:


Edit ```config.py.example``` and save as ```config.py```


The code can then be run after the Conda environment is activated:

```
python report_cruk.py
```
***
## Packaging for deployment
The software needs to be packaged to run on imaged PCs without Python installed. The package needs to be built on a Windows 7 PC with Python 3.7 installed.

Install pyinstaller if it is not already installed:

```
conda install pyinstaller
```

Package the software:

```
pyinstaller report_cruk.py
```
***
## Deployment
Copy the dist directory generated by pyinstaller to the PC or shared drive from which the sofware is to be run. 

It may be useful to create a shortcut to the executable file ```report_cruk.exe``` for the user.
***
## Instructions for usage
### Running the software
Double click on the ```report_cruk.exe``` file.
### Using the software
1. Wait for a pop-up box called "CRUK Generator Data Entry" to appear, enter the required data in every field in the first pop-up box and click OK

2. Wait for a second pop-up box with logging information to appear. This box is called ""CRUK Generator Log".
	* If the text indicates successes, with the final entry "XML file copied to directory for sending to CRUK", click OK.
	* If there is an error message displayed, **the software has not executed correctly**, click OK **and perform troubleshooting.**
3. Close the software down completely by clicking on the "Close Program" button in the small pop-up window remaining.

***
## Troubleshooting
A log file ```cruk_report.log``` is generated at each execution of the software to aid troubleshooting

***
## Notes
### Current known issues
* valid_data.py is missing as it is currently not finalised

### Dependency List
In case the Conda environment build fails.

* python 3.7
* tkinter
* xlrd
* openpyxl
* pandas
* reportlab
* lxml






