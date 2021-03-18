
from mrjob.job import MRJob
from mrjob.step import MRStep
from math import log

import pandas as pd

class MRWordFrequency(MRJob):
	
	def keyword_mapper(self, _, tweet):
		# read word from tweets column of tweetsDf from Tweepy_Test.py by row
		# yield each word in the line, and the row id
		# set N to number of docs in collection
		N = len(tweetsDf['id'])
		for word in tweetsDf['tweets'](tweet):
			yield (word.lower(), N), float(tweetsDf['id'])

    def count_combiner(self, word, id):
		# combiner
		# each word-id pair becomes key, add count of 1 as value
		yield (word, N, id) , 1

	def word_counts(self, word_id, counts):
		# reducer
		# take sum of word counts for each word per tweet id
		yield word, (id, N, sum(counts))

	def total_word_mapper(self, word, doc_counts):
		# second mapper
		# make list of ids where word occurs
		# keep running total of word ocurrence in collection
		# make list of sums to match ids in list
		# yield word, word occurence for doc, total
		ids = []
		total = 0
		occurence = []
		for value in doc_counts:
			ids.append(value[0])
			total += value[2]
			occurence.append(value[2])
		for value in range(N):
			yield word, (ids[value], occurence[value], total)


	def tfidf_reducer(self, word, weights):
		# 2nd reducer
		# calculate idf for word
		# take word, calculate tf.idf
		# yield word, (id, tf.idf)
		n = len(occurence)
		idf = log(N/n)
		tfidfs = []
		for value in weights:
			tfidf.append(occurence[value]*idf)
		for value in range(N):
			yield word, (weights[0], tfidfs[value])


	def steps(self):
		# multistep MR
		return [
		MRStep(mapper=self.keyword_mapper, 
			combiner=self.count_combiner,
			reducer=self.word_counts),
		MRStep(mapper=self.total_word_mapper,
			reducer=self.tfidf_reducer)
		]
		
if __name__ == '__main__'
	MRWordFrequency.run()

