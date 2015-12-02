#http://www.nltk.org/install.html

def gender_features(word):
    return {'last_letter': word[-1]}

#gender_features(‘Shrek’) 

import nltk
from nltk.corpus import names
import random

names = ([(name, 'male') for name in names.words('male.txt')] + [(name, 'female') for name in names.words('female.txt')])

random.shuffle(names)

featuresets = [(gender_features(n), g) for (n,g) in names]

train_set, test_set = featuresets[500:], featuresets[:500]

classifier = nltk.NaiveBayesClassifier.train(train_set)
#classifier = nltk.NaiveBayesClassifier.train([({'last_letter': u't'}, 'female'), ({'last_letter': u'a'}, 'male')])

classifier.classify(gender_features('Neo'))
#classifier.prob_classify(gender_features('Neo')).prob('male')

classifier.classify(gender_features('Trinity'))
#classifier.classify({'last_letter': 't'})

classifier = classifier.train([({'last_letter': u'e'}, 'female'), ])  #增量学习
classifier.classify({'last_letter': 'e'})

print nltk.classify.accuracy(classifier, test_set)

classifier.show_most_informative_features(5)

classifier._label_probdist.freqdist().tabulate()

