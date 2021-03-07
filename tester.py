from scripts.pdf_parser import PDFParser
from scripts.summarizer import Summarizer


if __name__ == '__main__':
    pdf_file = r"C:\Users\jorqu\Downloads\LeaseRenewalAgreement_12222020.pdf"
    pdf_parser = PDFParser(pdf_file)
    text = pdf_parser.convert_to_pure_text()
    summarizer = Summarizer(text=text)
    val, summary = summarizer.get_optimal_subset_by_percent_words(.10, ret_as="str")

    print(summary)