from django.shortcuts import render
from .book_generator import book_generator
from .models import Book, Chapter, SubChapter, Genre, Tone, GenrePrompt, GenreContentPrompt

# Create your views here.

def bookcreate(request):

    return render(request, 'bookcreator/index.html')
