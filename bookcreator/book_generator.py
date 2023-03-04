import openai
import os
import re
import json
import time
import traceback
import spacy



"""genres = ['Romance', 'Mystery', 'Science Fiction', 'Fantasy', 'Horror',
          'Comics and graphic novels', 'Travel and adventure', 'Science and nature',
          'Religion and spirituality', 'Business and economics', 'Education and teaching',
          'Art and photography', 'Food and cooking', 'Sports and recreation',
          'Memoir and autobiography', 'Poetry', 'Drama', 'Children\'s books',
          'Biography', 'History', 'Self-help', 'Reference books']"""

genres = ['Science and nature', 'Religion and spirituality',
          'Business and economics', 'Education and teaching',
          'Art and photography', 'Food and cooking', 
          'Sports and recreation', 'Memoir and autobiography', 
          'Poetry', 'Drama', 'Children\'s books', 'Biography',
          'History', 'Self-help', 'Reference books']


tones_list = ["Informative","Romantic", "Instructive", "Persuasive",
        "Entertaining", "Inspiring", "Serious", "Humorous",
        "Formal", "Conversational", "Friendly"]


tone_descriptions = {
    "Informative": "conveying useful and accurate information on a topic",
    "Instructive": "conveying step-by-step guidance or instructions",
    "Persuasive": "aiming to convince the reader of a certain viewpoint",
    "Entertaining": "providing enjoyment, amusement, or diversion",
    "Inspiring": "aiming to motivate or encourage the reader",
    "Serious": "conveying a weighty or significant message or tone",
    "Humorous": "aiming to amuse or make the reader laugh",
    "Formal": "using proper language, grammar, and syntax",
    "Conversational": "using everyday language and tone",
    "Friendly": "conveying a warm and approachable tone"
}

chapter_prompt = "Imagine you are a writer tasked with creating the chapter\
and subchapter outline for a new book. The book title is \
[insert title], the genre is [insert genre], the book objective\
is [insert objective], and the target audience is [insert audience]. Using this information, create a detailed chapter and subchapter outline for the book that\
will effectively achieve the book objective and resonate\
with the target audience. The chapters should be [chapter number] and for each chapters, the subchapters should be 5. use the outline below as reference.\
\nIntroduction\n[subintro]:\nChapter 1:\n[subchater]:\n[subchapter]:\n[subchapter]:\n[subchapter]:\nConclusion\n[subconclusion]:"




# This class is used to generate a book
class BookGenerator:
    uid = 0
    def __init__(self, genre, tone, title, book_objective, target_audience):
        # Initializing the book generator
        self.id = self.uid + 1
        self.genre = genre
        self.tone = tone
        self.title = title
        self.sections = []
        self.book_objective = book_objective
        self.target_audience = target_audience

        self.uid += 1

    def __str__(self):
        """ A string representation of the object """
        return "[{}] - {}".format(self.title, self.generate_chapters())

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
            max_tokens=3000,
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
            prompt = chapter_prompt
            prompt = prompt.replace("[insert title]", self.title)
            prompt = prompt.replace("[chapter number]", "10")
            prompt = prompt.replace("[insert objective]", self.book_objective)
            prompt = prompt.replace("[insert audience]", self.target_audience)

            chapters = self.makeApiCall(prompt)
            return (chapters)
        else:
            raise ValueError("Invalid genre, tone, or title")

    def generate_book(self, chapters_dict=None):
        """
        Generates the content of the book and saved to a txt file

        Args:
        chapters_dict (dict): A dictionary containing Parts, chapters, subchapter and sections

        """

        outline = self.split_chapters()
        #print(chapters_split)
        if outline is None or len(outline) == 0 or type(outline) != dict:
            self.generate_book()
            #raise ValueError("No chapters found")
        if self.validate():
            try:
                for k, chapters in outline.items():
                    if len(chapters) == 0:
                        self.generate_book(self)
                        #raise ValueError("No chapters found")
                    else:
                        chapter = k.strip()
                        try:
                            with open("bookcreator/book.txt", "a") as f:
                                f.write(f"Chapter: {chapter}\n")
                        except Exception as e:
                            print(f"Error writing to file: {str(e)}")
                    
                    for subchapter in chapters:
                        subchapter = subchapter.strip()
                        #chapter_title = i.split(":")[1].strip()
                        previous_subchapters = []
                        prompt = self.generate_prompt(subchapter, previous_subchapters)
                        time.sleep(1)
                        subchapter_content = self.makeApiCall(prompt)
                        subchapter_content = self.remove_conclusion(subchapter_content)
                        previous_subchapters.append(subchapter)
                        try:
                            with open("bookcreator/book.txt", "a") as f:
                                f.write(f"{subchapter_content}\n\n")
                        except Exception as e:
                            print(f"Error writing to file: {str(e)}")
                
                return "Book generated successfully"
                
            except Exception as e:
                print(f"Error generating book: {str(e)}")
                traceback.print_exc()
        else:
            raise ValueError("Invalid genre, tone, or title")

    def generate_prompt(self, subchapter, previous_subchapters):
        """ 
        returns the prompt for the given intent based on the title, 
        genre and tone of the book

        args:
        intent (str): The intent of the prompt (generate chapters or generate chapter content)
        chapter_title (str): The title of the chapter (default=None)
        subchapter (str): The title of the sub chapter (default=None)
        prev_chapter (str): The name of the previous sub chapter (default=None)

        """
        intent_list = ["generate chapters", "generate content"]
        if self.validate():
            try:
                prompt = self.load_json(subchapter, previous_subchapters)
                prompt_lowercase = {k.lower(): v for k, v in prompt.items()}
                prompt_pp = prompt_lowercase[self.genre.lower()]
                return prompt_pp
            except Exception as e:
                traceback.print_exc()
        else:
            raise ValueError("Invalid genre, tone, or title")
        
    def load_json(self,subchapter):
        """
        Loads the json file and returns the prompt

        Args:
        prompt (str): The type of prompts to load, it can be (generate chapters or generate content)
        chapter_title (str): The title of the chapter
        subchapter (str): The title of the sub chapter
        prev_chapter (str): The name of the previous sub chapter

        """

        # Check if the genre, tone, and title are valid
        if self.validate():
            content_prompt = {}
            try:
                with open('bookcreator/contprompt.json', 'r') as f:
                    content_prompt = json.load(f)
                for k, v in content_prompt.items():
                    v = v.replace("[objective]", self.book_objective)
                    v = v.replace("[subchapter title]", subchapter)
                    v = v.replace("[tone]", self.tone)
                    v = v.replace("[previous subchapter]", str(previous_subchapters))
                    v = v.replace("[book title]", self.title)
                    content_prompt[k] = v
                return dict(content_prompt)
            except Exception as e:
                traceback.print_exc()
                return "invalid"
        else:
            raise ValueError("Invalid genre, tone, or title")
        
    def split_chapters(self):
        """
        Splits the generated chapters into a dictionary of dictionaries
        The dictionary contains
        {
            Part title
             chapter title
               subchapter title
                 [list of sections]
            }
        Args: 
        obj (str): The object to split its dictionary
        """
        
        chapters = {}
        current_chapter = None
        chapters["Introduction"] = []
        text = self.generate_chapters()

        for line in text.split("\n"):

            if line.lower().startswith("[introduction]") or line.lower().startswith("-[introduction]"):
                chapters["Introduction"] = []

            elif line.startswith("[subintro") or line.startswith("[Subintro]"):
                if ":" in line:
                    subintro = line.split(":")[1].strip()
                elif "-" in line:
                    subintro = line.split("-")[1].strip()
                chapters["Introduction"].append(subintro)

            elif line.strip().lower().startswith("chapter"):
                if ":" in line:
                    current_chapter = line.split(":")[1].strip()
                elif "-" in line:
                    current_chapter = line.split("-")[1].strip()
                chapters[current_chapter] = []

            elif line.strip().lower().startswith("conclusion"):
                chapters["Conclusion"] = []

            elif line.strip().lower().startswith("-[subconclusion") or line.strip().startswith("[subconclusion"):
                if ":" in line:
                    subconclude = line.split(":")[1].strip()
                elif "-" in line:
                    subconclude = line.split("-")[1].strip()
                chapters["Conclusion"].append(subconclude)

            elif line.strip().startswith("[subchapter") or line.strip().startswith("[Subchapter"):
                if ":" in line:
                    subchap = line.split(":")[1].strip()
                elif "-" in line:
                    subchap = line.split("-")[1].strip()
                chapters[current_chapter].append(subchap)
        print(text)
        return chapters
        
    def format_text(self):
        """
        Formats the text to be a book
        """
        if self.validate():
            try:
                with open("bookcreator/book.txt", "r") as f:
                    text = f.read()
                text = text.split("\n")
                for word in text:
                    if word.startswith("Chapter Title:"):
                        text.remove(word)
                    elif word.startswith("Subchapter Title:"):
                        text.remove(word)
                    elif word.startswith("Tone:"):
                        text.remove(word)
                    elif word.startswith("Book Objective:"):
                        text.remove(word)
                    elif word.startswith("Target Audience:"):
                        text.remove(word)
                    elif word.startswith("Conclusion:") or word.startswith("Conclusion"):
                        text.remove(word)
                    elif word.startswith("##Conclusion"):
                        text.remove(word)
                    elif word.startswith("Introduction:"):
                        text.remove(word)
                    elif word.startswith("Content"):
                        text.remove(word)

                with open("bookcreator/book1.txt", "w") as f:
                    for word in text:
                        f.write(word + "\n")
                print("text formatted")
                return text
            except Exception as e:
                print(f"Error reading file: {str(e)}")
                traceback.print_exc()
        else:
            raise ValueError("Invalid genre, tone, or title")
        
    def section_similarity_check(self, current_section):
        """
        Checks for similarity between sections
        """
        nlp = spacy.load("en_core_web_md")
        doc1 = nlp(current_section)
        if len(self.sections) == 0:
            return False
        for section in self.sections:
            doc2 = nlp(section)
            if doc1.similarity(doc2) > 0.9:
                return True
        return False

    def remove_conclusion(self, subchapter):
    # Find the index of the substring "Conclusion"
        text = subchapter
        index = text.find("Conclusion")

        # If the substring is found, find the index of the next paragraph
        if index != -1:
            next_index = text.find("\n\n", index)

            # If the next paragraph is found, remove the range of text between the indices
            if next_index != -1:
                text = text[:index] + text[next_index:]
            # If the next paragraph is not found, remove everything after the "Conclusion" paragraph
            else:
                text = text[:index]

        # Return the modified text
        return text



    
b1 = BookGenerator("Self-help", "Inspiring", "Getting Over Depression", "to help people get over depression", "young adults")
#b1 = BookGenerator("Food and Cooking", "Informative", "The Art of cooking Intercontinental", "to teach people how to cook", "young adults")
#b1 = BookGenerator("Religion and spirituality", "Informative", "How to live in peace", "to help people live in peace with others", "everyone")
#print(b2.format_text())
#b1 = BookGenerator("Self-help", "Inspiring", "Overcoming Addiction", "to help people overcome masturbation and pornography addiction", "young adults")
#print(type(b1.load_json("generate chapters", "The Art of Cooking", "Introduction", "Introduction")))
print("====================================")
print(b1.generate_book())
#print(b1.generate_chapters())
print("===================================")
#print(b1.parse_book())
#print(b1.split_chapters())
#print(b1.generate_chapters())
#print(b1.test())