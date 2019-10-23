from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.lib import colors
from reportlab.platypus import Paragraph, Preformatted, Spacer, Table, TableStyle
from reportlab.platypus import SimpleDocTemplate
from os import path as op


class GenerateReport:

    def __init__(self, file_name, sample_dict, ml, status=None):
        self.sample_dict = sample_dict
        self.pagesize = A4
        self.file_name = file_name
        self.status = status
        self.col_widths_dict = {"s": [1.2 * cm, 1.6 * cm, 2.1 * cm, 6.5 * cm, 5.5 * cm, 1.2 * cm, 6 * cm],
                                "f": [1.2 * cm, 1.6 * cm, 3 * cm, 2.5 * cm, 7.2 * cm, 1.2 * cm, 7.5 * cm],
                                "w": [1.2 * cm, 1.6 * cm, 3 * cm, 2.5 * cm, 7.2 * cm, 1.2 * cm, 7.5 * cm]}
        self.ml = ml
        self.log = ml.module_logger
        self.popup = ml.my_message

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

        # Checker data added to report
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
            self.log.error("Error at PDF generation stage. See bioinformatics team for help.")
            self.popup.mainloop()
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
        file_name = op.basename(self.file_name)
        return f"PDF report {file_name} generated"


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
