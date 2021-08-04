
from nltk.corpus import wordnet as wn, stopwords
from nltk.tokenize import word_tokenize
import nltk 
nltk.download('wordnet')
nltk.download('stopwords')
nltk.download('punkt')

def remove_punctuation(string):
    punctuation = '''!()-[]{};:'"\, <>./?@#$%^&*_~—'''
    for ele in string:  
        if ele in punctuation:  
            string = string.replace(ele, "") 
    return string

def tokenize_text(path):
    stop_words = set(stopwords.words('english'))
    filtered_sentence = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            word_tokens = word_tokenize(line)
            for w in word_tokens:
                if w not in stop_words:
                    filtered_sentence.append(w)
    return filtered_sentence 

def exists_in_wordnet(word):
    return len(wn.synsets(word)) > 0
    
def get_pos(input_word):
    # v = verb; n = noun; a = s = adjective; s = ; r = adverb; 
    synset = wn.synsets(input_word)
    is_verb = False
    pos = set()
    for syn in synset:
        # print(syn)
        s = syn.name().split('.')
        pos.add(s[1])
    return pos

def exists_as_is(input_word):
    synsets = wn.synsets(input_word)
    exists = False
    i = 0
    while not exists and i < len(synsets):
        syn = synsets[i]
        s = syn.name().split('.')
        if (s[0] == input_word):
            exists = True
        i = i+1
    return exists

def is_verb(input_word):
    pos = get_pos(input_word)
    return 'v' in pos

def is_noun(input_word):
    pos = get_pos(input_word)
    return 'n' in pos

def lemmatize_list(list):
    result = []
    for word in list:
        lemmatized = lemmatize(word)
        if lemmatized != None:
            result.append(lemmatized)
    return result

def lemmatize(input_word):
    m = wn.morphy(input_word)
    return m
    
def lemmatize_as_verb(input_word):
    m = wn.morphy(input_word, wn.VERB)
    return m

def lemmatize_as_noun(input_word):
    m = wn.morphy(input_word, wn.NOUN)
    return m

def isplural(word):
    lemma = wn.morphy(word, 'n')
    plural = True if word is not lemma else False
    return plural

def process_with_wordnet_multiple_lemmatizing(input_word):
    # we lemmatize each word as noun and verb
    result = []
    word = lemmatize_as_verb(input_word)
    if word != None:
        result.append(word)
    word = lemmatize_as_noun(input_word)
    if word != None:
        result.append(word)
    return result # it will return None if after lemmatization the word doesnt exist

def removeVerbs(list):
    result = []
    for w in list:
        if not (is_verb(w) and (not is_noun(w))):
            result.append(w)
    return result
    
def removePlurals(list):
    result = []
    for w in list:
        if not isplural(w):
            result.append(w)
    return result
