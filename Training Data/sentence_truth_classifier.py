from sentence import *


classifications = ["ambiguous", "predatory", "important", "unimportant"]
class_string = "0: skip; " + "; ".join([f'{i+1}, {j}' for i, j in enumerate(classifications)])

from pdf_parser import PDFParser

# pdf_file = r"C:\Users\jorqu\Documents\Kenneth Himma _Ethicsal Issues Involving Computer Security..._.pdf"
pdf_file = r"C:\Users\jorqu\Downloads\LeaseRenewalAgreement_12222020.pdf"
pdf_parser = PDFParser(pdf_file)
sentences = pdf_parser.convert_to_sentences()

# sentences = parse_sentences(str(open("amazon_tos.txt", 'rb').read()), Sentence)

for s in sentences:
    sentence_file = open("sentences.txt", 'a')
    classifications_file = open("classifications.txt", 'a')

    print(s.text, '\n')
    classifications = input(f"Select classification: {class_string} (or q to quit): ")
    print('\n\n\n')

    if classifications == 'q':
        sentence_file.close()
        classifications_file.close()
        break
    if classifications == '0':
        sentence_file.close()
        classifications_file.close()
        continue
    sentence_file.write(s.text + "\n")
    classifications_file.write(classifications + "\n")

    sentence_file.close()
    classifications_file.close()



    
    