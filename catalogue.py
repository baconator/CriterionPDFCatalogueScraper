from movie import Movie

__author__ = 'Bacon'

# Pdf miner ...
from pdfminer.layout import LAParams
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.layout import LTTextBox, LTTextLine, LTPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
# ... why. Just. Why.

class Catalogue(object):
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path

    # Returns a generator that permits iteration over a pdf's pages and layouts.
    @property
    def pages(self):
        with open(self.pdf_path, "rb") as pdf:
            # Deal with PDFMiner's goooorgeous interface for parsing PDFs
            # Mostly from https://euske.github.io/pdfminer/programming.html
            catalogue = PDFDocument(PDFParser(pdf))
            layout_parameters = LAParams()
            resource_manager = PDFResourceManager()
            device = PDFPageAggregator(resource_manager, laparams=layout_parameters)
            interpreter = PDFPageInterpreter(resource_manager, device)
            for page in PDFPage.create_pages(catalogue):
                interpreter.process_page(page)
                layout = device.get_result()
                yield (layout, page)

    def __find_text_recursively(self, layout):
        if isinstance(layout, LTTextBox) or isinstance(layout, LTPage):
            for sub_layout in layout:
                for result in self.__find_text_recursively(sub_layout):
                    if result is not None:
                        yield result
        elif isinstance(layout, LTTextLine):
            yield layout
        else:
            yield None

    # Iterates over each line of every page
    @property
    def lines(self):
        for (layout, page) in self.pages:
            for line in self.__find_text_recursively(layout):
                yield line.get_text()

    @property
    def movies(self):
        for line in self.lines:
            try:
                yield Movie(line)
            except AttributeError:
                pass # the line didn't have a movie in it.