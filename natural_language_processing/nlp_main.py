from nlp import NLP
from nlp_parsers import NLP_Parsers
import pprint as pp

def main():
    nlp = NLP()
    parser = NLP_Parsers()

    nlp.load_text('texts/turkjbio-44-110.pdf', 'Paper1', parser.pdf_parser)
    nlp.load_text('texts/1-s2.0-S0952791514001563-main.pdf', 'Paper2', parser.pdf_parser)
    nlp.load_text('texts/nihms659174.pdf', 'Paper3', parser.pdf_parser)
    nlp.load_text('texts/dark_side_of_CRISPR.txt', 'Article1', parser.txt_parser)
    nlp.load_text('texts/promises_of_CRISPR.txt', 'Article2', parser.txt_parser)
    nlp.load_text('texts/guide_to_crispr.txt', 'Article3', parser.txt_parser)

    nlp.compare_num_words()

if __name__ == '__main__':
    main()