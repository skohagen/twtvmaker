import subprocess
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
import csv
import time
import twitch

## setting up selenium
options = Options()
options.headless = True

twitch.do_it() #executing api call from twitch.py, this creates the CSV file used for the rest

ffmpegfile = open('ffmpegvideo.txt', 'w') #create the txt file for ffmpeg to read and combine videos


with open('clipdata.csv', 'r') as csv_file: #get CSV file as source of twitch clips
        csv_reader = csv.reader(csv_file)
        #iterates over each line in csv
        for line in csv_reader:
                url = line[0]
                driver = webdriver.Chrome(options=options)
                driver.get(url) #open browser with url from csv
                time.sleep(5) #other ways of pausing selenium was not working for me, so we manually sleep
                html = driver.execute_script('return document.documentElement.outerHTML') #get html from link
                driver.close() #close browser
                soup = BeautifulSoup(html, 'lxml') #use Beautiful Soup and lmxl to read data
                vurl = soup.find("video").get("src") #find the video and get the src
                r = requests.get(vurl) #get url to download video below
                filename = str(vurl).split('/')[3] #get filename
                print(filename) #console.log filename
                #download video
                with open(filename, 'wb')as out_file:
                        out_file.write(r.content)

                ffmpegfile.write("file '"+filename+"'\n")
                #Skylar attempting to fix the issue with different video output encoding. Didn't work :/
                #time.sleep(15)
                #print('ffmpeg -i ' + filename + ' -c:v libx264 -crf 18 -preset slow -c:a copy en_' + filename)
                #subprocess.call('ffmpeg -i ' + filename + ' -c:v libx264 -crf 18 -preset slow -c:a copy en_' + filename)
                print('Video download complete')
ffmpegfile.close()
#call ffmpeg to read the txt file created and combine all the videos
subprocess.call('ffmpeg -f concat -safe 0 -auto_convert 1 -i ffmpegvideo.txt -c copy output.mp4', shell="True");