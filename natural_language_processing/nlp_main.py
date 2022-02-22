from nlp import NLP, NLP_Parsers
import pprint as pp

def main():
    nlp = NLP()
    parser = NLP_Parsers()

    parser.load_stop_words('stop.txt')

    nlp.load_text('texts/turkjbio-44-110.pdf', 'Paper1', parser.pdf_parser)
    nlp.load_text('texts/1-s2.0-S0952791514001563-main.pdf', 'Paper2', parser.pdf_parser)
    nlp.load_text('texts/nihms659174.pdf', 'Paper3', parser.pdf_parser)
    nlp.load_text('texts/dark_side_of_CRISPR.txt', 'Article1', parser.txt_parser)
    nlp.load_text('texts/promises_of_CRISPR.txt', 'Article2', parser.txt_parser)
    nlp.load_text('texts/guide_to_crispr.txt', 'Article3', parser.txt_parser)

    # nlp.compare_num_words()
    # nlp.word_count_sankey(None, 7, False)
    # nlp.word_count_sankey(None, 7, True)
    # nlp.sentiment_analysis()
    # nlp.sentence_length_and_unique_words_comparison()
    nlp.plot_heaps_law()

if __name__ == '__main__':
    main()