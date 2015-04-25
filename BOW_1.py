#!/usr/bin/python
import re
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet as wn
from nltk.corpus import wordnet_ic
brown_ic = wordnet_ic.ic('ic-brown.dat')
def bow_score(hypothesis_list,text_list):
	wordnet_lemmatizer = WordNetLemmatizer()
	stop_word_list = ['a', 'an', 'the', ',', '.', ';', ':' ]
	i = 0
	while i < len(hypothesis_list):
		if hypothesis_list[i] in stop_word_list:
			del hypothesis_list[i]
			i = i - 1
		i = i  + 1
	if len(hypothesis_list) == 0:
		return 0
	i = 0	
	while i < len(text_list):
		if text_list[i] in stop_word_list:
			del text_list[i]
			i = i - 1
		i = i + 1
	if len(text_list) == 0:
		return 0
	## Stop words removed up until here

	score = 0	
	for word_text in text_list:
		lemma_text = wordnet_lemmatizer.lemmatize(word_text)
		for word_hypothesis in hypothesis_list:
			lemma_hypothesis = wordnet_lemmatizer.lemmatize(word_hypothesis)
			print lemma_hypothesis
			print lemma_text
			score += lexical_compare(lemma_text,lemma_hypothesis)
			print str(score)
	return score

def get_index(synset1,synset2):
	i = 0
	A = [(str(synset.name())) for synset in synset1] 			
	for word in A:
		if word.split('.')[1] == str(synset2[0].name()).split('.')[1]:
			return i
		i +=1
	return -1

def lexical_compare(lemma_text,lemma_hypothesis):
	similarity_score = 0
	brown_ic = wordnet_ic.ic('ic-brown.dat')
	if re.search(lemma_text,lemma_hypothesis,re.M|re.I):
		return 50
	hypo_synset = wn.synsets(lemma_hypothesis)
	text_synset = wn.synsets(lemma_text)
	synset_index = get_index(hypo_synset, text_synset)
	if synset_index == -1:
		return 0	
	if len(hypo_synset) > 0 and len(text_synset) > 0:
		similarity_score = hypo_synset[synset_index].path_similarity(text_synset[0],brown_ic)
		similarity_score += hypo_synset[synset_index].wup_similarity(text_synset[0],brown_ic)  
		similarity_score += hypo_synset[synset_index].lin_similarity(text_synset[0],brown_ic)  	
		similarity_score += hypo_synset[synset_index].res_similarity(text_synset[0],brown_ic)  	
	return similarity_score
		
	
def main():
	l1 = ['If','an','object','is','attracted','to','a','magnet',',','it','is','most','likely','made','of','metal']
	l2 = ['Cat','is','in','room']
	score = bow_score(l1,l2)	
	print score

if __name__ == "__main__":
    main()
