import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import json
import time
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import re
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
import io
from PIL import Image, ImageChops
import os


browser = webdriver.Firefox()

input_place = 'foggia'    #insert the name of the place you want to search

link = 'https://www.google.com/maps/place/'+input_place
browser.get(link)

def find_n_click(path):
    try:
        element = browser.find_element(By.CSS_SELECTOR, path)
        element.click()
        time.sleep(1.5)
    except:
        print('error')
        pass

find_n_click(".VtwTSb > form:nth-child(1) > div:nth-child(1) > div:nth-child(1) > button:nth-child(1)")
find_n_click(".vF7Cdb")   
find_n_click("div.KNfEk:nth-child(1) > button:nth-child(1) > span:nth-child(1)")

divSideBar=browser.find_element(By.CSS_SELECTOR,"div.DxyBCb:nth-child(1)")
while True:
    divSideBar.send_keys(Keys.PAGE_DOWN) 
    time.sleep(0.5)
    
    if browser.find_elements(By.CSS_SELECTOR, ".HlvSq"):
        break


i = 3  # Initial value of i
count = 0  # Initialize the count
while True:
    selector = f"div.DxyBCb:nth-child(1) > div:nth-child({i}) > div:nth-child(1) > a:nth-child(1)"
    
    # Check if an element with the selector exists
    if browser.find_elements(By.CSS_SELECTOR, selector):
        count += 1
        i += 2  # Increment i by 2 for the next iteration
    else:
        break

print(f"Total elements found: {count}")

def get_element_text(elem, selector):
    try:
        element = elem.find_element(By.CSS_SELECTOR, selector)
        return element.text
    except:
        return None


all = []
for i in range(3,3+(count*2),2):
    #print("starting:  " first element/second, ....)

    print(f"--- starting element: {int(((i+1)/2)-1)}/{count} ----")

    link_page = "div.DxyBCb:nth-child(1) > div:nth-child("+str(i)+") > div:nth-child(1)"
    find_n_click(link_page)
    elems = browser.find_elements(By.XPATH, "/html/body/div[3]/div[8]/div[9]/div/div/div[1]/div[3]/div/div[1]/div/div")
    
    for elem in elems:
        name = get_element_text(elem, ".DUwDvf")
        type_food = get_element_text(elem, ".DkEaL")
        rating = get_element_text(elem, ".F7nice > span:nth-child(1) > span:nth-child(1)")
        quant_review = get_element_text(elem, ".F7nice > span:nth-child(2) > span:nth-child(1) > span:nth-child(1)")

        try:
            total_num = quant_review.replace("(","")
            total_num = total_num.replace(")","")
            if '.' in str(total_num):
                total_num = total_num.replace(".","")
                total_num = int(total_num)
            else:
                total_num = int(total_num)
        except:
            total_num = None

        expensiveness = get_element_text(elem, ".mgr77e > span:nth-child(1) > span:nth-child(2) > span:nth-child(1) > span:nth-child(1)")
        address = get_element_text(elem, "div.RcCsl:nth-child(3) > button:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1)")
        site = get_element_text(elem, ".ITvuef > div:nth-child(1)")


        phone = None
        for k in range(6, 10):
            phone = get_element_text(elem, f"div.RcCsl:nth-child({k}) > button:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1)")
            if phone:
                break
        print(name)
        print("> general info completed")

        # Scraping the reviews
        find_n_click("button.hh2c6:nth-child(2) > div:nth-child(2) > div:nth-child(2)")

        try:
            divSideBar=browser.find_element(By.CSS_SELECTOR,"div.m6QErb:nth-child(3)")

            # Scroll as many times as necessary to load all reviews
            if total_num is not None:
                
                for j in range(0,(round(total_num/70))):
                    divSideBar.send_keys(Keys.PAGE_DOWN)
                    time.sleep(0.4)
            else:
                total_num = 100
                for j in range(0,(round(total_num/70))):
                    divSideBar.send_keys(Keys.PAGE_DOWN)
                    time.sleep(0.4)
            
            more_buttons = browser.find_elements(By.XPATH, "//button[contains(text(), 'Altro')]")
            for button in more_buttons:
                browser.execute_script("arguments[0].click();", button)

            response = BeautifulSoup(browser.page_source, 'html.parser')
            reviews = response.find_all('div', class_='GHT2ce')
            time.sleep(1)

            rev_dict = {'Review Rate': [],
            'Review Time': [],
            'Review Text' : []}

            for result in reviews:
                review_rate_element = result.find('span', class_='kvMYJc')
                try:

                    review_rate = review_rate_element.get("aria-label")
                except:
                    review_rate = 'empty'
                
                review_time_element = result.find('span', class_='rsqaWe')
                try:
                    review_time = review_time_element.text
                except:
                    review_time = 'empty'
                
                review_text_element = result.find('span', class_='wiI7pd')
                try:
                    review_text = review_text_element.text
                except:
                    review_text = 'empty'
                
                if review_rate != 'empty':
                    rev_dict['Review Rate'].append(review_rate)
                
                if review_time != 'empty':
                    rev_dict['Review Time'].append(review_time)

                if review_text != 'empty':
                    rev_dict['Review Text'].append(review_text)
            print("> reviews completed")
        except:
            print("> reviews not found")
            rev_dict = None

        all.append({
            'name': name,
            'type_food': type_food,
            'rating': rating,
            'quant_review': quant_review,
            'expensiveness': expensiveness,
            'address': address,
            'site': site,
            'phone': phone,
            'reviews': 'prova'
        })
        print(f"--- element: {int(((i+1)/2)-1)} completed ----")
print(all)

with open('data.json', 'w') as outfile:
    json.dump(all, outfile)

browser.quit()
