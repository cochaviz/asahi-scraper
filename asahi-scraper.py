#!/usr/bin/python

import re
import sys
import csv
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains 
from selenium.common.exceptions import NoSuchElementException


def parse_dates(filename, username, passwd, search_query, range=[1984, 2021]):
    url = 'https://login.ezproxy.leidenuniv.nl/login?qurl=http://database.asahi.com%2findex.shtml'

    # Start
    driver = webdriver.Chrome("chromedriver")
    driver.get(url)

    print("Succesfully found and started the chromedriver")
    print("User query: " + search_query)
    print("Looking from " + str(range[0]) + " to " + str(range[1]) + "\n")

    # -- LEIDEN UNIV ---
    print("Loggin in to leidenuniv...")
    
    # SSO
    login_button = driver.find_element_by_id('sso')
    login_button.click()

    # Enter creds
    username_field = driver.find_element_by_name('Ecom_User_ID')
    passwd_field = driver.find_element_by_name('Ecom_Password')

    username_field.send_keys(username)
    passwd_field.send_keys(passwd)

    # Wait for second login button
    driver.implicitly_wait(5)
    login_button = driver.find_element_by_id('loginbtn')
    login_button.click()

    print("Successful!")

    # --- ASAHI ---
    print("Logging in to asahi...")

    # Login
    login_xpath = '/html/body/div[1]/div[2]/div/div/div[1]/p[1]/a'
    login_button = driver.find_element_by_xpath(login_xpath)
    login_button.click()
    
    print("Successful!")

    # Wait after login, because it's slooooooww   
    driver.implicitly_wait(5)

    print("Entering query...")

    # Asahi uses iframes for each of the web elements, bruh
    search_iframe_xpath = '/html/frameset/frame[2]'
    search_iframe = driver.find_element_by_xpath(search_iframe_xpath)
    driver.switch_to.frame(search_iframe)

    # Set advanced search
    query_field= driver.find_element_by_id('txtWord_ID')
    query_field.send_keys(search_query)

    # Enter query
    advanced_search= driver.find_element_by_id('rdoSrchMode2') 
    advanced_search.click()

    # Only scan title and contents
    select_article_name_and_content = driver.find_element_by_id('rdoSrchItem2')
    select_article_name_and_content.click()
    
    # Set range (1984-2021)
    action = ActionChains(driver);
    from_year = driver.find_element_by_name('cmbIDFy')
    to_year = driver.find_element_by_name('cmbIDTy')
    
    print("Successful!")

    # Search
    driver.implicitly_wait(5)
    search_button = driver.find_element_by_xpath('/html/body/center/form[2]/table/tbody/tr[2]/td/table/tbody/tr[4]/td[2]/div/input[2]')

    # Perform!
    action.move_to_element(from_year).click().send_keys(str(range[0]) + '\n')\
          .move_to_element(to_year).click().send_keys(str(range[1]) + '\n')\
          .pause(1)\
          .move_to_element(search_button).click().perform()

    print("Searching and parsing dates...\n")

    # Regex expression for extracting dates
    page = 1
    date_expression = '([0-9]{4}).+?([0-9]{2}).+?([0-9]{2}).+?'

    # Open output file
    myfile = open(filename + ".csv", 'a', newline='')
    print("Opened file: " + filename + ".csv")
    file_writer = csv.writer(myfile, quoting=csv.QUOTE_ALL)

    # Now cycle through the pages and extract the dates
    while True:
        # User feedback
        print("Reading page " + str(page) + "...")
        

        # Get elements
        date_elements = driver.find_elements_by_xpath("//td[@class='topic-list']")
        
        # Collapse the list
        date_text_list = map(lambda e : e.text, date_elements)

        # Look through our list for matches
        dates = []

        for text in date_text_list:
            match = re.match(date_expression, text)
            # If it matches, format and append
            if match:
                dates.append(match.group(3) + "-" + match.group(2) + "-" + match.group(1))

        # Write matches to file
        print("Appending to file...")
        print(dates, "\n")
        file_writer.writerow(dates)
       
        # Try to get next page
        next = getNext(driver)
        
        # Return if we don't have anymore
        if not next:
            break;

        # Continue to next page
        page += 1
        next.click()


def getNext(driver):
    next = None

    try:
        next = driver.find_element_by_name('next') 
    except NoSuchElementException:
        pass
    finally:
        return next


def create_file(filename="out"):
    with open(filename + ".csv", 'w', newline='') as myfile:
     print("Created " + filename + ".csv")

    return filename


if __name__=="__main__":
    if len(sys.argv) < 2:
        print("usage: asahi-scraper <username> <passwd> optional:<file_name>")
        exit(1)

    username = sys.argv[1]
    passwd = sys.argv[2]
    
    search_query = "国産"
    lookup_range = [1984, 2021]
    
    file = None
    filename = None
    
    if len(sys.argv) > 3:
        filename = create_file(filename=sys.argv[3])
    else:
        filename = create_file()

    parse_dates(filename, username, passwd, search_query, range=lookup_range)
    
    exit(0)
    
