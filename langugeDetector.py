from textblob import TextBlob
from textblob.exceptions import TranslatorError
import numpy as np
import pandas as pd
df=pd.read_csv("liveChatData.csv")
language=[]
msgs=df.Message

for i in range(len(msgs)):
    try:
        t1=TextBlob(msgs[i])
        lan=t1.detect_language()
        language.append(lan)
    except (TypeError,TranslatorError):
        lan=np.nan
        language.append(lan)
        print("Translator Error")
    print(i)

df["Language"]=language
df.to_csv("langDf.csv")
