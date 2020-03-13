import pickle
import random
from datetime import date
from PIL import Image, ImageDraw, ImageFont
from litlithelp_stanza import asonante, consonante
import os

from model.generator import GrammarSensitiveGenerator


def text_on_img(filename='01.png', text="Hello", size=12, color=(255, 255, 0), bg='red'):
    "Draw a text on an Image, saves it, show it"
    fnt = ImageFont.truetype('OpenSans-Regular.ttf', size)
    # create image
    image = Image.new(mode="RGB", size=(int(size) * len(text.split("\n")[0]) + 100, size + 200), color=bg)
    draw = ImageDraw.Draw(image)
    # draw text
    draw.text((10, 10), text, font=fnt, fill=color)
    # save file
    image.save(filename)


location = "Spanish/"
# Pick up the trained model
f = open(location + "model", 'rb')
spanish_model = pickle.load(f)
f.close()

# Get the grammar
f = open(location + "grammar", 'rb')
spanish_grammar = pickle.load(f)
f.close()

# Don't forget about the tokens
f = open(location + "tokenized", 'rb')
spanish_tokens = pickle.load(f)
f.close()

# Generate

generator = GrammarSensitiveGenerator(spanish_model, spanish_grammar, spanish_tokens)

syllables = random.randrange(6,14)
coin = random.randint(0,1)
text = ""
if coin == 0:
    text = asonante(syllables, generator)
else:
    text = consonante(syllables, generator)

filename = "Instagram/" +date.today().__str__() + ".png"
f = open(filename, "w")
f.close()
if text != -1:
    text_on_img(filename=filename, text=text, size=20, bg='white', color=(0, 0, 0))