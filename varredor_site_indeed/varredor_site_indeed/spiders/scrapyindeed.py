import scrapy
import logging
from selenium.webdriver.remote.remote_connection import LOGGER
from selenium.common.exceptions import *
from selenium.webdriver.support import expected_conditions as CondicaoExperada
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from scrapy.selector import Selector
from time import sleep



class SpiderIndeed(scrapy.Spider):
    # identidade
    name = 'botindeed'
    # request
    def start_requests(self):
        urls = ['https://br.indeed.com/jobs?q=python&l=&from=searchOnHP&vjk=6e6cef681619c176']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    # response
    def parse(self, response):  

        for vaga in response.xpath("//td[@class='resultContent']"): 
            yield{
                'Cargo' : vaga.xpath(".//span[1]/text()").get(),
                'nome_empresa' : vaga.xpath(".//span[@class='companyName']/text()").get(),
                'local' : vaga.xpath(".//div[@class='companyLocation']/span/text()").get(),
                'link' : 'https://br.indeed.com' + vaga.xpath(".//a/@href").get()
            }    
              