from splinter import Browser
from bs4 import BeautifulSoup
import time


def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)


# In[8]:
def scrape():
    browser = init_browser()
    mars = {}

    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    time.sleep(1)

    html = browser.html
    news_soup = BeautifulSoup(html, 'html.parser')
    x = news_soup.find('div', class_='grid_layout')
    mars["news_title"] = x.find('a').get_text()
    mars["news_paragraph"] = x.find('div', class_='rollover_description_inner').get_text()

    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    time.sleep(1)

    full_image_elem = browser.find_by_id('full_image')
    full_image_elem.click()
    time.sleep(2)

    more_info_elem = browser.find_link_by_partial_text('more info')
    more_info_elem.click()
    time.sleep(2)

    html = browser.html
    img_soup = BeautifulSoup(html, 'html.parser')
    
    img_url_rel = img_soup.find('figure', class_='lede').find('img')['src']

    mars["featured_image"] = f'https://www.jpl.nasa.gov{img_url_rel}'

    
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    time.sleep(1)

    html = browser.html
    weather_soup = BeautifulSoup(html, 'html.parser')

    
    mars_weather_tweet = weather_soup.find('div', attrs={"class": "tweet", "data-name": "Mars Weather"})

    mars["weather"] = mars_weather_tweet.find('p', 'tweet-text').get_text()

    
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    time.sleep(1)

    
    hemisphere_image_urls = []

    
    links = browser.find_by_css("a.product-item")

    
    for i in range(len(links)):
        hemisphere = {}

        browser.find_by_css("a.product-item")[i].click()

        sample_elem = browser.find_link_by_text('Sample').first
        hemisphere['img_url'] = sample_elem['href']

        hemisphere['title'] = browser.find_by_css("h2.title").text

        hemisphere_image_urls.append(hemisphere)

        browser.back()
        time.sleep(1)

    mars["hemispheres"] = hemisphere_image_urls

    df = pd.read_html('http://space-facts.com/mars/')[0]
    df.columns = ['description', 'value']
    df.set_index('description', inplace=True)

    table = df.to_html()
    table = table.replace('\n', '')

    mars['facts'] = table

    browser.quit()

    return mars


