import random
import json
import pickle
import numpy as np
import nltk
import pymorphy2
import langid
from nltk.corpus import stopwords
from stop_words import get_stop_words
from nltk.stem import WordNetLemmatizer, PorterStemmer
from keras.models import load_model

langid.set_languages(['en', 'ru'])
stopWordsEn = set().union(get_stop_words('en'), stopwords.words('english'))
stopWordsRu = set().union(get_stop_words('ru'), stopwords.words('russian'))
stopWords = list(set().union(stopWordsEn, stopWordsRu))
stopWords.sort()
lemmatizer = WordNetLemmatizer()
stemmer = PorterStemmer()
morph = pymorphy2.MorphAnalyzer()
with open('intence.json', 'r', encoding='utf-8') as f:
    intents = json.load(f)

words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))
model = load_model('chatbot_model.h5')

def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    lemmedTokens = []
    for word in sentence_words:
        if word not in stopWords:
            if langid.classify(word)[0] == 'en':
                    lemmedTokens.append(stemmer.stem(word))
                    lemmedTokens.append(lemmatizer.lemmatize(word))
            elif langid.classify(word)[0] == 'ru':
                    lemmedTokens.append(morph.parse(word)[0].normal_form)
    return lemmedTokens

def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0]*len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)
def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]), verbose=0)[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]

    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({'intent': classes[r[0]], 'probability': str(r[1])})
    return return_list

def get_response(intents_list, intents_json):
    result = ''
    try:
        tag = intents_list[0]['intent']
        list_of_intents = intents_json['intents']
        for i in list_of_intents:
            if i['tag'] == tag:
                result = random.choice(i['responses'])
                break
        return result
    except:
        return result
def get_true_response(message: str) -> str:
    mem = message.lower()
    ints = predict_class(mem)
    res = get_response(ints, intents)
    if res == '':
        return
    else:
        return res