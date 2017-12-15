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
            try:
                d = 'data/images/'
                pic = d + random.choice(os.listdir(d))
            except Exception:
                print(Colour.Red + 'No images')
                yes = set(['YES', 'yes', 'y', 'Y'])
                no = set(['NO', 'no', 'n', 'N'])
                choice = input(Colour.White + 'Use test image? Y/n ')
                if choice in no:
                    print(Colour.White + '\nExiting\n')
                    sys.exit(1)
                elif choice in yes:
                    testimg = 1
                    pic = 'data/test.jpg'

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
            if not gen:
                try:
                    os.remove(pic)
                except Exception:
                    print(Colour.Red + 'No images')
                    yes = set(['YES', 'yes', 'y', 'Y'])
                    no = set(['NO', 'no', 'n', 'N'])
                    choice = input(Colour.White + 'Use test image? Y/n ')
                    if choice in no:
                        print(Colour.White + '\nExiting\n')
                        sys.exit(1)
                    elif choice in yes:
                        testimg = 1
                        pic = 'data/test.jpg'

        else:
            print('test mode')

        if not loop:
            break
        else:
            time.sleep(timer)

    except KeyboardInterrupt:
        print(Colour.White + '\nExiting\n')
        sys.exit(1)
