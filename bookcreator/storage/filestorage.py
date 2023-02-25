import json
import os
from book_generator import BookGenerator

# This class is used to store the book in a file storage

class FileStorage:
	""" This class is used to store the book in a file storage """

	def __init__(self, title, chapters):
		""" 
		Initializing the file 

		Args:
		title (str): 
		"""
		self.filename = "filestorage.json"
		self.title = title
		self.chapters = chapters
		book_list = []

	def new(self):
		"""add a new item to the list of books """
		







