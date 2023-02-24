import openai
import os

genres = ['Romance','Mystery','Science Fiction', 'Fantasy', 'Horror',
        'Comics and graphic novels','Travel and adventure', 'Science and nature',
        'Religion and spirituality','Business and economics','Education and teaching',
        'Art and photography','Food and cooking','Sports and recreation',
        'Memoir and autobiography', 'Poetry', 'Drama','Children\'s books',
        'Biography', 'History', 'Self-help', 'Reference books']

tones_list = ['Humorous', 'Romantic', 'Mysterious', 'Lighthearted', 
                'Moody', 'Witty', 'Satirical', 'Informative', 'Suspenseful',
                'Thrilling', 'Inspiring', 'Somber', 'Educational', 'Sophisticated', 
                'Dramatic', 'Fantastical', 'Action-Packed']

# This class is used to generate a book
class BookGenerator:
        
        def __init__(self, genre, tone, title): 
        # Initializing the book generator
                self.genre = genre
                self.tone = tone
                self.title = title
                self.chapters = []

        def makeApiCall(self, prompt):
                """
                Makes an API call to OpenAI's API and returns the response

                args:
                prompt (str): The prompt to be used for the API call
                """
                openai.api_key = os.getenv("OPENAI_API_KEY")
                response = openai.Completion.create(
                        engine="davinci",
                        prompt=prompt,
                        temperature=0.9,
                        max_tokens=100,
                        top_p=1,
                        frequency_penalty=0,
                        presence_penalty=0,
                        stop=["\n", "Input:"]
                )
                response = response["choices"][0]["text"].strip()
                return response
        
        def validate(self):
                """Validates the genre, tone, and title of the book"""

                if self.genre not in genres:
                        raise ValueError("Genre not found")
                if type(self.genre) != str:
                        raise ValueError("Genre must be a string")
                if self.tone not in tones_list:
                        raise ValueError("Tone not found")
                if type(self.tone) != str:
                        raise ValueError("Tone must be a string")
                if self.title != str:
                        raise ValueError("Title must be a string")
                return True
        
        def generate_chapters(self):
                """Generates the chapters of the book"""
                if self.validate():
                        chapters_response = self.makeApiCall("Input: Genre\n" + self.genre + "\nInput: Tone\n" + self.tone + "\nInput: Title\n" + self.title + "\nInput: Chapter\n")
                        self.chapters.append(chapters_response["choices"][0]["text"].strip())
                        return self.chapters
                else:
                        raise ValueError("Invalid genre, tone, or title")

        def generate_book(self):
                """Generates the book"""
                if self.validate():
                        book_response = self.makeApiCall("Input: Genre\n" + self.genre + "\nInput: Tone\n" + self.tone + "\nInput: Title\n" + self.title + "\nInput: Book\n")
                        return book_response["choices"][0]["text"].strip()
                else:
                        raise ValueError("Invalid genre, tone, or title")