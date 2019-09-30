from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.platypus import Paragraph, Table, TableStyle

class GenerateReport:

    def __init__(self, file_name, sample_dict):
        self.file_name = file_name
        self.sample_dict = sample_dict

    def pdf_writer(self):
        template = canvas.Canvas(self.file_name, pagesize=A4, bottomup=1)
        width, height = A4
        #template.translate(2*cm, 3*cm) # Move origin
        template.setFont("Helvetica", 25)
        template.drawString(2*cm, height-(3*cm), "Title")
        template.setFont("Helvetica", 12)
        template.drawString(2*cm, height-(4*cm), f"Date sample sent: {self.sample_dict.get('date_sample_sent')}")
        template.drawString(11*cm, height-(4*cm),
                            f"Date sample received: {self.sample_dict.get('date_sample_received')}")

        #Create table of data for table format
        print(self.sample_dict.get('genes'))
        #TODO Abstract this out later?
        # Create styles
        style_header = getSampleStyleSheet()["BodyText"]
        style_header.fontName = 'Helvetica'
        style_header.fontSize = 6
        style_header.textColor = colors.white
        style_header.listAttrs()
        style_body = getSampleStyleSheet()["BodyText"]
        style_body.fontName = 'Helvetica'
        style_body.fontSize = 5
        style_normal = getSampleStyleSheet()["Normal"]
        table_data = [[Paragraph('Gene number', style_header), Paragraph('Gene name', style_header),
                       Paragraph('Method of test', style_header), Paragraph('Scope of test', style_header),
                       Paragraph('Test result', style_header), Paragraph('Test report', style_header),
                       Paragraph('Test status', style_header), Paragraph('Comments', style_header)]]
        for k, v in self.sample_dict.get('genes').items():
            line_table = []
            line_table.append(v.get('gene'))
            line_table.append(k)
            line_table.append(v.get('test_method'))
            line_table.append(v.get('test_scope'))
            line_table.append(v.get('test_results'))
            line_table.append(v.get('test_report'))
            line_table.append(v.get('test_status'))
            line_table.append(v.get('comments'))
            table_data.append(line_table)

        #TODO flowables.append(PageBreak()) [from reportlab.platypus import PageBreak]
        table = Table(table_data, colWidths=[1.2*cm, 2*cm, cm, 3*cm, 2*cm, 4*cm, cm, 4*cm])
        table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                                   ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                                   ('FONTNAME', (0, 0), (-1, -1), "Helvetica"),
                                   ('FONTSIZE', (0, 0), (-1, -1), 5),
                                   ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                                   ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                                   ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.lightgrey, colors.white])]))

        #table._argW[4]=5*cm
        table.wrapOn(template, (width-5*cm), (height-5*cm))
        table.drawOn(template, 2*cm, 0*cm)
        template.showPage()

        # Multiple pages
        template.showPage()
        template.save()