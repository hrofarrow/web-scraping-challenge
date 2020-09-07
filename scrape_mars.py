# Dependencies
from bs4 import BeautifulSoup
import requests
import os
from splinter import Browser
import pandas as pd


def init_browser():
    executable_path = {"executable_path": "C:\chromedriver_win32\chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()
    mars_facts_data = {}

    # url of page to be scraped
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"

    # Retrieve page with requests module
    response = requests.get(url)

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(response.text, 'html.parser')

    print(soup.prettify())

    # Look for news titles
    news_title = soup.find('div', class_="content_title").text
    news_title

    # find paragraph descriptions
    news_p = soup.find('div', class_='rollover_description_inner').text
    news_p

    # Use splinter to navigate the site and find the image url for the current Featured Mars
    # Image and assign the url string to a variable called featured_image_url.

    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    # print(soup.prettify())
    image_url = soup.find('img', class_="fancybox-image")["src"]
    featured_image_url = "https://www.jpl.nasa.gov" + image_url
    featured_image_url

    # Visit the Mars Facts webpage here and use Pandas to scrape the table containing facts
    # about the planet including Diameter, Mass, etc.

    url = "https://space-facts.com/mars/"

    mars_table = pd.read_html(url)
    mars_table

    # Visit the USGS Astrogeology site here to obtain high resolution images for each of Mar's hemispheres.
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    hemisphere_image_urls = []

    for x in range(4):
        images = browser.find_by_tag('h3')
        images[x].click()
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        image_url_end = soup.find("img", class_="wide-image")["src"]
        title = soup.find("h2", class_="title").text
        img_url = 'https://astrogeology.usgs.gov' + image_url_end
        image_dict = {"title": title, "img_url": img_url}
        hemisphere_image_urls.append(image_dict)
        browser.back()

    hemisphere_image_urls

    return mars_facts_data
3