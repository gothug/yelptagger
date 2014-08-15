import nltk
import functools
import random

import util

class Model:
    def __init__(self, learn_data_array, parse_func):
        self.learn_data_array = learn_data_array
        self.parse_func = parse_func

    def build_classifier(self, extract_features_func):
        self.__parse_learn_data()

        random.shuffle(self.learn_data_array)
        train_data, test_data = util.split_list(self.learn_data_array, 75) # percentage split for train/test data

        self.features = self.__get_word_features(train_data)

        train_set = nltk.classify.apply_features(\
            functools.partial(extract_features_func, self.features),\
            train_data)
        test_set  = nltk.classify.apply_features(\
            functools.partial(extract_features_func, self.features),\
            test_data)

        print "Total set length", len(self.learn_data_array)
        print "Train set length", len(train_set)
        print "Test set length",  len(test_set)

        classifier = nltk.NaiveBayesClassifier.train(train_set)

        print "Test set accuracy",\
            nltk.classify.accuracy(classifier, test_set)

        self.classifier = classifier

    def predict(self, data_array, parse_func, extract_features_func):
        data_array = map(lambda e: parse_func(e, 1), data_array)

        predicted_values = []

        for item in data_array:
            guess = self.classifier.classify(\
                extract_features_func(self.features, item))
            predicted_values.append(guess)

        return predicted_values

    def __parse_learn_data(self):
        learn_data_array = []

        for (rating, sentence, tag) in self.learn_data_array:
            learn_data_array.append(\
                (self.parse_func(sentence, 1), tag))

        self.learn_data_array = learn_data_array

    def __get_word_features(self, train_data):
        wordlist = nltk.FreqDist(self.__get_words(train_data))
        features = wordlist.keys()[:3000] # get N most frequent words for feature list
        return features

    def __get_words(self, data):
        return reduce(lambda x, y: x + y,\
            map(lambda e: e[0]['words'], data))
