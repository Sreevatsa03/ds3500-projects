from nlp import NLP
from nlp_parsers import NLP_Parsers
import pprint as pp

def main():
    nlp = NLP()
    parser = NLP_Parsers()

    nlp.load_text('file1.txt', 'A')
    nlp.load_text('file2.txt', 'B')
    nlp.load_text('file3.txt', 'C')

    nlp.load_text('myfile.json', 'J', parser=parser.json_parser)

    pp.pprint(nlp.data)
    nlp.compare_num_words()

    print(NLP.version)

if __name__ == '__main__':
    main()