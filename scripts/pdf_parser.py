from sentence import *
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
import os


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
        return text

    def convert_to_sentences(self, ret_type=str):
        return parse_sentences(self.convert_to_pure_text(), Sentence)



if __name__ == '__main__':
    pdf_file = r"C:\Users\jorqu\Documents\Kenneth Himma _Ethicsal Issues Involving Computer Security..._.pdf"
    pdf_parser = PDFParser(pdf_file)
    sents = pdf_parser.convert_to_sentences()
    print(sents)



