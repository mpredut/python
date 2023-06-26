#!/usr/bin/python
# -*- coding: latin-1 -*-

import requests
from bs4 import BeautifulSoup

url = "https://www.autovit.ro/autoturisme/<BREND>/<MODEL>?page=<PAGE>"

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
  
  
def by_year(ele):
    ele[0]

 
def by_price(ele):
    return ele[1]
  
    
def only_numerics(seq):
    seq = seq.split(",")[0]
    seq_type = type(seq)
    return seq_type().join(filter(seq_type.isdigit, seq))
 
 

def parseurl(url, text): 
    
    text = text.lower()
        
    #print("[url " + url + " cheie " + text +"]")    
    response = requests.get(url)

    # Extragem con?inutul paginii web
    content = response.content
    # Analizam con?inutul folosind BeautifulSoup
    soup = BeautifulSoup(content, 'html.parser')

    ad_elements = soup.find_all('article', { 'data-testid': 'listing-ad'})
    
    find_items  = False;
    # Parcurgem fiecare element de anun? pentru a extrage informa?iile despre ma?ini
    for ad_element in ad_elements:
        #print(ad_element)
        year = ad_element.find('li')
        
        # span aria-hidden="true" data-make="lexus" data-placeholder="financing-widget" data-price="43900" data-testid="financing-widget" data-title="Lexus Seria NX 300h AWD">
        title = ad_element.find('span', {'aria-hidden': 'true'})
        if( title is None) :
           continue
  
        price = title["data-price"]
        title = title["data-title"]
        ancora = ad_element.find('a', href=True);
        if(ancora is not None) : 
            #print("Ancora " + ancora['href']);
            strancora = ancora['href'];

        detail = ad_element.find('p')
        if (detail is not None) :
            title = title + " " + detail.text.lower();
        
        year = year.text.lower();
        stryear = only_numerics(str(year))      
        strtitle = str(title).lower();
        
        strprice = "0";
        if( price is not None) :
            strprice  = str(price);
        strprice = only_numerics(strprice);
        if(strprice == "") :
            strprice = "0";
       
        #pentru detallii cauta <a href="https://www.autovit.ro/anunt/lexus-seria-nx-ID7H5QwU.html" target="_self">
              
        #if(text != "" and ( not text in strtitle)):
        #    continue

        if((strtitle.find("leasing") != -1 or strtitle.find("rate") != -1)):
            if (int(strprice) < 41000) :
                find_items  = True
                #print(f"AN:{stryear} Pret: {strprice}. {strtitle} ") 
                data.update([(stryear, strprice, strtitle, strancora)])
                    
        
        if (stryear != "" and strprice != "") :
            if(int(stryear) > 2008 and int(strprice) < 10000) :
                find_items  = True
                #print("AN:" + stryear + " Pret: " +  strprice +  ". " + strtitle)   
                data.update([(stryear, strprice, strtitle)])
            if(int(stryear) > 2016 and int(strprice) < 33000) :
                find_items  = True
               # print("AN:" + stryear + " Pret: " +  strprice +  ". " + strtitle)
                data.update([(stryear, strprice, strtitle, strancora)])
        
        if(int(stryear) > 2016 and strprice == "") :
            find_items  = True
            #print("AN:" + stryear + " Pret: LIPSA! " + strtitle)
            data.update([(stryear, 'LIPSA', strtitle, strancora)])
    #endfor
        
    if(find_items) :
        print("[url " + url + " cheie " + text +"]")

#end functions

def cautamasina(brend, model): 
    print("")
    
    global url
    urlreal = url.replace("<BREND>", brend)
    urlreal = urlreal.replace("<MODEL>", model)

    #get nb of items to calculate nb of pages
    urlsearch = urlreal.replace("<PAGE>", "1")
    response = requests.get(urlsearch)
    content = response.content
    soup = BeautifulSoup(content, 'html.parser')
    nb = soup.find('h1')
    if(nb is None) :
       print("nu exista pagina " + urlsearch)
       strnb = "1000"
    else :
        strnb = only_numerics(nb.text)
    if(strnb == "") : #//nu sunt rezultate pt. cautare
        print("nu sunt rezultate pentru "+ urlsearch)
        return;
    nb = int(int(strnb) / 32) + 1
    print(str(nb) + " pagini pentru " + model)
    
    for i in range(0, nb + 1) :
        urlsearch = urlreal.replace("<PAGE>", str(i))
        parseurl(urlsearch, model)
       
    global data       
    datas = sorted(data)
    print("")
    for val in datas:
        print(val)

#MAIN


cautamasina("ford", "explorer")
cautamasina("ford", "mustang")
cautamasina("lexus", "seria-rx")
cautamasina("lexus", "altul")
cautamasina("toyota", "land-cruiser")
cautamasina("toyota", "highlander")
#cautamasina("bmw", "x5")
#cautamasina("nissan", "navara")
cautamasina("toyota", "hilux")
cautamasina("land-rover","")