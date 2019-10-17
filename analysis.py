import pandas as pd
from plotly import express as px
from plotly import graph_objects as go
import plotly
df=pd.read_csv("cleanData.csv")

df=df.drop(['Unnamed: 21','Unnamed: 22'],axis=1)
df.columns

len(df)
df.drop_duplicates()
df["duration"]

cd=df[['Country','viewCount', 'likeCount', 'dislikeCount',
         'commentCount','categoryId']]
#cd[['viewCount', 
#    'likeCount', 
#    'dislikeCount',
#    'commentCount']]=cd[['viewCount', 
#                        'likeCount', 
#                        'dislikeCount',
#                        'commentCount']].apply(pd.to_numeric)

cd.describe()



corrMap=cd[['viewCount', 'likeCount', 'dislikeCount','commentCount']].corr()
corrMap.as_matrix()

fig = go.Figure(data=go.Heatmap(
                   z=corrMap.as_matrix(),
                   x=corrMap.index,
                   y=corrMap.index))
fig.show()

df['channelTitle'].value_counts()

countries=cd["Country"].unique()

testdf=cd[cd["Country"]=="Algeria "]

cd.columns
import statistics

statistics.mean(testdf["viewCount"])

mDf=pd.DataFrame(columns=["Country","Views","Likes","Dislikes","Comments"])
for i in countries:
    testdf=cd[cd["Country"]==i]
    testdf=testdf.dropna(axis=0, how='any', thresh=None, subset=None, inplace=False)
    views=statistics.mean(testdf["viewCount"])
    likes=statistics.mean(testdf["likeCount"])
    dislikes=statistics.mean(testdf["dislikeCount"])
    comments=statistics.mean(testdf["commentCount"])
    mDf=mDf.append({
        "Country":i.strip(),
        "Views":views,
        "Likes":likes,
        "Dislikes":dislikes,
        "Comments":comments
    },ignore_index=True)
import numpy as np
mDf["log_Views"]=np.log(mDf["Views"])
fig = go.Figure(data=go.Choropleth(
    locations=mDf["Country"], # Spatial coordinates
    z = mDf["Comments"].astype(float), # Data to be color-coded
    locationmode = 'country names', # set of locations match entries in `locations`
    colorscale = 'purples',
    colorbar_title = "Average Comments",
))
fig.show()

fig2=px.scatter_3d(mDf,x="Likes",
                        y="Dislikes",
                        z="Comments",
                        color="Country",
                        size="Views"
    )

plotly.offline.plot(fig2, filename='3d plot.html')


