from selenium import webdriver
import pandas as pd
import requests 
from bs4 import BeautifulSoup
import csv
import re
from datetime import datetime
import typer
import datefinder
from facebook_scraper import get_posts

app = typer.Typer()

head = ["Item Name","MIN price (Rs.)", "MAX price (Rs.)"]
item_list = []

search_list = []
element_in_lists = []

@app.command()
def thbuththegama_DEC_prices():
    URL = "https://www.thambuttegamadec.com/app/public/"
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find(id="nav-home-all")
    item_elements = results.find_all("div", class_="top")

    for item_element  in item_elements:
        min = ""
        max = ""

        # get data using html elements
        title_element = item_element.find("h5", class_="title")
        price_element = item_element.find("a", class_="button")

        title_e= title_element.text.strip()
        price_e = price_element.text.strip()

        # select only english letters 
        title = re.sub("[^A-Za-z]", "", title_e.strip())

        # replace word
        price = price_e.replace('අද මිලරු:', '');

        # String check  
        string_check= re.compile('-') 

        #separate min max prices
        if(string_check.search(price) == None): 
            min = price   
        else: 
            min = price.split("-",1)[0]
            max = price.split("-",1)[1] 

        val = [title, min, max]

        #add item to the list
        item_list.append(val)
        
        name = datetime.today().strftime('%Y-%m-%d')
        with open(name+' thabuththegama-full.csv', 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)

            # write the header
            writer.writerow(head)

            # write multiple rows
            writer.writerows(item_list)
    
    print("Full thabuththegama price list creation complete")

@app.command()
def dambulla_DEC_prices():
    listposts = []
    for post in get_posts("දඹුල්ල-විශේෂිත-ආර්ථික-මධ්යස්ථානය-Dambulla-Dedicated-Economic-Centre-113256350388269", pages=1):
        listposts.append(post)
    
    releventpost=[]
    releventpost = listposts[0]
    
    releventpost=releventpost["text"].replace('දඹුල්ල විශේෂිත ආර්ථික මධ්\u200dයස්ථානය\n\nදෛනික මිල තොරතුරු තොග මිල ( Rs/1 Kg)\n\n', '').replace('(දඹුල්ල විශේෂිත ආර්ථික මධ්\u200dයස්ථාන\nකළමනාකරණ භාරය විසින් නිකුත් කරන මිල ගණන්)\n\n', '')
    items=releventpost.split(sep='\n\n')
    
    dates_in_string = []
    matches = datefinder.find_dates(items[0])
    for match in matches:
        dates_in_string.append(match)

    date = dates_in_string[0]
    date = date.strftime('%Y-%m-%d')
    del items[0]
    
    for item in items:
        price = []
        names =[]
        patterns= [r'\D+']

        for p in patterns:
            match= re.findall(p, item)
            name=match[0].unicode('utf8')
            
        numbers = re.findall(r'\d+', item)
        r=len(numbers)

        #separate min max prices
        if(r==0):
            min = '-'
            max = '-'

        elif(r == 2): 
            min = numbers[0]
            max = numbers[1] 
        else: 
            min = numbers[0]
            max = '-'


        val = [name,min,max]

        item_list.append(val)

    with open(date+'Dambulla-dec-prices'+'.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)

        # write the header
        writer.writerow(head)

        # write multiple rows
        writer.writerows(item_list)
    
    print("Full Dambulla price list creation complete")

@app.command()
def text_to_list(filename : str,funname : str):
    
    if(funname == "thabuththegama"):
        functionRun = thbuththegama_DEC_prices()
    elif (funname == "dabulla"):
        functionRun = dambulla_DEC_prices()
    else:
        print("invalied function")

    new_list =[]
    
    # open item list text file as a list
    with open(filename+".txt", "r") as i_list:
        new_list = i_list.readlines()
     
    # remove \n from list
    for item in new_list:
        new = item.replace("\n", "") 
        search_list.append(new)
        
    # Search in item_list 
    for i in search_list:
        for list in item_list:
            if i in list:
               element_in_lists.append(list)
    

    Today = datetime.today().strftime('%Y-%m-%d')
    # create csv and write data
    with open(Today+funname+"-"+filename+'-items-price.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        
        #write Headers
        writer.writerow(head)
        
        # write multiple rows
        writer.writerows(element_in_lists)
    
    print(filename + " named Custom price list has been created ...")

if __name__ == "__main__":
    app()