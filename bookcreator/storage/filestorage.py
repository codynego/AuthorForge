import json
import os
from bookcreator.book_generator import BookGenerator

# This class is used to store the book in a file storage

class FileStorage:
	""" This class is used to store the book in a file storage """

	book_list = {}

	def __init__(self):
		""" 
		Initializing the file 

		Args:
		title (str): 
		"""
		self.filename = "filestorage.json"

	def new(self, obj):
		"""add a new item to the list of books """
		key = "{} '{}'".format(obj.title, obj.generate_chapters())
		self.book_list[key] = obj

		return self.book_list
	

b1 = BookGenerator("Self-help", "inspiring", "The Book of Life", "to inspire people", "everyone")
f1 = FileStorage()
print(f1.new(b1))






