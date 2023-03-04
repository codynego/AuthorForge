import json
from bookcreator.book_generator import BookGenerator
import requests
from bs4 import BeautifulSoup


class ArticleSummarizer:
	"""
	Summarizes article either from blog post link or articles using openai Api
	"""

	def __init__(self, article=None, link=None):
		self.article = article
		self.link = link

		if self.article is None and self.link is None:
			raise ValueError("Article or link must be provided")
		elif self.article is not None and self.link is not None:
			raise ValueError("Only one of article or link must be provided")
		elif self.link is not None:
			self.article = None

	def __str__(self):
		return f"Article Summarizer"

	def writeprompt(self):
		"""
		Writes prompt to be used by openai api
		"""
		if self.link is None:
			prompt = f"Please summarize the following article:\
			{self.article} Provide a summary of the main points \
			covered in the article, including any important information,\
			key takeaways, or notable insights"
		else:
			prompt = f"Please summarize the article from the following link:\
			{self.link} Provide a summary of the main points \
			covered in the article, including any important information,\
			key takeaways, or notable insights"

		return prompt
	
	def summarize(self):
		"""
		Summarizes article
		"""
		prompt = self.writeprompt()
		summarized_article = BookGenerator.makeApiCall(self, prompt)
		return summarized_article.strip()
	
	def translate(self, language):
		"""
		Translates article to specified language
		"""
		language = language.lower()
		prompt = "given this link {}, Please translate the following article to {}".format(self.link, language)
		translated_article = BookGenerator.makeApiCall(self, prompt)
		return translated_article.strip()
	

"""a1 = ArticleSummarizer("Meditation is a practice that has been around for thousands of years and is believed to have originated in ancient India. Over time, it has spread throughout the world and is now practiced by millions of people for its many benefits to both the mind and body.\
		       One of the most well-known benefits of meditation is its ability to reduce stress and anxiety. Studies have shown that regular meditation practice can lower levels of cortisol, the hormone that is released in response to stress. This can help to reduce feelings of anxiety and improve overall mental health.\
		       Meditation has also been shown to improve focus and concentration. This is because the practice requires you to focus your attention on a single point, such as your breath or a mantra. Over time, this can help to improve your ability to concentrate on other tasks as well.\
		       In addition to these benefits, meditation has also been shown to improve sleep quality, reduce symptoms of depression, and even lower blood pressure. It is a simple and effective way to promote overall health and well-being")"""
#a1 = ArticleSummarizer(link="https://www.simplilearn.com/tutorials/programming-tutorial/what-is-software-development")
#print(a1.translate("Spanish"))