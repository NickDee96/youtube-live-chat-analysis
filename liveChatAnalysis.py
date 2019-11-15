import pandas as pd
import numpy as np
df=pd.read_csv("liveChatData.csv")
minDf=df[df.Timestamp.str.contains("-")==False].reset_index(drop=True)
minDf.Timestamp.to_timestamp()
df.Timestamp.value_counts()

minDf.columns
from datetime import datetime

times=[]
for i in range(len(minDf["Timestamp"])):
    tsmp=minDf["Timestamp"][i]
    if (len(tsmp)==4) or (len(tsmp)==5):
        struct_time = datetime.strptime(tsmp, "%M:%S").time()
    elif len(tsmp)==7:
        struct_time = datetime.strptime(tsmp, "%H:%M:%S").time()
    times.append(struct_time)
    print(struct_time)


len(times)
len(minDf["Timestamp"])
minDf=minDf.drop(["Timestamp"],axis=1)  
minDf["Timestamp"]=times


from textblob import TextBlob
polarity=[]
num=0
for i in minDf.Message:
    try:
        blob = TextBlob(i)
        ply=blob.sentiment.polarity
        polarity.append(ply)
    except TypeError:
        polarity.append(np.nan)
    num=num+1
    print(num)

minDf["Polarity"]=polarity
minDf.columns


minDf.dtypes

minDf.to_csv("mindf.csv",index=False)

###
#minDf=pd.read_csv("mindf.csv")

minDf.describe()




minDf=minDf.fillna("")
from sklearn.feature_extraction.text import TfidfVectorizer
vectorizer = TfidfVectorizer(max_features=20,stop_words="english",ngram_range=(1,2))
vectorizer.fit_transform(minDf["Message"])

vectorizer.get_feature_names()



## Top 50 Most active users
top=df.Author.value_counts().head(50)

a=df[df.Author=="trevor wasike"].reset_index(drop=True)["Message"]

from sklearn.feature_extraction.text import TfidfVectorizer

vectorizer = TfidfVectorizer(max_features=20,stop_words="english")
X = vectorizer.fit_transform(a)
print(vectorizer.get_feature_names())


from textblob import TextBlob
from textblob.exceptions import TranslatorError

t1=TextBlob(a[1])

t1.detect_language()

t1.translate(to="en")



##plotting post data
s=pd.to_datetime(minDf.Timestamp)
minDf.Timestamp.strftime("%H:%M")

ts=[x.strftime("%H:%M") for x in minDf.Timestamp]
uData=pd.DataFrame()
uData["Timestamp"]=ts
u=uData["Timestamp"].value_counts().to_frame().reset_index()
u.columns=["Timestamp","Posts"]
u=u.sort_values("Timestamp").reset_index(drop=True)

pData=minDf.Timestamp.value_counts().to_frame().reset_index()
pData.columns=["Timestamp","Posts"]
pData=pData.sort_values("Timestamp").reset_index(drop=True)


import plotly.graph_objects as go

fig = go.Figure()
fig.add_trace(
    go.Scatter(
        x=u.Timestamp,
        y=u.Posts
    )
)
fig.add_trace(
    go.Scatter(
        x=["01:02","03:01"],
        y=[max(u.Posts),max(u.Posts)],
        text=[
            "Start of the Race",
            "End of the Race"
        ],
        mode="text"
    )
)
fig.add_shape(
        # start of the race
        go.layout.Shape(
            type="line",
            x0="01:02",
            y0=min(u.Posts),
            x1="01:02",
            y1=max(u.Posts),
            line=dict(
                color="LightSeaGreen",
                width=4,
                dash="dashdot",
            )
))
fig.add_shape(
        # start of the race
        go.layout.Shape(
            type="line",
            x0="03:01",
            y0=min(u.Posts),
            x1="03:01",
            y1=max(u.Posts),
            line=dict(
                color="LightSeaGreen",
                width=4,
                dash="dashdot",
            )
))
fig.update_layout(title_text='Time Series with Rangeslider',
                  xaxis_rangeslider_visible=True)
fig.show()
