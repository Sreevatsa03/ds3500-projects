from nlp import NLP
from nlp_parsers import NLP_Parsers
import pprint as pp

def main():
    nlp = NLP()
    parser = NLP_Parsers()

    nlp.load_text('sample_texts/turkjbio-44-110.pdf', 'sample', parser.pdf_parser)
    # pp.pprint(nlp.data)
    nlp.compare_num_words()
    

if __name__ == '__main__':
    main()