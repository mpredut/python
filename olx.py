#!/usr/bin/python
# -*- coding: latin-1 -*-

import requests
from bs4 import BeautifulSoup

#data = {'An':"", 'Pret':"",'Descriere':""}
data = set()       
        
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
 
    
def only_numerics(seq):
    seq = seq.split(",")[0]
    seq_type = type(seq)
    return seq_type().join(filter(seq_type.isdigit, seq))
 
 

def parseurl(url, text): 
        
    response = requests.get(url)

    # Extragem con?inutul paginii web
    content = response.content
    # Analizam con?inutul folosind BeautifulSoup
    soup = BeautifulSoup(content, 'html.parser')

    ad_elements = soup.find_all('div', { 'data-cy': 'l-card'})

    find_items  = False;
    # Parcurgem fiecare element de anun? pentru a extrage informa?iile despre ma?ini
    for ad_element in ad_elements:
        #  print(ad_element)
        # Ob?inem informa?iile despre ma?ina
        title = ad_element.find('h6')
        price = ad_element.find('p', {'data-testid': 'ad-price'})
        yearandkm = ad_element.find('div', {'class': 'css-efx9z5'})
        location = ad_element.find('td', {'class': 'bottom-cell'})
        
        strtitle = str(title.text.strip()).lower();
        strprice = only_numerics(str(price.text.strip()).lower());
        
        text = text.lower()
        if(text != "" and ( not text in strtitle)):
            continue
        
        year = "1000"
        if(yearandkm is not None and str(yearandkm.text.strip()).find(" - ") != -1):
            split = yearandkm.text.strip().split(" - ")
            year = split[0]
            km = split[1]

        stryear = only_numerics(str(year))

        if((strtitle.find("leasing") != -1 or strtitle.find("rate") != -1)):
            if(strprice == "") :
                find_items  = True
                print(f"AN:{stryear} Pret: LIPSA!. {strtitle} ")  
                data.update([(stryear, 'LIPSA', strtitle)])
            else :
                if (int(strprice) < 45000) :
                    find_items  = True
                    print(f"AN:{stryear} Pret: {strprice}. {strtitle} ") 
                    data.update([(stryear, strprice, strtitle)])
        
        if (stryear != "" and strprice != "") :
            if(int(stryear) > 2008 and int(strprice) < 10000) :
                find_items  = True
                print("AN:" + stryear + " Pret: " +  strprice +  ". " + strtitle)   
                data.update([(stryear, strprice, strtitle)])
            if(int(stryear) > 2016 and int(strprice) < 35000) :
                find_items  = True
                print("AN:" + stryear + " Pret: " +  strprice +  ". " + strtitle)
                data.update([(stryear, strprice, strtitle)])
        
        if(int(stryear) > 2016 and strprice == "") :
            find_items  = True
            print("AN:" + stryear + " Pret: LIPSA! " + strtitle)
            data.update([(stryear, 'LIPSA', strtitle)])
    #endfor
        
    if(find_items) :
        print("[url " + url + " cheie " + model +"]")

#end functions

#cautamasina("marca", "model")

#MAIN

url = 'https://www.olx.ro/auto-masini-moto-ambarcatiuni/autoturisme/lexus/?currency=EUR'

url = "https://www.olx.ro/auto-masini-moto-ambarcatiuni/autoturisme/<BREND>/?currency=EUR&page=<PAGE>"


brend = "lexus"
model = "rx"


#print(only_numerics("59 989,09"))
 
url = url.replace("<BREND>", brend)
for i in range(1, 9) :
    urlsearch = url.replace("<PAGE>", str(i))
    parseurl(urlsearch, model)
    


for val in data:
    print(val)
