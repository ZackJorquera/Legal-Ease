from scripts.sentence import *
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
import unidecode
import os

REMOVE_REGEX = '[^a-zA-Z0-9\'\"]'

class PDFParser(object):
    __pdf_file_loc = None
    __pdf_file = None

    def __init__(self, file):
        assert os.path.isfile(file), f"File does not exist: {file}"
        assert file.endswith(".pdf"), f"File is not pdf: {file}"

        self.__pdf_manager = PDFResourceManager()
        self.__pdf_file = open(file, 'rb')

    def __del__(self):
        if self.__pdf_file is not None:
            self.__pdf_file.close()

    def _parse_with_ocr(self):
        pass

    def convert_to_pure_text(self):
        ret_str = StringIO()
        device = TextConverter(self.__pdf_manager, ret_str, laparams=LAParams())

        interpreter = PDFPageInterpreter(self.__pdf_manager, device)

        for page in PDFPage.get_pages(self.__pdf_file, set(), maxpages=0, password="", caching=True,
                                      check_extractable=True):
            interpreter.process_page(page)

        text = ret_str.getvalue()

        text = unidecode.unidecode(text)
        text = re.sub(r'(\r\n|\n){2,}', '.\n', text)
        text = re.sub(r'[^\S\r\n]+', ' ', text)  # remove multiple space next to each other (but dont remove newlines)

        return text

    def convert_to_sentences(self, ret_type=str):
        return parse_sentences(self.convert_to_pure_text(), Sentence)


def pdf_parser(pdf_file):
    pdf_parser = PDFParser(pdf_file)
    sents = pdf_parser.convert_to_sentences()
    return sents

