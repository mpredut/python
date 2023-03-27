#!/usr/bin/python
# -*- coding: latin-1 -*-

import requests
from bs4 import BeautifulSoup
from re import search


url = "https://www.olx.ro/auto-masini-moto-ambarcatiuni/autoturisme/<BREND>/?currency=EUR&page=<PAGE>&search%5Bfilter_enum_model%5D%5B0%5D=<MODEL>"


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
        ancora = ad_element.find('a', href=True);
        #<a class="css-rc5s2u" href="/d/oferta/toyota-hilux-2017-IDfSZon.html">
        
        strtitle = str(title.text.strip()).lower();
        
        strprice = ""
        if(price is not None) :
            strprice = only_numerics(str(price.text.strip()).lower());
        
        text = text.lower()
        #if(text != "" and ( not text in strtitle)):
        #    continue
        
        year = "1000"
        if(yearandkm is not None and str(yearandkm.text.strip()).find(" - ") != -1):
            split = yearandkm.text.strip().split(" - ")
            year = split[0]
            km = split[1]

        if(ancora is not None) : 
            #print("Ancora " + ancora['href']);
            strancora = ancora['href'];
        if(not search("www.autovit.ro", strancora)): 
            strancora = "https://www.olx.ro/" + strancora;
            
        stryear = only_numerics(str(year))

        if((strtitle.find("leasing") != -1 or strtitle.find("rate") != -1)):
            if(strprice == "") :
                find_items  = True
                #print(f"AN:{stryear} Pret: LIPSA!. {strtitle} ")  
                data.update([(stryear, 'LIPSA', strtitle, strancora)])
            else :
                if (int(strprice) < 41000) :
                    find_items  = True
                    #print(f"AN:{stryear} Pret: {strprice}. {strtitle} ") 
                    data.update([(stryear, strprice, strtitle, strancora)])
        
        if (stryear != "" and strprice != "") :
            if(int(stryear) > 2008 and int(strprice) < 10000) :
                find_items  = True
                #print("AN:" + stryear + " Pret: " +  strprice +  ". " + strtitle)   
                data.update([(stryear, strprice, strtitle, strancora)])
            if(int(stryear) > 2016 and int(strprice) < 32000) :
                find_items  = True
                #print("AN:" + stryear + " Pret: " +  strprice +  ". " + strtitle)
                data.update([(stryear, strprice, strtitle, strancora)])
        
        if(int(stryear) > 2016 and strprice == "") :
            find_items  = True
            #print("AN:" + stryear + " Pret: LIPSA! " + strtitle)
            data.update([(stryear, 'LIPSA', strtitle, strancora)])
    #endfor
        
    if(find_items) :
        print("[url " + url + " cheie " + text +"]")

#end functions

#cautamasina("marca", "model")

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
    nb = soup.find('div', {'data-testid': 'total-count'})
    #print(nb)
    if(nb is None) :
       print("nu exista pagina " + urlsearch)
       return;
    strnb = only_numerics(nb.text)
    if(strnb == "") : #//nu sunt rezultate pt. cautare
        print("nu sunt rezultate pentru "+ urlsearch)
        return;
    nb = int(int(strnb) / 32) + 1
    print(strnb + " anunturi in " + str(nb) + " pagini pentru " + model)
    
    for i in range(1, nb) :
        urlsearch = urlreal.replace("<PAGE>", str(i))
        parseurl(urlsearch, model)
       
    global data       
    datas = sorted(data)
    print("")
    for val in datas:
        print(val)

#MAIN

brend = "lexus"
model = "rx"

cautamasina("ford", "explorer")
cautamasina("lexus", "seria-rx")
cautamasina("lexus", "egyeb") #altul
#cautamasina("toyota", "land-cruiser")
#cautamasina("bmw", "x5")
#cautamasina("nissan", "navara")
#cautamasina("toyota", "hilux")
