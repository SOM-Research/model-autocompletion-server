from nltk.corpus import wordnet as wn, stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import nltk 
import re
nltk.download('wordnet')
nltk.download('stopwords')
nltk.download('punkt')
lemma = WordNetLemmatizer()

contractions_list = {
  "ain't": "am not",
  "aren't": "are not",
  "can't": "cannot",
  "can't've": "cannot have",
  "'cause": "because",
  "could've": "could have",
  "couldn't": "could not",
  "couldn't've": "could not have",
  "didn't": "did not",
  "doesn't": "does not",
  "don't": "do not",
  "hadn't": "had not",
  "hadn't've": "had not have",
  "hasn't": "has not",
  "haven't": "have not",
  "he'd": "he would",
  "he'd've": "he would have",
  "he'll": "he will",
  "he'll've": "he will have",
  "he's": "he is",
  "how'd": "how did",
  "how'd'y": "how do you",
  "how'll": "how will",
  "how's": "how is",
  "i'd": "I would",
  "i'd've": "I would have",
  "i'll": "I will",
  "i'll've": "I will have",
  "i'm": "I am",
  "i've": "I have",
  "isn't": "is not",
  "it'd": "it had",
  "it'd've": "it would have",
  "it'll": "it will",
  "it'll've": "it will have",
  "it's": "it is",
  "let's": "let us",
  "ma'am": "madam",
  "mayn't": "may not",
  "might've": "might have",
  "mightn't": "might not",
  "mightn't've": "might not have",
  "must've": "must have",
  "mustn't": "must not",
  "mustn't've": "must not have",
  "needn't": "need not",
  "needn't've": "need not have",
  "o'clock": "of the clock",
  "oughtn't": "ought not",
  "oughtn't've": "ought not have",
  "shan't": "shall not",
  "sha'n't": "shall not",
  "shan't've": "shall not have",
  "she'd": "she would",
  "she'd've": "she would have",
  "she'll": "she will",
  "she'll've": "she will have",
  "she's": "she is",
  "should've": "should have",
  "shouldn't": "should not",
  "shouldn't've": "should not have",
  "so've": "so have",
  "so's": "so is",
  "that'd": "that would",
  "that'd've": "that would have",
  "that's": "that is",
  "there'd": "there had",
  "there'd've": "there would have",
  "there's": "there is",
  "they'd": "they would",
  "they'd've": "they would have",
  "they'll": "they will",
  "they'll've": "they will have",
  "they're": "they are",
  "they've": "they have",
  "to've": "to have",
  "wasn't": "was not",
  "we'd": "we had",
  "we'd've": "we would have",
  "we'll": "we will",
  "we'll've": "we will have",
  "we're": "we are",
  "we've": "we have",
  "weren't": "were not",
  "what'll": "what will",
  "what'll've": "what will have",
  "what're": "what are",
  "what's": "what is",
  "what've": "what have",
  "when's": "when is",
  "when've": "when have",
  "where'd": "where did",
  "where's": "where is",
  "where've": "where have",
  "who'll": "who will",
  "who'll've": "who will have",
  "who's": "who is",
  "who've": "who have",
  "why's": "why is",
  "why've": "why have",
  "will've": "will have",
  "won't": "will not",
  "won't've": "will not have",
  "would've": "would have",
  "wouldn't": "would not",
  "wouldn't've": "would not have",
  "y'all": "you all",
  "y'alls": "you alls",
  "y'all'd": "you all would",
  "y'all'd've": "you all would have",
  "y'all're": "you all are",
  "y'all've": "you all have",
  "you'd": "you had",
  "you'd've": "you would have",
  "you'll": "you you will",
  "you'll've": "you you will have",
  "you're": "you are",
  "you've": "you have"
}

subjects = {"i", "you", "he", "she", "it", "we", "they"}

c_re = re.compile('(%s)' % '|'.join(contractions_list.keys()))

'''Given a text and a list of common contractions, this method replaces each contraction and adds its expanded form.'''
def expand_contractions(text, c_re=c_re):
    def replace(match):
        return contractions_list[match.group(0)]
    return c_re.sub(replace, text.lower())

'''Given a list of words, we remove the subjects from it and return a new list without subjects.'''
def remove_subjects(list):
    list_without_subjects = []
    for item in list:
        if not item.lower() in subjects:
            list_without_subjects.append(item)
    return list_without_subjects

'''Given a string, we remove the punctuation symbols such as dots, commas, quotation marks, hashtags... and return a new string without punctuation symbols.'''
def remove_punctuation(string):
    punctuation = '''!()-[]{};:`'"\, <>./?@#$%^&*_~—‘’“”'''
    for ele in string:  
        if ele in punctuation:  
            string = string.replace(ele, "") 
    return string

'''Given a path to a file, we open the file and read its content. For each line in the file, we expand contractions, tokenize the text and remove stop words. 
We return a filtered sentence list.'''
def tokenize_text(path):
    stop_words = set(stopwords.words('english'))
    filtered_sentence = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            expanded = expand_contractions(line)
            word_tokens = word_tokenize(expanded)
            for w in word_tokens:
                if w not in stop_words:
                    filtered_sentence.append(w)
    return filtered_sentence 

'''Given a word, we check if it exists in wordnet or not.'''
def exists_in_wordnet(word):
    return len(wn.synsets(word)) > 0

'''Given an input word, we get its POS to know if it is a verb, noun, adjective...'''    
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

'''Given an input word, we check if it exists in wordnet or not.'''    
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

'''Given an input word, we check if it is a verb or not.'''   
def is_verb(input_word):
    pos = get_pos(input_word)
    return 'v' in pos

'''Given an input word, we check if it is a noun or not.'''  
def is_noun(input_word):
    pos = get_pos(input_word)
    return 'n' in pos

'''Given a list of words, we lemmatize the whole list and return a list with lemmatized words, excluding those that don't exist after lemmmatizing.'''  
def lemmatize_list(list):
    result = []
    for word in list:
        lemmatized = lemmatizer(word)
        if lemmatized != None:
            result.append(lemmatized)
    return result

'''Given a word, we lemmatize it and return it to the user.'''  
def lemmatizer(input_word):
    result = lemma.lemmatize(input_word)
    return result

'''
def lemmatize(input_word):
    m = wn.morphy(input_word)
    return m
    
'''

'''Given a word, we lemmatize it as a verb and return it to the user.''' 
def lemmatize_as_verb(input_word):
    m = wn.morphy(input_word, wn.VERB)
    return m

'''Given a word, we lemmatize it as a noun and return it to the user.''' 
def lemmatize_as_noun(input_word):
    m = wn.morphy(input_word, wn.NOUN)
    return m

'''Given a word, we check if it is plural or not.''' 
def is_plural(word):
    lemma = wn.morphy(word, 'n')
    plural = True if word is not lemma else False
    return plural

'''Given a word, we process it with wordnet multiple lemmatizing. First as a verb, then as a noun. It returns None if after lemmatization the word doesnt exist.''' 
def process_with_wordnet_multiple_lemmatizing(input_word):
    result = []
    word = lemmatize_as_verb(input_word)
    if word != None:
        result.append(word)
    word = lemmatize_as_noun(input_word)
    if word != None:
        result.append(word)
    return result 

'''Given a list of words we remove verbs and nouns from it and return a new list without verbs and nouns.'''
def remove_verbs(list):
    result = []
    for w in list:
        if not (is_verb(w) and (not is_noun(w))):
            result.append(w)
    return result

'''Given a list of words we remove plurals from it and return a new list without plurals.'''    
def remove_plurals(list):
    result = []
    for w in list:
        if not is_plural(w):
            result.append(w)
    return result

'''Given a list of words, for each word in the list, we write it lowercase and return a list containing lowercase words.'''
def lower(x):
    return [element.lower() for element in x] ; 
