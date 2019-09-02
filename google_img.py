import requests
from bs4 import BeautifulSoup
import re
import numpy as np
import pandas as pd
import time
from selenium import webdriver
from tqdm import tqdm, tqdm_notebook
from selenium.webdriver.chrome.options import Options
import os
import html
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import os

chrome_options = Options()
chrome_options.add_argument("--headless")       # define headless
chrome_options.add_argument("--window-size=1000,800")
browser = webdriver.Chrome(options=chrome_options)

files = os.listdir('word')
files.remove('Blank.csv')
exist = os.listdir('img')
exist = [e + '.csv' for e in exist]
remainder = list(set(files) - set(exist))

for file in tqdm_notebook(remainder, total=len(remainder)):
    items = pd.read_csv('word/' + file, header=None).T.values[0]
    print ('Now running %s'%(file))
    category = file.split('.')[0]
    dirName = 'img/'+category
    # Create target Directory if don't exist
    if not os.path.exists(dirName):
        os.mkdir(dirName)
        os.mkdir(dirName+'/%s_test'%(category))
        print("Directory " , dirName ,  " Created ")
    else:    
        print("Directory " , dirName ,  " already exists")
    
    for item in tqdm_notebook(items, total=len(items)):
        item_len = len(item)
        url = 'https://www.google.com/search?biw=1164&bih=801&tbm=isch&sa=1&ei=WJZOXe35GsyWr7wPp8-d-Ao&q=%s&oq=%s\
        &gs_l=img.3..35i39j0l9.5946968.5948390..5948893...0.0..0.130.345.1j2......0....1..gws-wiz-img.....0.62GBiwmruak&ved=0ahUKEwjthdyshvjjAhVMy4sBHadnB68Q4dUDCAY&uact=5'%(item, item)
        browser.get(url)
        png = browser.get_screenshot_as_png()
        im = Image.open(BytesIO(png))
        rgb_im = im.convert('RGB')
        rgb_im.save('img/%s/%s_test/%s.jpeg'%(category, category, item))
        drawAvatar   = ImageDraw.Draw(rgb_im)
        xSize, ySize = rgb_im.size
        fontSize     = 100 if item_len<=15 else int(1500/(item_len))
        myFont       = ImageFont.truetype("arial.ttf", fontSize)
        drawAvatar.text([max(0, 0.5 * xSize - (item_len)*20), 0.11 * ySize],\
        item, fill = (255, 0, 0), font = myFont)
        del drawAvatar
        
        rgb_im.save('img/%s/%s.jpeg'%(category, item))
        time.sleep(1)
        #im.show()
browser.close()