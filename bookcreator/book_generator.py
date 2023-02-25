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

    def __init__(self, genre, tone, title, book_objective, target_audience):
        # Initializing the book generator
        self.genre = genre
        self.tone = tone
        self.title = title
        self.chapters = []
        self.book_objective = book_objective
        self.target_audience = target_audience

    def __str__():
        """ A string representation of the object """
        return "{} - {}"

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
            engine="text-davinci-003",
            prompt=prompt,
            temperature=0.7,
            max_tokens=1000,
        )
        response = response["choices"][0]["text"].strip()
        return response

    def validate(self):
        """Validates the genre, tone, and title of the book"""

        tones = [x.lower() for x in tones_list]
        genres_list = [x.lower() for x in genres]

        if self.genre.lower() not in genres_list:
            raise ValueError("Genre not found")
        if type(self.genre) != str:
            raise ValueError("Genre must be a string")
        if self.tone.lower() not in tones:
            raise ValueError("Tone not found")
        if type(self.tone) != str:
            raise ValueError("Tone must be a string")
        if type(self.title) != str:
            raise ValueError("Title must be a string")
        return True

    def generate_chapters(self):
        """Generates the chapters of the book"""
        if self.validate():
            chapter_prompt = self.generate_prompt("generate chapters")
            chapters_response = self.makeApiCall(chapter_prompt)
            return chapters_response
        else:
            raise ValueError("Invalid genre, tone, or title")

    def generate_book(self):
        """Generates the book"""
        if self.validate():
            prompt = self.load_json("generate chapters")
            book_response = self.makeApiCall()
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
            try:
                prompt = self.load_json(intent)
                prompt = prompt[self.genre]
                return prompt
            except Exception as e:
                print(f"Error loading json file: {str(e)}")
                return "invalid syntax"
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
            if prompt_type == "generate chapters":
                try:
                    with open('bookcreator/outlineprompt.json', 'r') as f:
                        chapter_prompt = json.load(f)
                    for k, v in chapter_prompt.items():
                        v = v.replace("[book title]", self.title)
                        v = v.replace("[writing tone]", self.tone)
                        v = v.replace("[book objective]", self.book_objective)
                        v = v.replace("[target audience]", self.target_audience)
                        chapter_prompt[k] = v
                    return chapter_prompt
                except Exception as e:
                    print(f"Error loading json file: {str(e)}")
                    return "invalid"
            elif prompt_type == "generate content":
                try:
                    with open('bookcreator/genres.json', 'r') as f:
                        content_prompt = json.load(f)
                    for k, v in content_prompt.items():
                        v = v.replace("[insert sub-chapter title]", self.subchapter)
                        v = v.replace("[insert chapter title]", self.chaptertitle)
                        v = v.replace("[insert book title]", self.title)
                        v = v.replace("[writing tone]", self.tone)
                        content_prompt[k] = v
                    return content_prompt
                except Exception as e:
                    print(f"Error loading json file: {str(e)}")
                    return "invalid"
            else:
                raise ValueError("Invalid prompt type")
        else:
            raise ValueError("Invalid genre, tone, or title")
        
    def split_chapters(self, chapters):
        """Splits the chapters into a subchapter list"""
        parts = {}
        current_part = ""
        for line in chapters.split('\n'):
            if line.startswith("Part "):
                current_part = line.strip()
                parts[current_part] = []
            elif line.startswith("Chapter "):
                parts[current_part].append(line.strip())

        return (parts)


b1 = BookGenerator("Self-help", "inspiring", "The Book of Life", "to inspire people", "everyone")
#print(b1.generate_chapters())
print(b1.split_chapters(b1.generate_chapters()))
