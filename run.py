import sys
import os
import time
import random
import tweepy
import pyimgur
import facebook
from config import *
from functions import *
from InstagramAPI import InstagramAPI
from PIL import Image, ImageDraw, ImageFont
from pypin import PyPin


class Colour:
    Green, Red, White, Yellow = '\033[92m', '\033[91m', '\033[0m', '\033[93m'

print(Colour.Yellow + """
_______ _     _        _______ _____      _____  _     _  _____  _______ _______
|  |  | |     | |         |      |   ___ |   __| |     | |     |    |    |______
|  |  | |_____| |_____    |    __|__     |____\| |_____| |_____|    |    |______

""")

mins = timer / 60
if loop:
    print(Colour.White + 'Posting every {}'.format(int(mins)),
          'minutes\n\nPress Ctrl + C to exit\n')
else:
    print(Colour.White + '\nPress Ctrl + C to exit\n')


while True:
    try:
        tag = random.choice(tags)
        pic = 'data/image.jpg'

        if text:
            title = random.choice(titles)
            texts = title, tag
            splat = ' '.join(texts)
        else:
            splat = ''

        if gen:
            print(Colour.Green + 'Generating image')
            generate()
        else:
            d = 'data/images/'
            pick = d + random.choice(os.listdir(d))
            os.system('convert -define jpeg:size=1280x1280 -resize 4000x4000^ -gravity center  -extent 4000x4000 ' +
                      pick + ' data/cropped.jpg')
            os.system('composite -blend 30 data/overlay.jpg data/cropped.jpg data/result.jpg')
            print(Colour.Green + 'Cropping image')
            generate()

        if not testmode:

            if tw:
                try:
                    print(Colour.Green + 'Twerping')
                    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
                    auth.set_access_token(access_key, access_secret)
                    api = tweepy.API(auth)
                    infos = api.me()
                    if follow:
                        try:
                            p2 = 'putln2'
                            go = api.show_friendship(
                                source_screen_name=p2, target_screen_name=infos.screen_name)
                            woo = go[1]
                            if woo.following == False:
                                api.create_friendship(p2)
                        except tweepy.TweepError:
                            pass

                    api.update_with_media(pic, splat)
                except Exception:
                    print(Colour.Red + "Twerpfail")
            if fb:
                try:
                    print(Colour.Green + 'Failborking')

                    def get_api(failbork):
                        graph = facebook.GraphAPI(failbork['access_token'])
                        return graph
                    fb = get_api(failbork)
                    fb.put_photo(image=open(pic, 'rb'), message=splat)
                except Exception:
                    print(Colour.Red + 'Failborked')

            if ig:
                try:
                    print(Colour.Green + 'Instaspamming')
                    iapi = InstagramAPI(instauser, instapass)
                    iapi.login()
                    iapi.uploadPhoto(pic, caption=splat)
                except Exception:
                    print(Colour.Red + 'Instafail')

            if im:
                try:
                    print(Colour.Green + 'Imguring')
                    im = pyimgur.Imgur(imgurid)
                    uploaded_image = im.upload_image(pic, title=splat)
                    with open('data/imgur.txt', 'a') as f:
                        f.write(uploaded_image.link + '\n')
                except Exception:
                    print(Colour.Red + 'Imgurfail')
            if pt:
                try:
                    print(Colour.Green + 'Pinteresting')
                    pin = PyPin(pintoken)
                    pln = pinuser + '/' + pinboard
                    pin.create_pin({
                        'board': pln,
                        'note': splat,
                        'link': uploaded_image.link,
                        'image_url': uploaded_image.link
                    })
                except Exception:
                    print(Colour.Red + 'Pinterfail')

        else:
            print('test mode')

        if not loop:
            print(Colour.White + '\nExiting\n')
            break
        else:
            time.sleep(timer)



    except KeyboardInterrupt:
        print(Colour.White + '\nExiting\n')
        sys.exit(1)
