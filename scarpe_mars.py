
from bs4 import BeautifulSoup
import requests
from splinter import Browser
import pandas as pd

def scrape():
# # NASA Mars News

# URL of page to be scraped
    url = 'https://mars.nasa.gov/news/'

# Retrieve page with the requests module
    response = requests.get(url)
# Create BeautifulSoup object; parse with 'lxml'
    soup = BeautifulSoup(response.text, 'lxml')
#Scrape the NASA Mars News Site and collect the latest News Title and Paragraph Text. 
#Assign the text to variables that you can reference later
#News Title from the webpage
    news_title = soup.find_all(class_='content_title')[0].text
    
#News Paragraph Text
    news_p = soup.find_all(class_='rollover_description_inner')[0].text

# # JPL Mars Space Images - Featured Image

#Use splinter to navigate the site and find the image url for the current Featured Mars Image and 
#assign the url string to a variable called featured_image_url.

# https://splinter.readthedocs.io/en/latest/drivers/chrome.html
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
#Use splinter to navigate the site and find the image url for the current Featured Mars Image and 
#assign the url string to a variable called featured_image_url.
    url_1 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url_1)
# HTML object
    html = browser.html
# Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')
# Retrieve all elements that contain images information
    images = soup.find_all('li', class_='slide')

#get one image information
# Use Beautiful Soup's find() method to navigate and retrieve attributes
    link = images[6].find('a')
    href = link['data-fancybox-href']
    image_title = link['data-title']
    featured_image_url  = 'https://www.jpl.nasa.gov' + href

# # Mars Weather

# URL of page to be scraped
    url_2 = 'https://twitter.com/marswxreport?lang=en'

# Retrieve page with the requests module
    response = requests.get(url_2)
# Create BeautifulSoup object; parse with 'lxml'
    soup_1 = BeautifulSoup(response.text, 'lxml')

# Visit the Mars Weather twitter account here and scrape the latest Mars weather tweet from the page. 
#Save the tweet text for the weather report as a variable called mars_weather.

    mars_weather = soup_1.find_all(class_ = "js-tweet-text-container")[0].text
# Mars Facts

#Use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
    url_3 = 'https://space-facts.com/mars/'
    tables = pd.read_html(url_3)
    df = tables[0]
    df.columns = ['Description', 'Value']
#Set description as index
    df.set_index('Description', inplace=True)
    html_table = df.to_html()


#You will need to click each of the links to the hemispheres in order to find the image url to the full 
#resolution image.
    url_4 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url_4)
# HTML object
    html = browser.html
# Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')
# Retrieve all webpages that contain 4 images  information
    webpages = soup.find_all( class_='item')
    page_link = []
    for webpage in webpages:
        link = webpage.find('a')
        href = link['href']
        webpage_url  = 'https://astrogeology.usgs.gov' + href
        page_link.append(webpage_url)

# get the image from urls got from last section
    hemisphere_image_urls =[]
    for link in page_link:
        browser.visit(link)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        download = soup.find_all(class_ = "downloads")
        list_download = download[0].find('li')
        link_list_download= list_download.find('a')
        image_url = link_list_download['href']
        title = soup.find_all('h2',class_='title')[0].text
        image_dict = {"title":title, "img_url":image_url}
        hemisphere_image_urls.append(image_dict)
        
    scrape_mars = {"news_title":news_title,"news_p":news_p,"featured_image_url":featured_image_url,"mars_weather":mars_weather,
                   "html_table":html_table,"hemisphere_image_urls":hemisphere_image_urls}
    return scrape_mars
