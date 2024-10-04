import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import os
from dotenv import find_dotenv,load_dotenv

dotenv_path=find_dotenv()
load_dotenv(dotenv_path)

URL=os.getenv("url")
GOOGLE_SHEET_LINK=os.getenv("google_sheet_link")
PATH1=os.getenv("ans1_value")
PATH2=os.getenv("ans2_value")
PATH3=os.getenv("ans3_value")
PATH4=os.getenv("submit_value")
PATH5=os.getenv("sheet_value")
PATH6=os.getenv("element_clickable")

response=requests.get(URL)
con=response.text

cone=webdriver.ChromeOptions()
cone.add_experimental_option("detach" ,True)
class Housing():

    #Creating lists to store different listings
    def __init__(self):
        self.links=[]
        self.prices=[]
        self.address=[]
        self.soup=BeautifulSoup(con,"html.parser")
        self.listings=self.soup.find_all(name="ul" , class_="List-c11n-8-84-3-photo-cards")
        self.sheet_link=GOOGLE_SHEET_LINK
        self.driver=webdriver.Chrome(cone)

    #Fetchs the link of the listing
    def link(self):
        presence=set()
        for tag in self.soup.select(selector=".List-c11n-8-84-3-photo-cards li a"):
            b=tag.get("href")
            if b in presence:
                continue
            else:
                presence.add(b)
                self.links.append(b)
    #Fetchs the price of the Listing
    def price(self):
        for t in self.soup.find_all(class_="PropertyCardWrapper"):
            pri=t.text.strip()
            if "/" in pri:
                pri=pri.split("/")[0]
            if "+" in pri:
                pri=pri.split("+")[0]
            self.prices.append(pri)

    #Gets the address of the listing
    def addre(self):
        for h in self.soup.find_all(name="address"):
            ad=h.text.strip()
            if "|" in ad:
                addr=ad.split("|")
                addr=addr[0]+addr[1]
            else:
                addr=ad
            if "  " in addr:
                addr=addr.split("  ")
                addr=f"{addr[0]} {addr[1]}"
            self.address.append(addr)

    #Fills the Google Form
    def filling(self):

        for i in range(len(self.prices)):
            self.driver.get(f"{self.sheet_link}")
            sleep(3)
            ans1=self.driver.find_element(By.XPATH,value=PATH1)
            ans1.send_keys(f"{self.address[i]}")
            sleep(1)
            ans2=self.driver.find_element(By.XPATH,value=PATH2)
            ans2.send_keys(f"{self.prices[i]}")
            sleep(1)
            ans3=self.driver.find_element(By.XPATH,value=PATH3)
            ans3.send_keys(f"{self.links[i]}")
            sleep(1)
            submit=self.driver.find_element(By.XPATH,value=PATH4)
            submit.click()

        sleep(2)
        self.driver.close()

rental=Housing()
rental.link()
rental.addre()
rental.price()
rental.filling()
