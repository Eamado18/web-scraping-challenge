#!/usr/bin/env python
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager


# In[2]:


executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# In[ ]:


url = 'https://mars.nasa.gov/news/'
browser.visit(url)


# ## NASA Mars News

# In[ ]:


html = browser.html
soup = BeautifulSoup(html, "html.parser")
elem_slide = soup.select_one('div.list_text')


# In[ ]:


news_title = elem_slide.find('div', class_='content_title').get_text()
news_title


# In[ ]:


news_p = elem_slide.find('div', class_='article_teaser_body').get_text()
news_p 


# ## JPL Mars Space Images - Featured Image

# In[ ]:


url = "https://spaceimages-mars.com"
browser.visit(url)


# In[ ]:


full_image = browser.find_by_tag('button')[1]
full_image.click()


# In[ ]:


html = browser.html
soup = BeautifulSoup(html, 'html.parser')


# In[ ]:


url_img = soup.find("img", class_="fancybox-image")["src"]
url_img


# In[ ]:


featured_image_url = f'https://spaceimages-mars.com/{url_img}'
featured_image_url


# ## Mars Facts

# In[ ]:


url = "https://galaxyfacts-mars.com"


# In[ ]:


mars_tables = pd.read_html(url)
mars_facts = mars_tables[0]
mars_facts.head()


# In[ ]:


mars_facts.columns=['Description', 'Mars', 'Earth']
mars_facts.set_index('Description', inplace=True)
mars_facts


# In[ ]:


mars_facts.to_html()


# ## Mars Hemispheres

# In[3]:


url = 'https://marshemispheres.com'
browser.visit(url)
html = browser.html


# In[4]:


soup = BeautifulSoup(html,'html.parser')
hemispheres = soup.find_all("div", class_="item")


# In[7]:


hemisphere_image_urls = []

for x in hemispheres:
    title = x.find("h3").text
    hemispheres_img = x.find("a", class_="itemLink product-item")["href"]
    
    browser.visit(url + "/" + hemispheres_img)
    
    html = browser.html
    web_info = BeautifulSoup(html, "html.parser")
    
    img_url = url + web_info.find("img", class_="wide-image")["src"]
    
    hemisphere_image_urls.append({"title" : title, "img_url" : img_url})

    print("")
    print(title)
    print(img_url)

