import pandas as pd
df=pd.read_csv("liveChatData.csv")

df.describe()

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

from langdetect import detect

