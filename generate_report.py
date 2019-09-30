from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.platypus import Paragraph, Table, TableStyle
from itertools import islice


class GenerateReport:

    def __init__(self, file_name, sample_dict, report_status=None):
        self.col_widths_dict = {"success": [1.2*cm, 1.2*cm, 1.2*cm, 2.3*cm, 2.8*cm, 1.9*cm, cm, 5*cm],
                           "failed": [1.2*cm, 1.2*cm, 1.2*cm, 2.3*cm, 1.5*cm, 3.5*cm, cm, 4.6*cm],
                           "withdrawn": [1.2*cm, 1.2*cm, 1.2*cm, 2.3*cm, 1.5*cm, 3.5*cm, cm, 4.6*cm]}
        self.file_name = file_name
        self.sample_dict = sample_dict
        #column widths- if not foudn default columns widths for success
        self.col_widths = self.col_widths_dict.get(report_status, self.col_widths_dict.get("success"))


    def pdf_writer(self):
        template = canvas.Canvas(self.file_name, pagesize=A4, bottomup=1)
        width, height = A4
        #template.translate(2*cm, 3*cm) # Move origin
        template.setFont("Helvetica", 20)
        template.drawString(2*cm, height-(2.5*cm), "Title")
        template.setFont("Helvetica", 12)
        template.drawString(2*cm, height-(3.3*cm), f"Date sample sent: {self.sample_dict.get('date_sample_sent')}")
        template.drawString(11*cm, height-(3.3*cm),
                            f"Date sample received: {self.sample_dict.get('date_sample_received')}")

        #Create table of data for table format
        print(self.sample_dict.get('genes'))
        #TODO Abstract this out later?
        # Create styles
        style_header = getSampleStyleSheet()["BodyText"]
        style_header.fontName = 'Helvetica'
        style_header.fontSize = 6
        style_header.textColor = colors.white
        style_body = getSampleStyleSheet()["BodyText"]
        style_body.fontName = 'Helvetica'
        style_body.fontSize = 5
        style_body.textColor = colors.black
        headers = [Paragraph('Gene number', style_header), Paragraph('Gene name', style_header),
                       Paragraph('Test method', style_header), Paragraph('Scope of test', style_header),
                       Paragraph('Test result', style_header), Paragraph('Test report', style_header),
                       Paragraph('Test status', style_header), Paragraph('Comments', style_header)]
        first_table = list(islice(self.sample_dict.get('genes').items(), 21))
        second_table = list(islice(self.sample_dict.get('genes').items(),
                                   21, len(self.sample_dict.get('genes').items())))
        table_data = [headers]
        for k, v in first_table:
            line_table = []
            line_table.append(Paragraph(v.get('gene'), style_body))
            line_table.append(Paragraph(k, style_body))
            line_table.append(Paragraph(v.get('test_method'), style_body))
            line_table.append(Paragraph(": ".join(v.get('test_scope').split(":")), style_body))
            line_table.append(Paragraph(v.get('test_results'), style_body))
            line_table.append(Paragraph(v.get('test_report'), style_body))
            line_table.append(Paragraph(v.get('test_status'), style_body))
            line_table.append(Paragraph(v.get('comments'), style_body))
            #line_table.append(Paragraph("aaaaaaaaaa"*60, style_body))
            table_data.append(line_table)
        #table_data.append(PageBreak())

        #TODO flowables.append(PageBreak()) [from reportlab.platypus import PageBreak]
        table = Table(table_data, colWidths=self.col_widths)
        table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                                   ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                                   ('FONTNAME', (0, 0), (-1, -1), "Helvetica"),
                                   ('FONTSIZE', (0, 0), (-1, -1), 5),
                                   ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                                   ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                                   ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.lightgrey, colors.white])]))

        #table._argW[4]=5*cm
        table.wrapOn(template, width, height)
        table.drawOn(template, 2*cm, 2.9*cm)

        
        template.showPage()

        # Multiple pages
        table_data = [headers]
        for k, v in second_table:
            line_table = []
            line_table.append(Paragraph(v.get('gene'), style_body))
            line_table.append(Paragraph(k, style_body))
            line_table.append(Paragraph(v.get('test_method'), style_body))
            line_table.append(Paragraph(": ".join(v.get('test_scope').split(":")), style_body))
            line_table.append(Paragraph(v.get('test_results'), style_body))
            line_table.append(Paragraph(v.get('test_report'), style_body))
            line_table.append(Paragraph(v.get('test_status'), style_body))
            line_table.append(Paragraph(v.get('comments'), style_body))
            #line_table.append(Paragraph("aaaaaaaaaa"*60, style_body))
            table_data.append(line_table)

        table = Table(table_data, colWidths=self.col_widths)
        table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                                   ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                                   ('FONTNAME', (0, 0), (-1, -1), "Helvetica"),
                                   ('FONTSIZE', (0, 0), (-1, -1), 5),
                                   ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                                   ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                                   ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.lightgrey, colors.white])]))

        table.wrapOn(template, width, height)
        table.drawOn(template, 2*cm, 2*cm)
        template.showPage()
        template.save()