from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.lib import colors
from reportlab.platypus import Paragraph, Preformatted, Spacer, Table, TableStyle

from reportlab.platypus import SimpleDocTemplate


class GenerateReport:

    def __init__(self, file_name, sample_dict, status=None):
        self.sample_dict = sample_dict
        self.pagesize = A4
        self.file_name = file_name
        self.status = status
        self.col_widths_dict = {"s": [1.2 * cm, 1.6 * cm, 2.1 * cm, 6.5 * cm, 5.5 * cm, 1.2 * cm, 6 * cm],
                                "f": [1.2 * cm, 1.6 * cm, 3 * cm, 2.5 * cm, 7.2 * cm, 1.2 * cm, 7.5 * cm],
                                "w": [1.2 * cm, 1.6 * cm, 3 * cm, 2.5 * cm, 7.2 * cm, 1.2 * cm, 7.5 * cm]}

    def _headers(self, my_canvas, my_doc):
        my_canvas.saveState()

        styles = getSampleStyleSheet()
        header_style = styles['Normal']

        header1 = Paragraph(f"Clinical Hub: {self.sample_dict.get('clinical_hub')} ", header_style)
        header2 = Paragraph(f"{self.sample_dict.get('cruk_sample_id')} ", header_style)
        header3 = Paragraph(f"Lab ID: {self.sample_dict.get('lab_id')} ", header_style)
        w1, h1 = header1.wrap(my_doc.width, my_doc.topMargin)
        w2, h2 = header2.wrap(my_doc.width, my_doc.topMargin)
        w3, h3 = header3.wrap(my_doc.width, my_doc.topMargin)
        header1.drawOn(my_canvas, my_doc.leftMargin, my_doc.height + my_doc.topMargin - h1 + 1.2 * cm)
        header2.drawOn(my_canvas, my_doc.leftMargin + 9.7 * cm, my_doc.height + my_doc.topMargin - h2 + 1.2 * cm)
        header3.drawOn(my_canvas, my_doc.leftMargin + 21.5 * cm, my_doc.height + my_doc.topMargin - h3 + 1.2 * cm)

        my_canvas.restoreState()

    @staticmethod
    def _footer(my_canvas, my_doc):
        '''
        Add in here if want to add footer instead of header
        :param my_canvas:
        :param my_doc:
        :return:
        '''
        return None

    @staticmethod
    def first_page(my_canvas, my_doc):
        '''
        Template for putting in bespoke front page
        :param my_canvas:
        :param my_doc:
        :return:
        '''
        my_canvas.saveState()
        my_canvas.setFont('Times-Bold', 16)
        my_canvas.drawCentredString(my_doc.width / 2.0, my_doc.height - 108, "Title here")
        my_canvas.setFont('Times-Roman', 9)
        my_canvas.drawString(cm, 2 * cm, "First Page / %s" % "stuff")
        my_canvas.restoreState()

    def generate_pdf(self):

        doc = SimpleDocTemplate(self.file_name, rightMargin=72, leftMargin=72, topMargin=60, bottomMargin=60,
                                pagesize=landscape(self.pagesize))

        styles = getSampleStyleSheet()
        style_tabl_title = ParagraphStyle('tabletitle', parent=styles["BodyText"], fontSize=8, textColor=colors.white)
        style_tabl = ParagraphStyle('tablebody', parent=styles["BodyText"], fontSize=7, textColor=colors.black)
        title_style = ParagraphStyle('title', parent=styles['Normal'], fontSize=16, leading=8, alignment=TA_LEFT)

        # Elements
        elements = []
        elements.append(Paragraph("Illumina NGS TST170 Panel 43 of 170", title_style))
        elements.append(Spacer(1, 20))
        elements.append(Preformatted(f"Date sample sent: {self.sample_dict.get('date_sample_sent')}               "
                                     f"          Date sample received: {self.sample_dict.get('date_sample_received')}",
                                     styles['Normal']))
        elements.append(Spacer(1, 10))

        # Headers
        tabl_headers = [Paragraph('Gene num', style_tabl_title), Paragraph('Gene name', style_tabl_title),
                        Paragraph('Scope of test', style_tabl_title),
                        Paragraph('Test result', style_tabl_title), Paragraph('Test report', style_tabl_title),
                        Paragraph('Test status', style_tabl_title), Paragraph('Comments', style_tabl_title)]

        # Gene level data
        table_data = []
        for k, v in self.sample_dict.get('genes').items():
            line_table = []
            line_table.append(Paragraph(v.get('gene'), style_tabl))
            line_table.append(Paragraph(k, style_tabl))
            line_table.append(Paragraph(v.get('test_scope').split(":")[1], style_tabl))
            line_table.append(Paragraph(v.get('test_results'), style_tabl))
            line_table.append(Paragraph(v.get('test_report'), style_tabl))
            test_status = v.get('test_status')
            line_table.append(Paragraph(test_status, style_tabl))
            line_table.append(Paragraph(v.get('comments'), style_tabl))
            table_data.append(line_table)

        table_data.insert(0, tabl_headers)

        table = Table(table_data, self.col_widths_dict.get(self.status))
        table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                                   ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                                   ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                                   ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.lightgrey, colors.white])]))
        elements.append(table)
        elements.append(Spacer(1, 10))

        # Checker data
        # For sequenced samples
        num_fails = 0
        if self.status == "s":
            sig_table_data = [["", "", "Date"], ["Checker 1", self.sample_dict.get('reported_by_1'),
                                             self.sample_dict.get('date_reported_1')],
                          ["Checker 2", self.sample_dict.get('reported_by_2'),
                           self.sample_dict.get('date_reported_2')],
                          ["Authorised", self.sample_dict.get('authorised_by'),
                           self.sample_dict.get('date_authorised')]]
            # Count number of failed genes
            num_fails += len([count[-2].text for count in table_data if count[-2].text == "3"])
            elements.append(Paragraph(f"Number of failed genes: {num_fails}", styles['Normal']))
            elements.append(Spacer(1, 10))

        # For failed or withdrawn samples
        elif self.status == "f" or self.status == "w":
            sig_table_data = [["", "", "Date"],
                          ["Authorised", self.sample_dict.get('authorised_by'),
                           self.sample_dict.get('date_authorised')]]

        else:
            raise Exception("Could not determine if report is for QC fail, withdrawn or sequenced sample")

        sig_table = Table(sig_table_data, colWidths=[2.5 * cm, 1.5 * cm, 2.5 * cm], hAlign='LEFT')
        sig_table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                                       ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                                       ('FONTSIZE', (0, 0), (-1, -1), 8),
                                       ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                                       ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                                       ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white])]))

        elements.append(sig_table)

        doc.build(elements, onFirstPage=self._headers, onLaterPages=self._headers, canvasmaker=BespokeCanvasTemplate)
        return f"PDF report {self.file_name} generated"


class BespokeCanvasTemplate(canvas.Canvas):
    '''
    Create bespoke build of canvas to allow for objects to appear on every page
    Allows insertion of a footer that will also count the total number of pages in the document
    '''

    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        """add page info to each page (page x of y)"""
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        # Change the position of this to wherever you want the page number to be
        text_object = self.beginText()
        text_object.setTextOrigin(25.5 * cm, 1.9 * cm)
        text_object.setFont('Helvetica', 10)
        text_object.textLine(text=f"Page {self._pageNumber} of {page_count}")
        self.drawText(text_object)


'''
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
        # Saves and closes
        template.save()
        return f"PDF report {self.file_name} generated"

'''
