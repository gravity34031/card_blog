from django.conf import settings
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import random
import os


COLORS = [
    ['#DF7FD7', '#DF7FD7', '#591854'],
    ['#E3CAC8', '#DF8A82', '#5E3A37'],
    ['#E6845E', '#E05118', '#61230B'],
    ['#E0B050', '#E6CB97', '#614C23'],
    ['#9878AD', '#492661', '#C59BE0'],
    ['#787BAD', '#141961', '#9B9FE0'],
    ['#78A2AD', '#104F61', '#9BD1E0'],
    ['#78AD8A', '#0A6129', '#9BE0B3'],
    ['#AD8621', '#6B5621', '#E0AD2B'],
]

def create_avatar(msg):
        msg = msg
        W, H = (150, 150)
        color = random.choice(COLORS)
        fill_color = color[0]
        font_color = color[2]

        img = Image.new("RGBA", (W, H), fill_color)
        font = ImageFont.truetype("arial.ttf", size=100)

        draw = ImageDraw.Draw(img)

        draw.text((W / 2, H / 2), msg, font=font, anchor='mm', fill=font_color)
        now = datetime.now()
        time = str(now).replace(' ', '').replace(':', '')
        file_name = msg + '-' + time + '.png'
        path = file_name

        img.save(path)
        return path


def delete_avatar(path, file):
    file.close()
    try:
        print(path)
        os.remove(path)
    except:
        return ('Неизвестная ошибка при удалении аватара')