import pandas as pd
from bs4 import BeautifulSoup as bs4
import requests
import os
from splinter import Browser

def scrape():

    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

    news_title, news_p = mars_news(browser)

    data={
        "news_title": news_title, 
        "news_paragraph": news_p,
        "featured_image": mars_images(browser),
        "mars_weather": mars_weather(browser),
        "mars_facts": mars_facts(),
        "mars_hemi" : mars_hemi(browser)
    }
    browser.quit()
    return data

def mars_news(browser):
    # URL of page to be scraped
    mars_url = 'https://mars.nasa.gov/news/'
    browser.visit(mars_url)
    
    # Create HTML object
    html = browser.html

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = bs4(html, 'html.parser')
    # type(soup)

    # Assign news_title and news_paragraph variables to reference later 
    news_title = soup.find('div', class_='content_title').text
    news_p = soup.find('div', class_='article_teaser_body').text
    
    # Print featured_image_url link
    return news_title, news_p

def mars_images(browser):
    # URL of page to be scraped

    image_url_featured = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(image_url_featured)

    # Create HTML object
    image_html = browser.html

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = bs4(image_html, 'html.parser')
            
    # Retrieve background_image
    featured_image_url = soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]
    
    # Define anchor url 
    anchor_url = 'https://www.jpl.nasa.gov'

    # Create featured_image_url
    featured_image_url = anchor_url + featured_image_url

    # Print featured_image_url link
    return featured_image_url

def mars_weather(browser):
    # URL of page to be scraped
    twitter_weather_url = 'https://twitter.com/marswxreport?lang=en'
    result = requests.get(twitter_weather_url)

    # Create HTML object
    twitter_weather_html = result.text

    # Create BeautifulSoup object; parse with 'html.parser'
    twitter_weather_soup = bs4(twitter_weather_html, 'html.parser')

    twitter_mars_weather = twitter_weather_soup.find(class_='tweet-text').get_text()

    # Print weather tweet
    return twitter_mars_weather

def mars_facts():

    # Visit the Mars Facts webpage
    mars_facts_url = 'http://space-facts.com/mars/'

    # Use Pandas to scrape the table containing facts about the planet
    mars_facts = pd.read_html(mars_facts_url)
    #print(mars_facts)

    # Create dataframe
    mars_space_facts_df = mars_facts[0]
    #print(mars_space_facts_df)

    # Assign columns
    mars_space_facts_df.columns = ['Description','Value']

    # Remove indexing
    mars_space_facts_df.set_index('Description', inplace=True)

    # Display mars_df
    mars_space_facts_df

    # convert the data to HTML
    return mars_space_facts_df.to_html()

def mars_hemi(browser):
    hemi_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemi_url)

    # Create HTML object
    hemi_html = browser.html

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = bs4(hemi_html, 'html.parser')

    # Create HTML Object
    html_hemispheres = browser.html

    # Parse HTML with Beautiful Soup
    soup = bs4(html_hemispheres, 'html.parser')

    # Retrieve items that contain hemisphere info
    items = soup.find_all('div', class_='item')

    # Create empty list for hemisphere urls
    hemisphere_image_urls = []

    # Define anchor url 
    hemisphere_anchor_url = 'https://astrogeology.usgs.gov'

    # Loop through the items previously stored
    for i in items: 
        # Store title
        title = i.find('h3').text
        
        # Store link appendage for full image link
        append_img_url = i.find('a', class_='itemLink product-item')['href']
        
        # Visit full image website 
        browser.visit(hemisphere_anchor_url + append_img_url)
        
        # Create HTML object of individual hemisphere information website 
        append_img_html = browser.html
        
        # Parse HTML with Beautiful Soup for every individual hemisphere information website 
        soup = bs4(append_img_html, 'html.parser')
        
        # Build full image url 
        img_url = hemisphere_anchor_url + soup.find('img', class_='wide-image')['src']
        
        # Append to a list of dictionaries 
        hemisphere_image_urls.append({"title" : title, "img_url" : img_url})       

    # Display hemisphere_image_urls
    return hemisphere_image_urls