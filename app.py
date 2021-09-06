# -*- coding: utf-8 -*-
import os, io, base64
from flask import Flask, request
from random import choice, sample
from requests import get, post
from PIL import Image, ImageFont, ImageDraw
from textwrap import wrap
from time import time, ctime

app = Flask(__name__)
os.chdir(os.path.dirname(os.path.abspath(__file__)))

cats = open('cats.txt', encoding = 'UTF-8').readlines()

putin_pic = get("https://raw.githubusercontent.com/AtTime-Agency/AtTime_Presents_bot/main/Photos/Putin.png")
merkel_pic = get("https://raw.githubusercontent.com/AtTime-Agency/AtTime_Presents_bot/main/Photos/AngelaMerkel.jpg")
biden_pic = get("https://raw.githubusercontent.com/AtTime-Agency/AtTime_Presents_bot/main/Photos/JoeBiden.jpg")
emomali_pic = get("https://raw.githubusercontent.com/AtTime-Agency/AtTime_Presents_bot/main/Photos/Emomali.jpg")
billy_pic = get("https://raw.githubusercontent.com/AtTime-Agency/AtTime_Presents_bot/main/Photos/Billy.jpg")
kli4ko_pic = get("https://raw.githubusercontent.com/AtTime-Agency/AtTime_Presents_bot/main/Photos/Kli4ko.jpg")
nursultan_pic = get("https://raw.githubusercontent.com/AtTime-Agency/AtTime_Presents_bot/main/Photos/Nursultan.jpg")
einstein_pic = get("https://raw.githubusercontent.com/AtTime-Agency/AtTime_Presents_bot/main/Photos/Einstein.jpg")
jakfresko_pic = get("https://raw.githubusercontent.com/AtTime-Agency/AtTime_Presents_bot/main/Photos/Jak.jpg")
durov_pic = get("https://raw.githubusercontent.com/AtTime-Agency/AtTime_Presents_bot/main/Photos/Durov.jpg")
putin_font = get("https://github.com/AtTime-Agency/AtTime_Presents_bot/raw/main/Fonts/MarckScript-Regular.ttf").content

args = {
    'putin': [putin_pic, 32, 1039, 241],
    'merkel': [merkel_pic, 250, 1039, 1000],
    'biden': [biden_pic, 250, 1039, 1000],
    'emomali': [emomali_pic, 250, 1039, 1000],
    'billy': [billy_pic, 250, 1039, 1000],
    'kli4ko': [kli4ko_pic, 250, 1039, 1000],
    'nursultan': [nursultan_pic, 250, 1039, 1000],
    'einstein': [einstein_pic, 250, 1039, 1000],
    'jakfresko': [jakfresko_pic, 250, 1039, 1000],
    'durov': [durov_pic, 250, 1039, 1000]
}

@app.route('/', methods=['GET'])
def main():
    return choice(cats)

@app.route('/<name>/<text>', methods=['GET'])
def putin(name, text):
    try:
        t = time()
        meme = make_meme(text, args[name])['pic']
        img = upload_pic(meme)
        return {'ok': True, 'url': img['imgbb']['data']['url'], 'time': f'{str(time() - t)[:5]} sec'}

    except Exception as e:
        return {'ok': False, 'error': repr(e)}

def upload_pic(pic):
    try:
        key_imgbb = '' # Your imgbb api key
        with open(pic, "rb") as file:
            url = "https://api.imgbb.com/1/upload"
            payload = {
                "key": key_imgbb,
                "image": base64.b64encode(file.read()),
            }
            res = post(url, payload)
        return {'ok': True, 'imgbb': res.json()}
    except Exception as e:
        return {'ok': False, 'exc': repr(e)}

def make_meme(capt, arg):

    try:

        pic = arg[0]
        f = putin_font
        txt = capt
        pic.raw.decode_content = True
        img = Image.open(io.BytesIO(pic.content)).convert("RGB")
        W, H = img.size
        text = "\n".join(wrap(txt, 19))
        t = text + "\n"
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype(io.BytesIO(f), arg[1], encoding = 'UTF-8')
        w, h = draw.multiline_textsize(t, font = font)
        imtext = Image.new("RGBA", (w + 10, h + 10), (0, 0, 0, 0))
        draw = ImageDraw.Draw(imtext)
        draw.multiline_text((10, 10), t, (0, 0, 0), font = font, align = 'center')
        imtext.thumbnail((arg[2], arg[3]))
        w, h = 339, 181
        img.paste(imtext, (10,10), imtext)
        fname = ''.join(sample([chr(i) for i in range(65, 91)]+[str(i) for i in range(10)], 10)) + '.jpg'
        with open(fname, 'w') as f:
            img.save(f)

        return {'ok': True, 'pic' : fname}

    except Exception as e:
        return {'ok': False, 'exc': repr(e)}

if __name__ == '__main__':
    app.run()
