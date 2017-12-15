from PIL import Image, ImageDraw, ImageFont
import textwrap
import json
import random
import os


def generate():
    dir = os.path.dirname(__file__)
    mg = MaterialGenerator()
    qg = QuoteGenerator()
    quote = qg.get_quote()
    image = mg.draw_image(quote['quoteText'], quote[
                          'quoteAuthor'], (4000, 4000))
    image.save(os.path.join(dir, 'data/image.jpg'), 'JPEG')


def get_random_color():
    dir = os.path.dirname(__file__)
    colors = json.load(open(os.path.join(dir, 'data/material-colors.json')))
    color = random.choice(list(colors.keys()))
    return colors[color]['500']


class MaterialGenerator:

    def draw_image(self, text, author, size):
        COPYRIGHT_TEXT = "@PUTlN2"
        dir = os.path.dirname(__file__)
        im = Image.new('RGB', size)
        draw = ImageDraw.Draw(im)
        draw.rectangle(((0, 0), size), fill=get_random_color())
        font = ImageFont.truetype(os.path.join(
            dir, 'fonts/DeFonarts-Bold.otf'), 280)
        lines = textwrap.wrap(text, 20)
        #if author != "":
        #    lines.append(' ')
        #    lines.append('- ' + author)
        line_dimensions = [draw.textsize(line, font=font) for line in lines]
        offset = (size[1] - sum(h for w, h in line_dimensions)) // 2
        for line in lines:
            w, h = draw.textsize(line, font=font)
            pos = ((size[0] - w) / 2, offset)
            draw.text(pos, line, font=font, fill=(255, 255, 255))
            offset += font.getsize(line)[1]
        del draw
        return im


class QuoteGenerator:

    def get_quote(self):
        dir = os.path.dirname(__file__)
        quotes = self.filter_quotes(json.load(
            open(os.path.join(dir, 'data/quotes.json'), encoding='latin1')), 150, 15)
        quote = random.choice(quotes)
        return quote

    def filter_quotes(self, quotes, lenQ, lenA):
        _quotes = []
        for quote in quotes:
            lQ = quote['quoteText'].__len__()
            lA = quote['quoteAuthor'].__len__()
            if lQ <= lenQ and lA <= lenA:
                _quotes.append(quote)
        return _quotes
