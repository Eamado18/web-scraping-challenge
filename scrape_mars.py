
from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
import requests

def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=False)

def scrape(): # NASA Mars News
    browser = init_browser()
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
   
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    elem_slide = soup.select_one('div.list_text')

    news_title = [x.get_text() for x in elem_slide.find_all('div', class_='content_title')]
    news_p = [x.get_text() for x in elem_slide.find_all('div', class_='article_teaser_body')]


# ## JPL Mars Space Images - Featured Image
  
    url = "https://spaceimages-mars.com"
    browser.visit(url)

    full_image = browser.find_by_tag('button')[1]
    full_image.click()

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    url_img = soup.find("img", class_="fancybox-image")["src"]

    featured_image_url = f'https://spaceimages-mars.com/{url_img}'

# ## Mars Facts  
    url = "https://galaxyfacts-mars.com"

    mars_tables = pd.read_html(url)
    mars_facts = mars_tables[0]
    mars_facts.head()

    mars_facts.columns=['Description', 'Mars', 'Earth']
    mars_facts.set_index('Description', inplace=True)

    mars_facts.to_html()


# ## Mars Hemispheres

    url = 'https://marshemispheres.com'
    browser.visit(url)
    html = browser.html  

    soup = BeautifulSoup(html,'html.parser')
    hemispheres = soup.find_all("div", class_="item")

    hemisphere_image_urls = []

    for x in hemispheres:
        title = x.find("h3").text
        hemispheres_img = x.find("a", class_="itemLink product-item")["href"]
    
        browser.visit(url + "/" + hemispheres_img)
    
        html = browser.html
        web_info = BeautifulSoup(html, "html.parser")
    
        img_url = url + web_info.find("img", class_="wide-image")["src"]
    
        hemisphere_image_urls.append({"title" : title, "img_url" : img_url})

    Mars_info = {
      "News_mars": {
          "Title": news_title,
          "P": news_p
      }, 
      "Img_mars": featured_image_url,
      "Mars_facts": mars_facts,
      "Mars_Hemisphere": hemisphere_image_urls,
    }
    browser.quit()

    return Mars_info

