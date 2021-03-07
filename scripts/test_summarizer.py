from unittest import TestCase
from sentence import parse_sentences, parse_words
from summarizer import SummarizerSettings, Summarizer
from pdf_parser import PDFParser


class TestSummarizer(TestCase):
    def test_parse_sentence(self):
        text = "Mr. Smith bought cheapsite.com for 1.5 million dollars, i.e. he paid a lot for it! Did he mind? Adam Jones Jr. thinks he didn't. In any case, this isn't true... Well, with a probability of .9 it isn't."
        sentences = parse_sentences(text)
        assert len(sentences) == 4

    def test_number_of_words(self):
        text = "Mr. Smith bought cheapsite.com for 1.5 million dollars, i.e. he paid a lot for it! Did he mind? Adam Jones Jr. thinks he didn't. In any case, this isn't true... Well, with a probability of .9 it isn't."
        num_words = len(parse_words(text))
        assert num_words == 38

    def test_summarizer_settings(self):
        # ENUMS are annoying in python but here is how they work
        print(SummarizerSettings.PER_WORD)  # -> SummarizerSettings.PER_WORD
        print(SummarizerSettings.PER_WORD.value)  # -> 0
        print(SummarizerSettings.PER_WORD.name)  # -> PER_WORD

    def test_get_optimal_subset_by_percent_words(self):  # takes about 1.2 seconds
        with open('sample_text.txt', encoding="utf8") as text_file:

            # Load text
            sample_text = str(text_file.read())

            # Remove unwanted text in the essay. ie '(fr)'
            sample_text = sample_text.replace('(fr) ', '')

            # Load document class
            summarizer = Summarizer(text=sample_text)

            # Find summary with 25% words
            val, summary = summarizer.get_optimal_subset_by_percent_words(.10, ret_as="str")

            # Write out summary
            with open('output.txt', 'w+') as w_file:
                w_file.write(summary)

    def test_get_optimal_subset(self):  # takes about .9 seconds
        with open('sample_text.txt', encoding="utf8") as text_file:

            # Load text
            sample_text = str(text_file.read())

            # Remove unwanted text in the essay. ie '(fr)'
            sample_text = sample_text.replace('(fr) ', '')

            # Load document class
            summarizer = Summarizer(text=sample_text)

            # get summary
            val, summary = summarizer.get_optimal_subset(2500, ret_as="str")

            # Write out summary
            with open('output.txt', 'w+') as w_file:
                w_file.write(summary)

    def test_get_summary_from_pdf(self):
        pdf_file = r"C:\Users\jorqu\Downloads\LeaseRenewalAgreement_12222020.pdf"
        pdf_parser = PDFParser(pdf_file)
        text = pdf_parser.convert_to_pure_text()
        summarizer = Summarizer(text=text)
        val, summary = summarizer.get_optimal_subset_by_percent_words(.10, ret_as="str")

        # Write out summary
        with open('output.txt', 'w+') as w_file:
            w_file.write(summary)

