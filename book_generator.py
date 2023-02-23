import os
import openai

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


chapters = []
openai.api_key = "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"
chapters_response = openai.Completion.create(
        model="text-davinci-003",
        prompt="write me a song",
        max_tokens= 3000,
        temperature=0.7
)



print(chapters_response["choices"][0]["text"].strip())
