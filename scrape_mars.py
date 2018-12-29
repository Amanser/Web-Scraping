from bs4 import BeautifulSoup 
from splinter import Browser
import pandas as pd 
import requests
import time 


def init_browser(): 
    
    # Chromedriver setup for Windows. Chromedrive is set as a path variable
    executable_path = {'executable_path': 'chromedriver.exe'}
    
    return Browser('chrome', headless=True, **executable_path)

mars_info = {}

def scrape_news():
    
    browser = init_browser()

    url = 'https://mars.nasa.gov/news/'
    
    browser.visit(url)

    time.sleep(1)

    html = browser.html
    
    soup = BeautifulSoup(html, "html.parser")

    news_title = soup.find('div', class_='content_title').find('a').text.strip()

    news_p = soup.find_all(class_="rollover_description_inner")[0].text.strip()

    mars_info['news_title'] = news_title

    mars_info['news_p'] = news_p

    # Close the browser after scraping
    browser.quit()

    return mars_info

def scrape_feature():

    browser = init_browser()

    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    
    browser.visit(url)

    time.sleep(1)

    html = browser.html

    soup = BeautifulSoup(html, 'html.parser')

    url_1 = 'https://www.jpl.nasa.gov'

    url_2 = soup.find_all('img', class_='thumb')[0]['src']

    featured_image_url = url_1 + url_2

    mars_info['featured_image'] = featured_image_url

    # Close the browser after scraping
    browser.quit()

    return mars_info


def scrape_weather():

    browser = init_browser()

    url = 'https://twitter.com/marswxreport?lang=en'
    
    browser.visit(url)

    time.sleep(1)

    html = browser.html
    
    soup = BeautifulSoup(html, 'html.parser')

    mars_weather = soup.find_all('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text')[0].text

    mars_info['weather'] = mars_weather

    # Close the browser after scraping
    browser.quit()

    return mars_info


def scrape_facts():

    facts_url = 'https://space-facts.com/mars/'

    # Use Panda's read the html table
    mars_facts = pd.read_html(facts_url)

    # Find the mars facts DataFrame in the list of DataFrames as assign it to `mars_df`
    mars_df = mars_facts[0]

    # Assign column headers
    mars_df.columns = ['Description','Value']

    # Set the index to the `Description` column
    mars_df.set_index('Description', inplace=True)

    # Add the df to the mars_info dictionary
    mars_info['mars_facts'] = mars_df

    return mars_info


def scrape_hemisphere():

    browser = init_browser()
    
    hemispheres_url = 'http://web.archive.org/web/20181114171728/https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    browser.visit(hemispheres_url)

    time.sleep(1)

    html_hemispheres = browser.html

    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html_hemispheres, 'html.parser')

    # Retreive all items that contain mars hemispheres information
    items = soup.find_all('div', class_='item')

    new_url = 'http://web.archive.org' + items

    browser.visit(new_url)

    time.sleep(1)

    html_hemispheres = browser.html

    soup = BeautifulSoup(html_hemispheres, 'html.parser')

    # Retrieve the url for the full jpeg image
    hemi_img = soup.find('div', class_='wide-image-wrapper').find('li').find('a')['href']

    hemisphere_image_urls = []

    for x in items: 
        # Store title
        title = x.find('h3').text
        
        # Store link that leads to full image website
        partial_img_url = x.find('a', class_='itemLink product-item')['href']
        
        # Visit the link that contains the full image website 
        new_url = 'http://web.archive.org' + partial_img_url
        
        browser.visit(new_url)
        
        # HTML Object of individual hemisphere information website 
        partial_img_html = browser.html
        
        # Parse HTML with Beautiful Soup for every individual hemisphere information website 
        soup = BeautifulSoup( partial_img_html, 'html.parser')
        
        # Retrieve full image source 
        hemi_img = soup.find('div', class_='wide-image-wrapper').find('li').find('a')['href']
        
        # Append the retreived information into a list of dictionaries 
        hemisphere_image_urls.append({"title" : title, "img_url" : hemi_img})
    

    # Display hemisphere_image_urls
    mars_info['hemispheres'] = hemisphere_image_urls

    return mars_info