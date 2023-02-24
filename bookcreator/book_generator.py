import openai
import os
import json

genres = ['Romance', 'Mystery', 'Science Fiction', 'Fantasy', 'Horror',
          'Comics and graphic novels', 'Travel and adventure', 'Science and nature',
          'Religion and spirituality', 'Business and economics', 'Education and teaching',
          'Art and photography', 'Food and cooking', 'Sports and recreation',
          'Memoir and autobiography', 'Poetry', 'Drama', 'Children\'s books',
          'Biography', 'History', 'Self-help', 'Reference books']

tones_list = ['Humorous', 'Romantic', 'Mysterious', 'Lighthearted',
              'Moody', 'Witty', 'Satirical', 'Informative', 'Suspenseful',
              'Thrilling', 'Inspiring', 'Somber', 'Educational', 'Sophisticated',
              'Dramatic', 'Fantastical', 'Action-Packed']


# This class is used to generate a book
class BookGenerator:

    def __init__(self, genre, tone, title, book_objective=None, target_audience=None):
        # Initializing the book generator
        self.genre = genre
        self.tone = tone
        self.title = title
        self.chapters = []
        self.book_objective = book_objective
        self.target_audience = target_audience
        

    def get_genre(self):
        """Returns the genre of the book"""
        return self.genre

    def get_tone(self):
        """Returns the tone of the book"""
        return self.tone

    def get_title(self):
        """Returns the title of the book"""
        return self.title

    def get_chapters(self):
        """Returns the chapters of the book"""
        return self.chapters

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
        if type(self.title) != str:
            raise ValueError("Title must be a string")
        return True

    def generate_chapters(self):
        """Generates the chapters of the book"""
        if self.validate():
            chapters_response = self.makeApiCall(
                "Input: Genre\n" + self.genre + "\nInput: Tone\n" + self.tone + "\nInput: Title\n" + self.title + "\nInput: Chapter\n")
            self.chapters.append(
                chapters_response["choices"][0]["text"].strip())
            return self.chapters
        else:
            raise ValueError("Invalid genre, tone, or title")

    def generate_book(self):
        """Generates the book"""
        if self.validate():
            book_response = self.makeApiCall(
                "Input: Genre\n" + self.genre + "\nInput: Tone\n" + self.tone + "\nInput: Title\n" + self.title + "\nInput: Book\n")
            return book_response["choices"][0]["text"].strip()
        else:
            raise ValueError("Invalid genre, tone, or title")

    def generate_prompt(self, intent):
        """ 
        returns the prompt for the given intent based on the title, 
        genre and tone of the book

        args:
        intent (str): The intent of the prompt (generate chapters or generate chapter content)

        """
        intent_list = ["generate chapters", "generate content"]
        if intent not in intent_list:
            raise ValueError("Intent not found")
        if type(intent) != str:
            raise ValueError("Intent must be a string")
        if self.validate():
            if intent == "generate chapters":
                try:
                    with open('genres.json', 'r') as f:
                        genres = json.load(f)
                except:
                    genres = {}
                return "Input: Genre\n" + self.genre + "\nInput: Tone\n" + self.tone + "\nInput: Title\n" + self.title + "\nInput: Chapter\n"
            elif intent == "generate content":
                return "Input: Genre\n" + self.genre + "\nInput: Tone\n" + self.tone + "\nInput: Title\n" + self.title + "\nInput: Content\n"
        else:
            raise ValueError("Invalid genre, tone, or title")

    def load_json(self, prompt_type):
        """Loads the json file and returns the prompt"""

        # Check if the prompt type is valid
        prompt_types = ["generate chapters", "generate content"]
        if prompt_type not in prompt_types:
            raise ValueError("Invalid prompt type")
        if type(prompt_type) != str:
            raise ValueError("Prompt type must be a string")
        
        # Check if the genre, tone, and title are valid
        if self.validate():
            # Check if the prompt type is generate chapters
            if prompt_type == "generate content":
                try:
                    with open('bookcreator/genres.json', 'r') as f:
                        data = json.load(f)
                        data_prompt = data[self.genre]
                        data_prompt = data_prompt.replace("[insert chapter title]", self.genre)
                        data_prompt = data_prompt.replace("[writing tone]", self.tone)
                        data_prompt = data_prompt.replace("[insert book title]", self.title)

                        return data_prompt
                except:
                    return "Invalid statement"
            elif prompt_type == "generate chapters":
                try:
                    with open('bookcreator/outlineprompt.json', 'r') as f:
                        data = json.load(f)
                        data_prompt = data[self.genre]
                        data_prompt = data_prompt.replace("[book title]", self.title)
                        data_prompt = data_prompt.replace("[writing tone]", self.tone)
                        data_prompt = data_prompt.replace("[book objective]", self.book_objective)
                        data_prompt = data_prompt.replace("[target audience]", self.target_audience)
                        return data_prompt
                except:
                    return "Invalid statement"

b1 = BookGenerator("Fantasy", "Informative", "The Book of the Dead", "To entertain", "Children")
print(b1.load_json("generate chapters"))
