from mrjob.job import MRJob
from mrjob.step import MRStep

import pandas as pd

class MRWordFrequency(MRJob):

	def keyword_mapper(self, _, tweet):
		# read word from tweets column of tweetsDf from Tweepy_Test.py by row
		# yield each word in the line, and the row id
		for word in tweetsDf['tweets'](tweet):
			yield word.lower(), float(tweetsDf['id']

	def count_mapper(self, word, id):
		# second mapper
		# each word-id pair becomes key, add count of 1 as value
		yield (word, id), 1

	def word_counts(self, word, counts):
		# reducer
		# take sum of word counts for each tweet
		yield word, sum(counts)

	def steps(self):
		return [
		MRStep(mapper=self.keyword_mapper),
		MRStep(mapper=self.count_mapper,
			reducer=self.words_counts)
		]
if __name__ == '__main__'
	MRWordFrequency.run()