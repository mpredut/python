#!/usr/bin/python
# -*- coding: latin-1 -*-

import requests
from bs4 import BeautifulSoup
from re import search


yearreference = 2006 - 1
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
 
 

def parseurl(url, text, minyear, maxprice): 
    
    global yearreference
    
    ratereference = maxprice / (minyear - yearreference)
    text = text.lower()
    print("[url " + url + " cheie " + text +"]")
    #print("rateref " + str(ratereference))
    
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
        
        strprice = "0"
        if(price is not None) :
            strprice = only_numerics(str(price.text.strip()).lower());
        if(strprice == "") :
            strprice = "0";
        
        #text = text.lower()
        #if(text != "" and ( not text in strtitle)):
        #    continue
 
        year = "1000"
        if(yearandkm is not None and str(yearandkm.text.strip()).find(" - ") != -1):
            split = yearandkm.text.strip().split(" - ")
            year = split[0]
            km = split[1]

        stryear = only_numerics(str(year))
        
        
        if(int(stryear) <= yearreference) :
            continue;

        if(ancora is not None) : 
            #print("Ancora " + ancora['href']);
            strancora = ancora['href'];
        if(not search("www.autovit.ro", strancora)): 
            strancora = "https://www.olx.ro/" + strancora;
        #print(strancora)
            
        rate = int(strprice) / (int(stryear) - yearreference)
        #print("rate " + str(rate))
        if(rate > ratereference) :
            #print("ratereference" + str(ratereference))
            #print(strancora)
            continue;
        
        if((strtitle.find("leasing") != -1 or strtitle.find("rate") != -1)):
            if (int(strprice) < 41000) :
                find_items  = True
                #print(f"AN:{stryear} Pret: {strprice}. {strtitle} ") 
                data.update([(stryear, strprice, strtitle, strancora)])
                    

        if (stryear != "" and strprice != "") :
            if(int(stryear) > 2008 and int(strprice) < 14000) :
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


def cautamasina(brend, model, minyear, maxprice): 
    print("")

    global url
    urlreal = url.replace("<BREND>", brend)
    urlreal = urlreal.replace("<MODEL>", model)
    
     #get nb of items to calculate nb of pages
    urlsearch = urlreal.replace("<PAGE>", "1")
    response = requests.get(urlsearch)
    content = response.content
    soup = BeautifulSoup(content, 'html.parser')
    #print(soup)
    nb = soup.find('span', {'data-testid': 'total-count'})
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
    
    for i in range(0, nb) :
        urlsearch = urlreal.replace("<PAGE>", str(i))
        parseurl(urlsearch, model, minyear, maxprice)
       
    global data       
    datas = sorted(data)
    print("")
    for val in datas:
        print(val)

#MAIN


#Anul de referinta este setat la 2005. vei cauta incepand cu 2006

cautamasina("maserati", "", 2008, 8000)
cautamasina("ford", "explorer", 2008, 8000)
cautamasina("ford", "mustang", 2008, 6000)
cautamasina("lexus", "seria-rx", 2008, 8000)
cautamasina("lexus", "seria-lx", 2008, 8000)
cautamasina("lexus", "egyeb", 2008, 8000) #altul
cautamasina("toyota", "land-cruiser", 2008, 8000)
#cautamasina("bmw", "x5", 2010, 8000)
#cautamasina("volvo", "xc-90", 2010, 8000)
#cautamasina("volvo", "xc-60", 2010, 6000)
cautamasina("nissan", "navara", 2008, 4500)
cautamasina("toyota", "hilux", 2008, 7000)
cautamasina("toyota", "highlander", 2008, 7000)
#cautamasina("land-rover","", 2008, 5500)
#cautamasina("mercedes-benz","gle", 2008, 7000)
#cautamasina("mercedes-benz","gls", 2008, 8000)
#cautamasina("mercedes-benz","gl-class", 2008, 7000)


