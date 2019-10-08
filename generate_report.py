from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.platypus import Paragraph, Table, TableStyle
from itertools import islice


class GenerateReport:

    def __init__(self, file_name, sample_dict, report_status=None):
        self.col_widths_dict = {"s": [cm, 1.25 * cm, 1.2 * cm, 2.3 * cm, 3.25 * cm, 1.9 * cm, cm, 5.1 * cm],
                                "f": [1.2 * cm, 1.25 * cm, 1.2 * cm, 2.3 * cm, 1.5 * cm, 3.5 * cm, cm, 5.05 * cm],
                                "w": [1.2 * cm, 1.25 * cm, 1.2 * cm, 2.3 * cm, 1.5 * cm, 3.5 * cm, cm,
                                              5.05 * cm]}
        self.file_name = file_name
        self.sample_dict = sample_dict
        self.report_status = report_status
        # Set column widths
        self.col_widths = self.col_widths_dict.get(self.report_status)

    @staticmethod
    def get_gene_table_data(table_dict, style):
        table_data = []
        for k, v in table_dict:
            line_table = []
            line_table.append(Paragraph(v.get('gene'), style))
            line_table.append(Paragraph(k, style))
            line_table.append(Paragraph(v.get('test_method'), style))
            line_table.append(Paragraph(": ".join(v.get('test_scope').split(":")), style))
            line_table.append(Paragraph(v.get('test_results'), style))
            line_table.append(Paragraph(v.get('test_report'), style))
            test_status = v.get('test_status')
            line_table.append(Paragraph(test_status, style))
            line_table.append(Paragraph(v.get('comments'), style))
            table_data.append(line_table)
        return table_data

    def create_gene_table(self, table_data):
        table = Table(table_data, colWidths=self.col_widths)
        table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                                   ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                                   ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                                   ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                                   ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.lightgrey, colors.white])]))
        return table

    @staticmethod
    def create_sig_box_table(table_data):
        table = Table(table_data, colWidths=[2.5 * cm, 2 * cm, 2.5 * cm])
        table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                                   ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                                   ('FONTSIZE', (0, 0), (-1, -1), 8),
                                   ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                                   ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                                   ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white])]))
        return table

    def pdf_writer(self):
        template = canvas.Canvas(self.file_name, pagesize=A4, bottomup=1)
        width, height = A4
        # Draw headers on template
        template.setFont("Helvetica", 8)
        template.drawString(2 * cm, height-(1.5 * cm), f"Clinical Hub: {self.sample_dict.get('clinical_hub')}")
        template.drawString(8.6 * cm, height - (1.5 * cm), f"{self.sample_dict.get('cruk_sample_id')}")
        template.drawString(16.5 * cm, height - (1.5 * cm), f"Lab ID: {self.sample_dict.get('lab_id')}")
        # Draw title on template
        template.setFont("Helvetica", 20)
        template.drawString(2 * cm, height-(2.7 * cm), "Illumina NGS TST170 Panel 43 of 170")
        # Draw dates on template
        template.setFont("Helvetica", 10)
        template.drawString(2 * cm, height-(3.5 * cm), f"Date sample sent: {self.sample_dict.get('date_sample_sent')}")
        template.drawString(8.5 * cm, height-(3.5 * cm),
                            f"Date sample received: {self.sample_dict.get('date_sample_received')}")

        # Create table of data for table format
        style_header = getSampleStyleSheet()["BodyText"]
        style_header.fontName = 'Helvetica'
        style_header.fontSize = 6
        style_header.textColor = colors.white
        style_body = getSampleStyleSheet()["BodyText"]
        style_body.fontName = 'Helvetica'
        style_body.fontSize = 5
        style_body.textColor = colors.black
        # Generate headers for gene and gene data tables
        headers = [Paragraph('Gene num', style_header), Paragraph('Gene name', style_header),
                       Paragraph('Test method', style_header), Paragraph('Scope of test', style_header),
                       Paragraph('Test result', style_header), Paragraph('Test report', style_header),
                       Paragraph('Test status', style_header), Paragraph('Comments', style_header)]

        # Create data for first table of genes and associated data (22 genes fit on first page)
        first_table = list(islice(self.sample_dict.get('genes').items(), 22))
        table_data = self.get_gene_table_data(first_table, style_body)
        # Count number of failed genes- all failed samples are stored as a 3 in the second from last column
        num_fails = len([count[-2].text for count in table_data if count[-2].text == "3"])
        # Add headers to table (beginning)
        table_data.insert(0, headers)
        # Draw table
        table = self.create_gene_table(table_data)
        # Draw table on to template
        table.wrapOn(template, width, height)
        table.drawOn(template, 2 * cm, 1.5 * cm)
        template.setFont("Helvetica", 8)
        template.drawString(width-(3.5 * cm), cm, "Page 1 of 2")
        template.showPage()

        # Split table over multiple pages
        # Create data for second table of genes and associated data
        second_table = list(islice(self.sample_dict.get('genes').items(),
                                   22, len(self.sample_dict.get('genes').items())))
        table_data = self.get_gene_table_data(second_table, style_body)
        # Count number of failed genes- all failed samples are stored as a 3 in the second from last column
        num_fails += len([count[-2].text for count in table_data if count[-2].text == "3"])
        # Add headers to table (beginning)
        table_data.insert(0, headers)
        # Draw table
        table = self.create_gene_table(table_data)
        # Draw table on to template
        table.wrapOn(template, width, height)
        table.drawOn(template, 2 * cm, 4.2 * cm)

        # Create data for table of people checking this report
        # For sequenced samples
        if self.report_status == "s":
            table_data = [["", "", "Date"],
                        ["Checker 1", self.sample_dict.get('reported_by_1'), self.sample_dict.get('date_reported_1')],
                        ["Checker 2", self.sample_dict.get('reported_by_2'), self.sample_dict.get('date_reported_2')],
                        ["Authorised", self.sample_dict.get('authorised_by'), self.sample_dict.get('date_authorised')]]
            table = self.create_sig_box_table(table_data)
            # Draw table on to template
            table.wrapOn(template, width, height)
            table.drawOn(template, 2*cm, 1.4*cm)

            # Number of failed genes for this sample
            template.setFont("Helvetica", 10)
            template.drawString(11.4 * cm, 3.5 * cm, f"Gene fails: {num_fails}")

        # For failed or withdrawn samples
        elif self.report_status == "f" or self.report_status == "w":
            table_data = [["", "", "Date"],
                          ["Authorised", self.sample_dict.get('authorised_by'),
                           self.sample_dict.get('date_authorised')]]
            table = self.create_sig_box_table(table_data)
            # Draw table on to template
            table.wrapOn(template, width, height)
            table.drawOn(template, 2 * cm, 2.5 * cm)
        else:
            raise Exception("Could not determine if report is for QC fail, withdrawn or sequenced sample")

        # For all samples
        template.setFont("Helvetica", 8)
        template.drawString(width-(3.5 * cm), cm, "Page 2 of 2")
        template.showPage()
        template.save()
        return f"PDF report {self.file_name} generated"

