import nltk
import nltk.classify.util
import senticnet

# Text analysis
from textblob import TextBlob

# Sentic Analysis from my package :P 
from sentic import SenticPhrase # 0.0.8

from nltk.classify import NaiveBayesClassifier
from nltk.corpus import stopwords, movie_reviews

from textblob import TextBlob
from fuzzywuzzy import fuzz

import nltk
from collections import defaultdict
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA


DEPRESSION_WORDS = ["abandoned", "achy", "afraid", "agitated", "agony", "alone", "anguish", "antisocial", "anxious",
 "breakdown", "brittle", "broken", "catatonic", "consumed", "crisis", "crushed", "crying",
 "defeated", "defensive", "dejected", "demoralized", "desolate", "despair", "desperate",
 "despondent", "devastated", "discontented", "disheartened", "dismal", "distractable", "distraught",
 "distressed", "doomed", "dreadful", "dreary", "edgy", "emotional", "empty", "excluded", "exhausted",
 "exposed", "fatalistic", "forlorn", "fragile", "freaking", "gloomy", "grouchy",
 "helpless", "hopeless", "hurt", "inadequate", "inconsolable", "injured", "insecure", "irrational",
 "irritable", "isolated", "lonely", "lousy", "low", "melancholy", "miserable", "moody", "morbid",
 "needy", "nervous", "nightmarish", "oppressed", "overwhelmed", "pain", "paranoid", "pessimistic",
 "reckless", "rejected", "resigned", "sadness", "self-conscious", "self-disgust", "shattered",
 "sobbing", "sorrowful", "suffering", "suicidal", "tearful", "touchy", "trapped", "uneasy", "unhappy",
 "unhinged", "unpredictable", "upset", "vulnerable", "wailing", "weak", "weepy", "withdrawn", "woeful",
 "wounded", "wretched"]

ALL_OR_NOTHING_LIST = ["anything", "everything", "nothing", "always", "never", "anytime", "all", \
                       "none", "whenever", "no one", "everyone", "nobody", "everybody", "no matter", "doesn't matter"]
JUMPING_TO_CONCLUSIONS_LIST = ["must be", "definitely", " will think", "'ll think", "obvious","definite"]
SHOULD_OR_MUST_LIST = ["should", "should've", "shouldn't"]

STOPWORDS = set(stopwords.words("english"))

READ_UNICODE = "rU"

distortions_string = lambda distortions: "We noticed from your writing some patterns of " + ', '.join(distortions)

labeling_string = """
Labeling is when we automatically assign judgements to ourselves or others based on one instance or experience.
"""

should_or_must_string = """
Should thinking is an immediate response to a situation that may link a situation with undeserved punishment.
"""

all_or_nothing_string = """
All-or-nothing thinking is an immediate response that tends to make certain situations appear either totally good or totally bad. 
"""

jumping_to_conclusions_string = """ 
Jumping to conclusions assumes definitive consequences, which may not always accurately reflect the reality of a situation.
"""

ending_practice = """
These types of thought patterns are also known as cognitive distortions. Practice breaking the thought patterns by challenging yourself with the following questions:
Can you think of any alternatives to the statements you’ve made?
What is the evidence to support the ideas you’ve suggested? Is there evidence to suggest against this idea? 
If the worst case scenario were to happen, have you thought about how you might cope?
What is the best case scenario? After thinking those through, what is the most realistic scenario to happen?
Think about what you might tell a family member or friend if they were in the same situation as you. What might you recommend to them? 

<a href='https://positivepsychologyprogram.com/cognitive-distortions/#what'>Learn more about cognitive distortions</a> and how you can overcome them.
"""

################
# Sentiment Prep
################
# def word_feats(words):
#     return dict([(word, True) for word in words])
 
# negids = movie_reviews.fileids('neg')
# posids = movie_reviews.fileids('pos')
 
# negfeats = [(word_feats(movie_reviews.words(fileids = [f])), 'neg') for f in negids]
# posfeats = [(word_feats(movie_reviews.words(fileids = [f])), 'pos') for f in posids]
 
# negcutoff = int(len(negfeats) * 3 / 4)
# poscutoff = int(len(posfeats) * 3 / 4)

# trainfeats = negfeats[:negcutoff] + posfeats[:poscutoff]
# testfeats = negfeats[negcutoff:] + posfeats[poscutoff:]
# print('train on %d instances, test on %d instances' % (len(trainfeats), len(testfeats)))
 
# SENTIMENT_CLASSIFIER = NaiveBayesClassifier.train(trainfeats)
# print('accuracy:', nltk.classify.util.accuracy(SENTIMENT_CLASSIFIER, testfeats))

# SENTIMENT_CLASSIFIER.show_most_informative_features()

# sn = Senticnet()


def get_text_metrics(text):
    '''
    Uses Polarity and Sentiment calculations based on Senticnet4
    Don't need semantics, because we're already dissected the object for its variables. 
    Keeping dictionary for concepts in case we want to just return that in the future or something.
    '''
    sp = SenticPhrase("")
    return sp.info(text)

    # return {"total_concept_words": len(sp.get_sentics()),
    #         "polarity_sum": sp.get_polarity(),
    #         "moodtags": sp.get_moodtags(),
    #         "semantics": sp.get_semantics(),
    #         "other_measurements": sp.get_sentics()}

    # total_concept_words = 0
    # polarity_sum = 0
    # moodtags = set()
    # semantics = set()
    # sentics = {'attention': 0, 'sensitivity': 0, 'pleasantness': 0, 'aptitude': 0}
    # concepts = {}

    ### Uses senticnet package, but can abstract with Sentic Package
    # for word in text.split():
    #     try:
    #         if word not in concepts:
    #             concepts[word] = sn.concept(word)
    #             moodtags = moodtags.union(set(sn.moodtags(word)))
    #             semantics = semantics.union(set(sn.semantics(word)))
    #         polarity_sum += float(sn.polarity_intense(word))
    #         other_measurements = sn.sentics(word)
    #         for measurement in other_measurements:
    #             sentics[measurement] += float(other_measurements[measurement])
    #         total_concept_words += 1
    #     except KeyError:
    #         continue

    # return {"total_concept_words": total_concept_words,
    #         "polarity_sum": polarity_sum,
    #         "moodtags": moodtags,
    #         "semantics": semantics,
    #         "other_measurements": sentics,
    #         "concepts": concepts}

  
## This one uses TextBlob
# def get_polarity_and_subjectivity(text):
#     '''
#     Uses TextBlob polarity and sentiment analysis.
#     '''
#     blob = TextBlob(text)
#     assessments = blob.sentiment_assessments.assessments
#     return {"polarity": float(blob.sentiment.polarity), "subjectivity": float(blob.sentiment.subjectivity)}


def get_keywords(text):
    ''' Prints out the top 10 topics among the given files. '''
    # https://stackoverflow.com/questions/20984841/topic-distribution-how-do-we-see-which-document-belong-to-which-topic-after-doi
    # https://stackoverflow.com/questions/37466345/assigning-a-topic-to-each-document-in-a-corpus-lda
    # http://www.vladsandulescu.com/topic-prediction-lda-user-reviews/
    # https://www.yelp.com/html/pdf/YelpDatasetChallengeWinner_ImprovingRestaurants.pdf


    text = [word for word in text.lower().split() if word not in STOPWORDS]
    all_tokens = text
    tokens_once = set(word for word in set(all_tokens) if all_tokens.count(word) == 1)
    texts = [word for word in text if word not in tokens_once]


    #############################
    # LDA Model Generation (BoW)
    #############################

    # Create Dictionary.
    id2word = corpora.Dictionary(texts)
    # Creates the Bag of Word corpus.
    mm = [id2word.doc2bow(text) for text in texts]

    # Trains the LDA models.
    # Tune hyperparameters for model
    lda_model = models.ldamodel.LdaModel(corpus = mm, id2word = id2word, num_topics = 25, \
                                   update_every = 1, chunksize = 1000, passes = 1)
    print("lda model generated.")

    # Prints the topics.
    words_and_weights = [tuple(word.replace('"', "").strip().split("*")) for word in lda_model.show_topics()[0][1].split("+")]
    sorted_words = sorted(words_and_weights, key = lambda value: value[1])
    for word_and_weight in sorted_words:
        print("Word and Weight: " + str(word_and_weight))

    # Assigns the topics to the documents in corpus
    lda_corpus = lda_model[mm]

    # Find the threshold, let's set the threshold to be 1/#clusters,
    # To prove that the threshold is sane, we average the sum of all probabilities:
    scores = list(chain(*[[score for topic_id,score in topic] \
                          for topic in [doc for doc in lda_corpus]]))
    threshold = sum(scores)/len(scores)
    print("Threshold:" + str(threshold))

    pdb.set_trace()

    # pdb.set_trace()
    return lda_model


def get_depression_factor(text):
    # Take a bunch of examples of depressed peoples' blog posts and writings
    # Take a bunch of normal people's blog posts and writings
    if text:
        occurances = sum([text.count(word) for word in DEPRESSION_WORDS])
        similarity = fuzz.ratio(text, ' '.join(DEPRESSION_WORDS))
        blob = TextBlob(text)
        return blob.sentiment.subjectivity + float(occurances) / len(text)


def get_cbt_metrics_and_suggestions(text):
    sentences = nltk.tokenize.sent_tokenize(text)
    len_text = len(sentences)
    cbt_metrics = {}
    distortions = set()
    definitions = set()
    for i, s in enumerate(sentences):
        # only if the sentence is negative should you give it a cbt distortion label        
        if sia.polarity_scores(s)['neg'] >= 0:
            for metric_name, metric_func in cbt_metrics_dict.items():
                word, defin = metric_func(s)
                if word != 0:
                    distortions.add(metric_name.replace('_', ' '))
                    definitions.add(defin)
                    if i in cbt_metrics:
                        cbt_metrics[i].append(word)
                    else:
                        cbt_metrics[i] = [word]
                    
    distortions = list(distortions)
    distortions[-1] = 'and ' + distortions[-1]
    return cbt_metrics, distortions_string(distortions), '\n'.join(definitions) + ending_practice


def all_or_nothing_thinking(s):
    words = nltk.tokenize.word_tokenize(s)

    ALL_OR_NOTHING_LIST.extend([x.capitalize() for x in ALL_OR_NOTHING_LIST])
    found_words = [word for word in words if word in ALL_OR_NOTHING_LIST]    
    return found_words


def jumping_to_conclusions(s):
    words = nltk.tokenize.word_tokenize(s)
    found_words = [word for word in words if word in JUMPING_TO_CONCLUSIONS_LIST]    
    return found_words


def should_or_must_thinking(s):
    words = nltk.tokenize.word_tokenize(s)
    found_words = [word for word in words if word in SHOULD_OR_MUST_LIST]   
    return found_words


def labeling(s):
    # rather than identifying particular nouns as being labeling, we'll just say that
    # if any words are seriously negative, its a label
    words = nltk.tokenize.word_tokenize(s)
    found_words = [word for word in words if TextBlob(word).sentiment.polarity > 0.75]
    return found_words
