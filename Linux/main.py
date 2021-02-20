import requests 
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from web_driver_conf import get_web_driver_options
from web_driver_conf import get_chrome_web_driver
from web_driver_conf import set_ignore_certificate_error
from web_driver_conf import set_browser_as_incognito
from web_driver_conf import set_automation_as_head_less
from product import Product

def price_to_number(price):
    try:
        price = price.strip()[:-2].replace(',','.')
    except:
        Exception()
    return float(price)

# Set the Url, maximum namber of pages to search, and the item to find
URL = "https://www.amazon.it/"
NUMBER_OF_PAGES = 4
search_item = str(input('What are you looking for?\n'))

# Setting value do default
biggest_discount = 0.0
lowest_price = 0.0
chepest_product = Product("", "", "", "", "")
best_deal_product = Product("", "", "", "", "")
search_terms = search_item.split(" ")
products = []

# Browser settings
options = get_web_driver_options()
set_automation_as_head_less(options)
set_ignore_certificate_error(options)
set_browser_as_incognito(options)
driver = get_chrome_web_driver(options)

# Find the SearchBar and inserting the item to find, then press enter
driver.get(URL)
element = driver.find_element_by_id('twotabsearchtextbox')
element.send_keys(search_item)
element.send_keys(Keys.ENTER)
print('Elaborating...\n')

current_page = 1
#Loop for 5 pages, for every element trying to get price and previous price

while True:
    if current_page != NUMBER_OF_PAGES:
        try:
            driver.get(driver.current_url + "&page=" + str(current_page))
        except:
            break
#This is the XPath of the div containing all product in the research page
    for i in driver.find_elements_by_xpath('//*[@id="search"]/div[1]/div[2]/div/span[3]/div[2]'):
        counter = 0
#In this XPath we can navigate each element of the div above, wich are the products
        for element in i.find_elements_by_xpath('//div/div/span/div/div/div/div'):
            should_add = True
            name = ""
            price = ""
            prev_price = ""
            link = ""
            try:
                name = i.find_elements_by_tag_name('h2')[counter].text
                price = price_to_number(element.find_element_by_class_name('a-price').text)
                link = i.find_elements_by_xpath('//h2/a')[counter].get_attribute("href")
                try:
                    prev_price = price_to_number(element.find_element_by_class_name('a-text-price').text)
                except:
                    Exception()
                    prev_price = price
                    should_add = False
            except:
                should_add = False

            #product = Product(name, price, prev_price, link)
            can_add = True

#To improve accuracy, if not every word of the searched item is in the name of the selected item, it won't be add
            for word in search_terms:
                if word.lower() not in name.lower():
                    can_add = False

            if(should_add == True and can_add == True):
                new_prod = Product(name,price,prev_price,link,round(prev_price-price,3))
                if(new_prod not in products):
                    products.append(Product(name,price, prev_price, link, round(prev_price-price,3)))
             
            counter = counter + 1
    print('Currently analyzing page ' + str(current_page))
    current_page = current_page + 1
    if current_page == NUMBER_OF_PAGES:
        break

#Ordering the list of products based on the attribute discount 
products.sort(reverse=True)

with open('products.json', 'w') as json_file:
    data = {}
    data["Products"] = []
    for prod in products:
        data["Products"].append(prod.serialize())
    json.dump(data, json_file, sort_keys=True, indent=4)    

run = 0

for product in products:
    if run == 0:
        lowest_price = product.price
        chepest_product = product
        run = 1
    elif product.price < lowest_price:
        lowest_price = product.price
        chepest_product = product

biggest_discount = products[0].discount
best_deal_product = products[0]

print('The cheapest product is:\n')
print(json.dumps(chepest_product.serialize(), indent=4, sort_keys=True))
print('The best deal is: ')
print(json.dumps(best_deal_product.serialize(), indent=4, sort_keys=True))

#Finally opening the first 5 links of the list
options = get_web_driver_options()
set_ignore_certificate_error(options)
driver = get_chrome_web_driver(options)
driver.get(products[0].link)
for element in products[1:6]:
    driver.execute_script("window.open('"+element.link+"')")

driver.quit
