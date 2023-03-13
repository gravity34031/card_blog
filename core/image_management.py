from django.conf import settings
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import random
import os

#
import time


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

        img = Image.new("RGB", (W, H), fill_color)
        #font = ImageFont.truetype("arial.ttf", size=100)
        #font = ImageFont.truetype("/usr/local/share/fonts/arial.ttf", size=100)
        font = ImageFont.truetype(settings.FONT_PATH + "arial.ttf", size=100)

        draw = ImageDraw.Draw(img)

        draw.text((W / 2, H / 2), msg, font=font, anchor='mm', fill=font_color)
        now = datetime.now()
        time = str(now).replace(' ', '').replace(':', '')
        file_name = msg + '-' + time + '.webp'
        path = file_name

        img.save(path)
        return path


def delete_avatar(path, file):
    file.close()
    try:
        #print(path)
        os.remove(path)
    except:
        return ('Неизвестная ошибка при удалении аватара')



def compress_image(img, img_path, new_img_path):
    #start_time = time.time()
    def change_image_quality(img, img_path, quality):
        img.save(img_path, quality=quality)

    # check alpha
    img_size = os.path.getsize(img_path) / 1024
    if img_size > 100:
        img = img.convert('RGB')
    if img.mode == 'RGBA':
        img.save(new_img_path, 'webp', lossless=True)

    else:
        w = img.width
        h = img.height
        reduction_coeff = (round(max(w, h) / 100) / 10)
        if reduction_coeff > 1.1:
            new_w = round(w / reduction_coeff)
            new_h = round(h / reduction_coeff)
            img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
        img.save(new_img_path)
    
        img_size = os.path.getsize(new_img_path) / 1024
        quality = 100
        if img_size > 150:
            quality = 25
        if img_size > 100:
            quality = 30
        elif img_size > 70:
            quality = 45
        elif img_size > 50:
            quality = 55
        elif img_size > 25:
            quality = 70

        if quality < 100:
            change_image_quality(img, new_img_path, quality)
            img_size = os.path.getsize(new_img_path) / 1024
            quality = max(10, quality - 15)

        cycle = 1
        while img_size > 50 and cycle <= 3:
            change_image_quality(img, new_img_path, quality)
    
            quality = max(10, quality - 30)
            img_size = os.path.getsize(new_img_path) / 1024
            cycle += 1


    #print("--- %s seconds ---" % (time.time() - start_time))