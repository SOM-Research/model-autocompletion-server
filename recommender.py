from scipy import spatial 
from collections import OrderedDict
import lemmatizer as lemmas

'''Given an embeddings dictionary and a embedding, we find the closest embeddings to it using the embeddings dictionary provided and return a sorted embeddings list.'''
def find_closest_embeddings(glove_emb_dict, embedding):
    return sorted(glove_emb_dict.keys(), key=lambda token: spatial.distance.euclidean(glove_emb_dict[token], embedding))    

'''Given an embeddings dictionary, a positive concepts list, a negative concepts list (terms we do not want to get suggestions related to them) and the number of suggestions we want,
we find the closest concepts to them using the embeddings dictionary provided and return a list of closest terms found.'''
def find_closest_concepts(glove_emb_dict, positiveconcepts, negativeconcepts, num):
    try:
        concepts_number = 2*num
        embeddings = glove_emb_dict[positiveconcepts[0]]
        for t in positiveconcepts: #range(1, len(concepts)):
            if t in glove_emb_dict:
                embeddings = embeddings + glove_emb_dict[t]
        for t in negativeconcepts:
            if t in glove_emb_dict:
                embeddings = embeddings - glove_emb_dict[t]
        closest_terms = find_closest_embeddings(glove_emb_dict, embeddings)[:concepts_number] 
        # closest_terms = set(closest_terms) - set(concepts) # remove words that we already have
        return closest_terms
    except Exception as e:
        print("No embeddings found")
    
'''Given an embeddings dictionary, a positive concepts list, a negative concepts list (terms we do not want to get suggestions related to them) and the number of suggestions we want,
we get glove suggestions through queries to the NLP Model.'''        
def get_glove_recommendations(glove_emb_dict, positiveconcepts, negativeconcepts, num):
    """
    Given a list of words, we don't only compute the closest words to the whole set, but also to its subsets,
    i.e., we have to campute the powerset of the original set.
    For instance, if we have {'1', '2', '3'}, we compute the closest_concepts for:
    {1}, {2}, {3}, {1, 2}, {1, 3}, {2, 3} and {1, 2, 3} and return a set with all the results.
    As we said in the comment of "find_closest_concepts", we should consider these sets as lists, permute them all
    and compute the closest terms for each permutation. Nevertheless, I've observed that the results are very similar
    and the performance degrades a lot, so I've commented the version below (which computes the powerset and then the 
    permutation and I've left a simplified one that only takes into account the powerset (done by hand).
    
    recomm = []
    for subset in tuple(powerset(words)):
        if (len(subset) != 0):
            perm = permutations(subset)
            for subset1 in list(perm):
                concepts = find_closest_concepts(subset1, num)
                recomm = recomm + concepts
    return list(OrderedDict.fromkeys(recomm)) #remove duplicates and return
    """
    aux = []
    recomm = []
    for w in positiveconcepts:
        aux.append(w)
        concepts = find_closest_concepts(glove_emb_dict, aux, negativeconcepts, num)
        if concepts is not None:
            recomm = recomm + concepts
    return recomm

'''Given an embeddings dictionary, a positive concepts list, a negative concepts list (terms we do not want to get suggestions related to them) and the number of suggestions we want,
we get glove suggestions through queries to the NLP Model. Before querying the model, we convert each positive concept lowercase and after getting GloVe suggestions we process 
recommendations with multiple lemmatizing, remove duplicate words from the suggestions list and remove words that belong to the negative words list. 
As part of lemmatizing we remove verbs and plurals from the suggestions list.'''  
def get_suggestions(glove_emb_dict, positiveconcepts, negativeconcepts, num):
    concepts = lemmas.lower(positiveconcepts)
    glove_suggestions = get_glove_recommendations(glove_emb_dict, concepts, negativeconcepts, num)

    wordnet_words = []
    for w in glove_suggestions:
        if lemmas.exists_in_wordnet(w):
            wordnet_words.append(w)
        wordnet_words = wordnet_words + lemmas.process_with_wordnet_multiple_lemmatizing(w) #lemmatizacion
    wordnet_words = list(OrderedDict.fromkeys(wordnet_words))

    wordnet_words = [ele for ele in wordnet_words if ele not in concepts] # remove words that are already present
    wordnet_words = [ele for ele in wordnet_words if ele not in negativeconcepts] # remove words that are negative words

    wordnet_words = lemmas.remove_verbs(wordnet_words)
    wordnet_words = lemmas.remove_plurals(wordnet_words)
    return wordnet_words


