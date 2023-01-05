from urllib import response
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from optparse import Option
import random
from unicodedata import name
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import ElementNotInteractableException, TimeoutException, NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pandas as pd
import time
import csv
import json
import os

class webScraper (object):
    listaDeProdutos: list = []
    
    elemtet_data: dict = {
        "columnas": ["Titulos", "Precios"],
        "Titulos": [],
        "Precios": [],
        "categorias-link": [],
        "categorias": []
    }
    data = [("productos", listaDeProdutos),
            ("titulos",elemtet_data["Titulos"]), 
            ("titulos", elemtet_data["Precios"])]

    driver = 'D:\ProyectosCarToro\scraping\webscraper\webscraper\ChromeSetup.exe'    
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = chrome_options.binary_location = "C:\Program Files\Google\Chrome Beta\Application\chrome.exe"
    driver = webdriver.Chrome(service=ChromeService(
        ChromeDriverManager().install()), chrome_options=chrome_options)
    driver.minimize_window()
    driver.get("https://www.homecenter.com.co/homecenter-co/landing/cat5130007/")
    html = driver.page_source
    # time.sleep(0.1)
    botones:list = []
    def categorias(self):    
        categorias_list = self.driver.find_element(By.XPATH, '//*[@id="main"]/section/div[2]/aside/section/menu/ul').find_element(
            By.CLASS_NAME, 'jq-accordion').find_elements(By.XPATH, '//*[@id="main"]/section/div[2]/aside/section/menu/ul/li/a')
        # time.sleep()
        self.list_categories: list = []
        rango_lista_1: list = []
        for ul in categorias_list:
        
            href = ul.get_attribute('href')
            self.list_categories.append(href)
        list_pagination:list = []
        self.productos_list = []
        print(self.list_categories)

        for self.i in range(len(self.list_categories)):
                # time.sleep(1.10)
                self.driver.get(self.list_categories[self.i])
                # time.sleep(0.10)
                # time.sleep(5)
                self.driver.implicitly_wait(10)
                linkDelproducto = self.driver.find_elements(By.XPATH, '//*[@id="title-pdp-link"]')
                for a in linkDelproducto:
                    # time.sleep(0.10)
                    self.productos_list.append(a.get_attribute("href"))
                print(self.productos_list)
                break
            # self.driver.get(list_categories[i] + f"?currentpage={point_links}")
                        
                
    def pasarPagina(self):
            
            botton = self.driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div[7]/div[3]/div[1]/div[1]/div[4]/div[1]/div').find_elements(By.CSS_SELECTOR, "button.jsx-4278284191")
            
            for point_links in range(len(botton)):
                a = self.list_categories[self.i]
                print(a[-0:])
                print(point_links)
                print(point_links)
                self.driver.get(self.list_categories[self.i][-0:] + f"?currentpage={point_links +2}")
                linkDelproducto = self.driver.find_elements(By.XPATH, '//*[@id="title-pdp-link"]')
                for a in linkDelproducto:
                    # time.sleep(0.10)
                    self.productos_list.append(a.get_attribute("href"))
                    print(self.productos_list)
                # for i in self.productos_list:
                #     # print()
                #     # print(self.productos_list[int(i)])
                    
                #     time.sleep(4)
                #     self.driver.get(i)
                #     print("pase, line 104")
                #     time.sleep()
                    
            
    def dataProducto(self):
        dict_de_productos:dict = {'Titulo': [], 'precio': []}
        for i in self.productos_list:
            # time.sleep(5)
            self.driver.get(i)
            # time.sleep(1.30)
            titulo = self.driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div[4]/div[2]/div[1]/div[1]/h1').text
            # time.sleep(1.30)
            precio = self.driver.find_element(By. XPATH, '//div[@class="jsx-2167963490 primary"]/span[2]').text
            fichaTecnica = self.driver.find_element(By.XPATH, '//div[@class="jsx-3969330179 jsx-3762308956 row jsx-967453414"]')
            
            print("--------------------------------ficha tecnica")
            print(fichaTecnica)
            print("--------------------------------")
            print(titulo)
            dict_de_productos["Titulo"].append(titulo)
            print(precio)
            dict_de_productos["precio"].append(precio)
            print("--------------------------------")
            print(dict_de_productos)
            # time.sleep(4)
        df = pd.DataFrame(dict_de_productos["Titulo"])
        df2 = pd.DataFrame(dict_de_productos["precio"])
        df3 = pd.DataFrame.from_dict(dict_de_productos)
        df3.to_csv("dict_completo3.csv", sep=";")

            
            
                # linkDelproducto = self.driver.find_elements(By.XPATH, '//*[@id="title-pdp-link"]')
                # for a in linkDelproducto:
                #     time.sleep(0.10)
                #     self.productos_list.append(a.get_attribute("href"))
                #     print(a.get_attribute("href"))
    # def pasarPagina(self):
    #     pass
        # for a in linkDelproducto:
        #     time.sleep(0.10)
        #     self.productos_list.append(a.get_attribute("href"))
        #     print(a.get_attribute("href"))
                
                
                # return self.driver.get(list_categories[i])
    def producto(self):
        print("hola estoy aca")
        self.driver
        print("hola estoy aca X2")
        
        
        # linkDelproducto = self.driver.find_elements(By.XPATH, '//*[@id="title-pdp-link"]')
        # for i in linkDelproducto:
        #     i.click()
        #     print(titulo)
            
        #     time.sleep(1000)
            
        
        
clase1 = webScraper()
clase1.categorias()
clase1.pasarPagina()
clase1.dataProducto()
# clase1.pasarPagina()
    # # df = pd.DataFrame(elemtet_data)
    # df1 = pd.DataFrame(data=elemtet_data["Titulos"])
    # df2 = pd.DataFrame(elemtet_data["Precios"])

    # df4 = pd.DataFrame(data=elemtet_data["categorias"])
    # df5 = df4.to_csv("Datavajilla.csv" )

    # # df = pd.DataFrame({"Precios":[elemtet_data["Precios"]], "Titulos": [elemtet_data["Titulos"]]})
    # df2.to_excel("data234112.xlsx" )
    # print(df1)
    # print(df4)

    # print(df4)
    # print(df4.iloc[1:], "DF4 HOLA")

# except Exception as error:
#     print(f"ESTE ES EL ERROR!!! {error}")
