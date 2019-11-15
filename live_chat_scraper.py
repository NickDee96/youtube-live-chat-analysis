from bs4 import BeautifulSoup as soup
from selenium import webdriver
import os
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.select import Select
import selenium.webdriver.support.ui as ui
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import ElementClickInterceptedException
import csv


url="https://youtu.be/k-XgKRJUEgQ?t=6121"
driver=webdriver.Firefox(executable_path = 'geckodriver\\geckodriver.exe')
driver.get(url)
driver.switch_to.default_content()


a=driver.find_elements_by_tag_name("iframe")[1]
driver.switch_to.frame(a)

len(a)

with open("liveChatData.csv","a",newline="") as lFile:
    writer=csv.DictWriter(lFile,fieldnames=["Author","Message","Timestamp","Photo"])
    writer.writeheader()
    for j in range(1200):
        page=soup(driver.execute_script("return document.body.innerHTML"),"lxml")
        cContainers=page.find_all("yt-live-chat-text-message-renderer")
        for i in cContainers:
            author_photo=i.find_all("yt-img-shadow",{"id":"author-photo"})[0].img["src"]
            author_name=i.find_all("span",{"id":"author-name"})[0].text
            timestamp=i.find_all("span",{"id":"timestamp"})[0].text
            message=i.find_all("span",{"id":"message"})[0].text
            writer.writerow({
                "Author":author_name,
                "Message":message,
                "Timestamp":timestamp,
                "Photo":author_photo
            })
        time.sleep(5)
        print(str(j)+" is done")




with open("test.html","w") as tFile:
    tFile.write(str(page))



page.text
