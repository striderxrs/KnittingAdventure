import os
import csv
import requests
import pyodbc
from bs4 import BeautifulSoup
import sqlite3
from sqlite3 import Error


def wollplatz(source):

    url = source
    r = requests.get(url)

    #print(r.status_code)
    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            #print(response.status_code)
            response.raise_for_status()
    except requests.exceptions.RequestException as err:
        print("Encountered some Exception", err)


    soup = BeautifulSoup(r.text, 'html.parser')
    specs = soup.find('div', class_ = 'pdetail-specsholder').text.strip()


    '''Find the product name'''
    product_name = soup.find('div', class_ = 'variants-title').text.strip()
    print(product_name)


    '''Finding Composition'''
    composition_index_start = specs.find('Zusammenstellung')
    composition_index_end = composition_index_start + 16

    composition_percentage_start = composition_index_end
    composition_percentage_end = specs.find('Nadelstärke') - 1

    composition = (specs[composition_index_start:composition_index_end],':',specs[composition_percentage_start:composition_percentage_end])
    print(composition)

    ''' Finding needle size index and its value'''
    needle_index_start = specs.find('Nadelstärke')
    needle_index_end = needle_index_start + 11

    needle_size_value_start = needle_index_end
    needle_size_value_end = needle_size_value_start + 4

    needle_size = (specs[needle_index_start:needle_index_end],':', specs[needle_size_value_start:needle_size_value_end])
    print(needle_size)

    '''Finding price information (watch out for discounts)'''
    price = soup.find('div', class_ = 'buy-price').text.strip()
    price_index_start = 0
    price_index_end = price_index_start + 7

    price_with_vat_start = 97
    price_with_vat_end = price_with_vat_start + 15

    price_actual = (price[price_index_start:price_index_end])
    price_minus_tax = (price[price_with_vat_start:price_with_vat_end])
    print(price_actual)
    print(price_minus_tax)

    '''Find out if the product is in stock or not'''
    in_stock = soup.find('div', id = 'ContentPlaceHolder1_upStockInfoDescription').text.strip()
    print(in_stock)

    save_to_csv(product_name, composition, needle_size, price_actual, price_minus_tax, in_stock)


def save_to_csv(product_name, composition, needle_size, price_actual, price_minus_tax, in_stock):

    ''' Write product data to a csv file'''
    ''' Modify tuple data to only write needed information'''

    composition = composition[2]
    needle_size = needle_size[2]

    fields = ['Product Name', 'Composition', 'Needle Size', 'Price', 'Price excl Tax', 'Availability']

    rows = [product_name, composition, needle_size, price_actual, price_minus_tax, in_stock]

    file_name = 'KnittingAdventure.csv'


    with open(file_name, 'a+') as csvfile:
        data_writer = csv.writer(csvfile)
        file_empty = os.stat(file_name).st_size == 0
        if file_empty:
            data_writer.writerow(fields)

        data_writer.writerow(rows)
        csvfile.close()

    create_table(product_name, composition, needle_size, price_actual, price_minus_tax, in_stock)


def create_table(product_name, composition, needle_size, price_actual, price_minus_tax, in_stock):


    connection_obj = sqlite3.connect('pricelist.db')
    cursor_obj = connection_obj.cursor()

    ''' Create Table '''

    table = """CREATE TABLE IF NOT EXISTS PRICELIST(
    Product VARCHAR(255) NOT NULL,
    Composition VARCHAR(255),
    NeedleSize VARCHAR(100),
    TotalPrice VARCHAR(100),
    PricebeforeVAT VARCHAR(100),
    Availability CHAR(30)
    ); """

    cursor_obj.execute(table)
    #print("table is ready")

    '''Insert into Table'''

    cursor_obj.execute("insert into PRICELIST (Product, Composition, NeedleSize, TotalPrice, PricebeforeVAT, Availability) values(?,?,?,?,?,?)",(product_name, composition, needle_size, price_actual, price_minus_tax, in_stock))


    connection_obj.commit()
    connection_obj.close()
    return cursor_obj.lastrowid



if __name__ == '__main__':


    with open('urllist.csv', 'r') as file:
        data = file.readlines()

    for url_index in data:
        print(url_index)
        wollplatz(url_index)

    file.close()



    ''' Welcome to the Land of Promises! '''
    ''' Attempting to save output to a Microsoft Access Database''' '''DLC Content'''

    #
    # dbname = r'C:/Users/Guest/Desktop/NewDB.mdb'
    # constr = "DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={0};".format(dbname)
    #
    # dbconn = pyodbc.connect(constr)
    #
    # cursor = dbconn.cursor()
    # for i in cursor.tables(tableType='TABLE'):
    #     print(i.table_name)
    #
    # for i in cursor.tables(tableType='VIEW'):
    #     print(i.table_name)
    #
    # cursor.execute('create table Pricelist(Product_name string, Composition string, Needle_size string, Total_Price string, Price_before_VAT string, Availability string)')
    # cursor.commit()
    #
    # cursor.execute('INSERT INTO Pricelist (Product_name string, Composition string, Needle_size string, Total_Price string, Price_before_VAT string, Availability string)'
    #                'VALUES ('product_name', 'composition', 'needle_size', 'price_actual', 'price_minus_tax', 'in_stock' )')
    # cursor.commit()

    ''' Attempt to create a dynamic URL maker based on search term ''' '''DLC Content'''

    #     import csv
    #     import html
    #     from bs4 import BeautifulSoup
    #     from selenium import webdriver
    #     from lxml import etree
    #     from selenium.webdriver.common.by import By
    #     from selenium.webdriver.support.ui import WebDriverWait
    #     from selenium.webdriver.support import expected_conditions as ec
    #
    #     #driver = webdriver.Firefox()
    #     driver = webdriver.Chrome()
    #
    #     def get_url(search_term):
    #         ''' We need a url for search term.A placeholder for now https://
    #         wollplatz.de /  # sqr:(q[DMC%20Natura%20XL])'''
    #     web_address = 'https://www.wollplatz.de/#sqr:(q[{}])'  # using curly braces to add in the search term in the future
    #     # driver.get(web_address)
    #
    #     ''' note 1 - website has a cookie accept dialog ( have to deal with it)'''
    #
    #     ''' Next to insert search term '''
    #
    #     search_term = search_term.replace(' ', '%20')
    #     print(search_term)
    #     return web_address.format(search_term)
    #
    #
    # ''' Try to get sample search term'''
    # url = get_url('DMC Natura XL')
    # print(url)
    # driver.get(url)
    #
    # ''' Handle the cookie popup (yeah not a good idea to accept all cookies)'''
    # cookie_alert = driver.find_element_by_link_text('Alle zulassen')
    # cookie_alert.click()
    #
    # '''Taking the first product listed DMC Natura XL as an example, data extraction'''
    # # required_product = driver.find_element_by_class_name('productlistholder productlist25 sqr-resultItem data-id=4216')
    #
    # '''Wollplatz doesnt offer product info on the search results page, so needs a click to get to the page'''
    # required_product = driver.find_element_by_link_text('DMC Natura XL')
    # required_product.click()
    #
    # ''' now, data extraction : take 1'''
    # '''Initialize BeautifulSoup parse'''
    #
    # soup = BeautifulSoup(driver.page_source, "html.parser")
    # # soup = BeautifulSoup(driver.page_source, "lxml")
    #
    # dom = etree.HTML(str(soup))
    #
    # res = (dom.xpath('//*[@id="pdetailTableSpecs"]/table/tbody/tr[4]/td[1]'))
    #
    # for i in res:
    #     print(i)
    #     print('------')
    #
    # res1 = soup.find('tr', string='Nadelstärke')
    # print(res1)
    #
    # attrs = []
    # for elm in soup():  # soup() is equivalent to soup.find_all()
    #     attrs += list(elm.attrs.values())
    #
    # print(attrs)
    #
    # res2 = soup.find_all('div', attrs='.pdetail-detailholder')
    # print(res2)
    #
    # for tr in soup.find_all('tr')[2]:
    #     tds = tr.find_all('td')
    #     print(tds)