import os
from bs4 import BeautifulSoup
import requests
import html
import pyodbc
from selenium.webdriver import *
import lxml
import sqlite3

''' Experimental Part 1 - Adding Amazon.de results '''

base_url = 'https://www.amazon.de/s?k={}'

#Amzn URL format : https://www.amazon.de/s?k=dmc+natura+xl

search_term = 'dmc natura xl'
search_term = search_term.replace(' ', '+')

url = base_url.format(search_term)

print(url)










