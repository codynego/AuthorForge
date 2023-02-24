from django.db import models

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=100)

    def __str__(self):
        return self.title

class Chapter(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
class SubChapter(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Tone(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class GenrePrompt(models.Model):
    name = models.CharField(max_length=100)
    prompt = models.TextField()

    def __str__(self):
        return self.name

class GenreContentPrompt(models.Model):
    name = models.CharField(max_length=100)
    prompt = models.TextField()

    def __str__(self):
        return self.name
    

