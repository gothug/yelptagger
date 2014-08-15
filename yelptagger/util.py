import nltk
import pandas as pd
import csv
import pprint

def p(thing):
    pprint.pprint(thing)

def split_list(mylist, *args):
    ilist = map(lambda p : int(p * len(mylist) / 100.0), args) + [len(mylist)]
    return reduce(lambda l, v : [l[0] + [mylist[l[1]:v]], v], ilist, [[],0])[0]

def sentence_tokenize(sentence):
    sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
    return sent_detector.tokenize(sentence)

def write_to_csv(filename, data):
    f = open(filename, 'w')
    w = csv.writer(f, quotechar = '|', quoting=csv.QUOTE_ALL)
    w.writerows(data)
    f.close()

def parse_sentence(sentence, rating):
    words = [e.lower() for e in nltk.word_tokenize(sentence)\
        if (len(e) > 1 or e == '!')]

    for symbol in ('-', '.', ',', ':', '"', '\'', '$', '(', ')', '=', '+',
        '*', '?'):
        words = map(lambda x: x.replace(symbol, ' '), words)

    porter = nltk.PorterStemmer()
    words = map(lambda x: porter.stem(x), words)
    length = len(sentence)
    words_cnt = len(nltk.word_tokenize(sentence))
    return {'words': words, 'rating': rating, 'length': length,
        'words_cnt': words_cnt, 'orig_sentence': sentence}

def extract_features(features, document):
    document_words = set(document['words'])
    document_features = {'__words_cnt': document.get('words_cnt')}
    for word in features:
        document_features[word] = (word in document_words)
    return document_features

def load_data_corpus(corpora_data_file):
    df = pd.read_csv(corpora_data_file)

    df = df[df.FactoidType.str.startswith(\
        (   'judgement :: positive',
            'judgement :: negative',
            'judgement',
            '(none)',
            'fact',
            ))]

    data = df.as_matrix(columns = ['Review Rating', 'Sentence',\
        'FactoidType', 'ContextIndependence'])

    return data
