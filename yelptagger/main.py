import crawler
import model
import util

# NOTE, to make script work faster:
#   - decrease number of top frequent words taken in model.py/__get_word_features()
#   - decrease page offset limit in crawler.py/get_yelp_data()

if __name__ == '__main__':
    ### Load data corpus
    reviews = util.load_data_corpus('corpora.csv')

    ### Train classifiers
    print "Factoid model.."
    factoid_model = model.Model(map(lambda x: (x[0], x[1], x[2]), reviews),\
        util.parse_sentence)
    factoid_model.build_classifier(util.extract_features)

    print "Context independence model.."
    context_ind_model = model.Model(\
        map(lambda x: (x[0], x[1], x[3]), reviews), util.parse_sentence)
    context_ind_model.build_classifier(util.extract_features)

    ### Get Yelp data
    crawler = crawler.Crawler()
    yelp_data = crawler.get_yelp_data(\
        'http://www.yelp.com/biz/5-napkin-burger-new-york')

    print "Got", len(yelp_data), "yelp reviews"

    yelp_sentences = []
    for text in yelp_data:
        yelp_sentences.extend(util.sentence_tokenize(text))

    ### Predict
    predicted_factoids             = factoid_model.predict(\
        yelp_sentences, util.parse_sentence, util.extract_features)
    predicted_context_independence = context_ind_model.predict(\
        yelp_sentences, util.parse_sentence, util.extract_features)

    yelp_sentences = map(lambda x: x.encode('utf-8'), yelp_sentences)

    yelp_tagged = zip(yelp_sentences, predicted_factoids,\
        predicted_context_independence)

    ### Write to csv
    util.write_to_csv('yelp.predict.csv', yelp_tagged)
