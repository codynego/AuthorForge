from django.contrib import admin
from .models import Book, Chapter, SubChapter, Genre, Tone, GenrePrompt, GenreContentPrompt

# Register your models here.
admin.site.register(Book)
admin.site.register(Chapter)
admin.site.register(SubChapter)
admin.site.register(Genre)
admin.site.register(Tone)
admin.site.register(GenrePrompt)
admin.site.register(GenreContentPrompt)
