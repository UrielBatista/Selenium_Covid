from selenium import webdriver
from random import randrange, uniform
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
import requests
from bs4 import BeautifulSoup
import re
from time import sleep
from pymongo import MongoClient


#[brazil, venezuela, israel, poland, ireland, newyork_unitedstates]

pais = ['brazil', 'venezuela', 'israel', 'poland', 'ireland', 'newyork_unitedstates', 
'amazonas_brazil', 'bahia_brazil', 'sopaulo_brazil', 'minasgerais_brazil', 'cear_brazil', 
'maranho_brazil', 'acre_brazil', 'roraima_brazil', 'par_brazil', 'matogrosso_brazil', 'riodejaneiro_brazil', 
'paran_brazil', 'santacatarina_brazil', 'riograndedosul_brazil', 'matogrossodosul_brazil',
'gois_brazil', 'federaldistrict_brazil', 'tocantins_brazil', 'paraiba_brazil']

class Scraping:
    def __init__(self):
        print('...CAPTURANDO DADOS!!...')
        
        #Conexao com o servidor local
        self._client = MongoClient("localhost", 27017)
        self._db = self._client.Covid
    
    def scrap_and_insert(self):
        
        result = []
        
        try:
            
            print('...Dados page...')

            self._db.dados_covid.delete_many({})
            print('...Deletando dados antigos...')

            sleep(4)
            cont = 0

            webdriver.FirefoxProfile()
            driver = webdriver.Firefox()
            
            while(pais):

                driver.get('https://www.bing.com/covid/local/{}?cc=br'.format(pais[cont]))
                driver.set_page_load_timeout(60)

                #Casos ativos
                ativos = driver.execute_script("return document.getElementsByClassName('total')[3].innerText;")
                if(ativos == ''):
                    ativos = 'Nao a casos ativos!!'
                print(ativos)

                #Casos recuperados
                recuperados = driver.execute_script("return document.getElementsByClassName('total')[4].children[0].innerText")
               
                if(len(recuperados)):
                    print(recuperados)

                if(recuperados == '-'):
                    recuperados = 'Nao existe casos recuperados'
                
                #Casos fatais
                fatais = driver.execute_script("return document.getElementsByClassName('legend')[5].innerText;")
                regex1 = re.findall(r"[0-9]{0,3}[.][0-9]{0,3}", fatais)
                regex2 = re.findall(r"[0-9]{2,3}", fatais)
                
                if(len(regex1)):
                    fatais = regex1[0]
                    print(fatais)

                elif(len(regex2)):
                    fatais = regex2[0]
                    print(fatais)
                
                else:
                    fatais = 'Nao existe casos fatais'
                
                num = randrange(0, 456156)

                self._db.dados_covid.insert_one({
                    
                    "id": num,
                    "UF": pais[cont],
                    "Ativos": ativos,
                    "Recuperados": recuperados,
                    "Fatais": fatais
                })
                
                cont = cont + 1
                
        except Exception as exception:
            print('===========ERROR============')
            print(exception)

    
          
