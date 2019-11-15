from apiclient.discovery import build 
import pandas as pd
import requests as req
from bs4 import BeautifulSoup as soup
import random
import csv
import time
   
# Arguments that need to passed to the build function 
DEVELOPER_KEY = "" 
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
   
# creating Youtube Resource Object 
youtube_object = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, 
                                        developerKey = DEVELOPER_KEY) 
   
query="wamlambez"
max_results = 5  
       
# calling the search.list method to retrieve youtube search results 
search_location = youtube_object.search().list(q = query, type ='video', 
                                       location ='-1.300210, 36.775039', 
                          locationRadius ='100km', part = "id, snippet", 
                                      maxResults = max_results).execute() 
   
# extracting the results from search response 
results = search_location.get("items", []) 

# empty list to store video metadata 
videos = [] 
   
# extracting required info from each result object 
for result in results: 

    # video result object 
    videos.append(result["id"]["videoId"]) 
video_ids = ", ".join(videos) 
video_response = youtube_object.videos().list(id = video_ids, part ='snippet,recordingDetails').execute() 
       
search_videos = [] 
for video_result in video_response.get("items", []): 
    search_videos.append("% s, (% s, % s)" %(video_result["snippet"]["title"], 
                     video_result["recordingDetails"]["location"]["latitude"], 
                   video_result["recordingDetails"]["location"]["longitude"])) 

print ("Videos:\n", "\n".join(search_videos), "\n") 


b=youtube_object.search().list(type ='video', location ='-1.300210, 36.775039', 
                          locationRadius ='100km', part = "id, snippet", 
                                      maxResults = 50).execute() 


b["items"][0]["id"]["videoId"]


c=youtube_object.videos().list(id="M-TnBlnrSoc",part="id, snippet,statistics,contentDetails,recordingDetails").execute() 

d=youtube_object.videoCategories().list(id="1",part="id, snippet").execute()


with open("yt_cat.csv","w",newline="") as yfile:
    writer2=csv.DictWriter(yfile,fieldnames=['code','category'])
    writer2.writeheader()
    for i in range(1,44):
        d=youtube_object.videoCategories().list(id=str(i),part="id, snippet").execute()
        e=d["items"][0]["snippet"]['title']
        writer2.writerow({
            "code":i,
            "category":e
        })





headers=(
    {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'},
    {'user-agent':'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36'},
    {'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'},
    {'user-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36'},
    {'user-agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1'},
    {'user-agent':'Mozilla/5.0 (X11; U; Linux Core i7-4980HQ; de; rv:32.0; compatible; JobboerseBot; http://www.jobboerse.com/bot.htm) Gecko/20100101 Firefox/38.0'},
    {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0'},
    {'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:63.0) Gecko/20100101 Firefox/63.0'},
    {'user-agent':'Mozilla/5.0 (X11; od-database-crawler) Gecko/20100101 Firefox/52.0'},
    {'user-agent':'Mozilla/5.0 (X11; U; Linux i686; fr; rv:1.9.2.16) Gecko/20110323 Ubuntu/10.04 (lucid) Firefox/3.6.16'},
)



def getTrending(link):
    page=soup(req.get(link,).text,"lxml")
    titles=page.find_all("h3",{"class":"yt-lockup-title"})
    videoId=titles[0].a["href"].split("=")[1]
    ids=list()
    for i in titles:
        videoId=i.a["href"].split("=")[1]
        ids.append(videoId)
    return ids

def getWorldTrending():
    cCodes=pd.read_csv("codes.csv")
    tData=dict()
    for i in range(len(cCodes)):
        code=cCodes["Code"][i]
        country=cCodes["Country"][i]
        url="https://www.youtube.com/feed/trending?gl={}"
        vIds=getTrending(url.format(code))
        tData.update({
            country:vIds
        })
        print(country +" is done")
    return tData
cData=getWorldTrending()
import json
with open("worldTrending.json","w") as jfile:
    jfile.write(json.dumps(cData,indent=2))



fNames=['publishedAt',
 'channelId',
 'title',
 'description',
 'channelTitle',
 'categoryId',
 'liveBroadcastContent',
 'defaultAudioLanguage',
 'defaultLanguage',
 'viewCount',
 'likeCount',
 'dislikeCount',
 'favoriteCount',
 'commentCount',
 'duration',
 'dimension',
 'definition',
 'caption',
 'licensedContent',
 'projection',
 'Country']


with open("yData3.csv","a",newline="") as yfile:
    writer=csv.DictWriter(yfile,fieldnames=fNames)
    #writer.writeheader()
    for i in range(15,len(cData.keys())):
        vIds=cData[(list(cData.keys())[i])]
        for j in vIds:
            c=youtube_object.videos().list(id=j,part="id, snippet,statistics,contentDetails,recordingDetails").execute()
            upDict={}
            try:
                upDict.update(c["items"][0]["snippet"])
                upDict.update(c["items"][0]["statistics"])
                upDict.update(c["items"][0]["contentDetails"])
            except IndexError:
                pass
            upDict.update({"Country":list(cData.keys())[i]})
            ommit=['thumbnails','tags','localized','regionRestriction']
            for k in ommit:
                if k in list(upDict.keys()):
                    upDict.pop(k)
            writer.writerow(upDict)
            print(j)
            time.sleep(.2)
        print('''
        ______________

        {}
        _______________'''.format(list(cData.keys())[i]))



