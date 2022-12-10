import requests
from bs4 import BeautifulSoup
import os
import json
import random
import time
import threading
from winput import *
from yt_dlp import YoutubeDL

def lcm(a, b):
    if a > b:greater = a
    else:greater = b
    while(True):
        if((greater % a == 0) and (greater % b == 0)):
            lcm = greater
            break
        greater += 1
    return lcm

def run(i):
    reqs = requests.get(config["searchPornhubUrl"])
    soup = BeautifulSoup(reqs.text, 'html.parser')
    urls = []

    substring = "/view_video.php?viewkey=ph"
    for link in soup.find_all('a'):
        if substring in str(link.get('href')):
            (urls).append(link.get('href'))
    #print(urls)
    vid = random.choice(urls)
    for ih in lim:
        if vid == ih and config["dontPlaySameVidTwicePerCurrentRun"]:
            raise Exception("vid has been played already")
    lim.append(vid)
    streamurl = f"https://www.pornhub.com{vid}"

    print(streamurl)

    fifs = YoutubeDL().extract_info(streamurl, download=False)

    gias = fifs["resolution"].split("x")
    tuy = lcm(int(gias[0]), int(gias[1]))
    gias = f'{round(tuy / 1080)}:{round(tuy / 1920)}'

    if str(gias) != "16:9" and config["disableNon16:9Videos"] is False:
        raise Exception(f"not 16:9 but {gias}")


    #godshiz = fifs['formats'][4]['url']
    godshiz = streamurl
    if godshiz == None or fifs['duration'] < 10 or fifs['duration'] > config["maxSecondsVideoLength"]:
        raise Exception(f"video too long it is {fifs['duration']} and max {config['maxSecondsVideoLength']}")
    #print("m3u8 url = " + godshiz)
    with open(f'{str(dir[i])}\\livelyinfo.json', 'r+') as f:
        data = json.load(f)
        data['Contact'] = godshiz
        data['FileName'] = godshiz
        data['Type'] = 10
        data['Title'] = 'Pornhub monitor ' + str(i)
        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()

    print(f"Durations: {fifs['duration']} Resolution: {fifs['resolution']} Aspect Ratio: {gias} Title: {fifs['title']} URL: {streamurl} Monitor: {i}")
    dur[i] = (fifs['duration'])
    print(str(dur))
    fif.append(f"https://www.pornhub.com{vid}")

def d(x):
    while True:
        while True:
            try:
                run(x)
                break
            except Exception as e:
                print(f"error on video {x} with {e}")
        print(f"Sending video update command to lively on monitor {str(x)}")
        os.system(f'{config["Lively.exeLocation4"]} setwp --file "{dir[x]}" --monitor {x + 1}')
        print(f"Starting timer for monitor {str(x)}")
        time.sleep(dur[x])
        print(f"done waiting for monitor {str(x)}")


def fe():
    hook_keyboard(keyboard_callback)
    wait_messages()


def keyboard_callback(event):
    if config["keyboardDebugForInteger"]:
        print(str(event.vkCode))
    if str(event.vkCode).find(str(config["keybindToTurnOffInteger/NotASCII"])) != -1:
        os.system("taskkill /f /im mpv.exe")
        os.system("taskkill /f /im lively.exe")
        os._exit(0)


if __name__ == "__main__":
    with open("config.json") as f:
        config = json.load(f)
    nm = len(config["LocationOfLivelyWalpapers"])
    config["Lively.exeLocation4"] = config["Lively.exeLocation"].replace(" ", '" "')

    #os.startfile(config["Lively.exeLocation"])

    dir = []; fif = []; dur = {}; lim = []
    for i in config["LocationOfLivelyWalpapers"]: dir.append(i)
    print(dir)
    f = threading.Thread(target=fe, args=())
    f.start()


    with open('log.hub.txt', 'a') as f:
        f.write(f'{"".join(["-" for f in range(200)])}\n')
        for i in fif:
            f.write(f'[{time.ctime()}] : {i}\n')


        # creating thread
    for i in range(nm):
        t = threading.Thread(target=d, args=(i,))
        print(f'{i} threat created')
        t.start()

    # both threads completely executed
