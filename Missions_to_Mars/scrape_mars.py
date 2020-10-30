from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
from bs4 import BeautifulSoup
import requests
import pandas as pd



# def init_browser():
#     executable_path = {'executable_path': 'chromedriver.exe'}
#     return Browser('chrome', **executable_path, headless=False)

def scrape():

    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    
    # browser = init_browser

### NASA Mars News
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    titles = soup.find_all('div', class_= "content_title")
    news_title = titles[1].text
    paragraphs = soup.find_all('div', class_= "article_teaser_body")
    news_paragraph = paragraphs[0].text
    
   
### JPL Mars Space Images - Featured Image
    url2 = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    home_main = "https://www.jpl.nasa.gov"
    browser.visit(url2)
    html2 = browser.html
    soup = BeautifulSoup(html2, 'html.parser')
    footer = soup.find('footer')
    full = home_main + footer.find('a')['data-link']
    browser.visit(full)

    html3 = browser.html
    soup = BeautifulSoup(html3, 'html.parser')
    figure = soup.find('figure', class_ = "lede")
    full_img = home_main + figure.find('a')['href']

### Mars Facts
    url3 = "https://space-facts.com/mars/"
    tables = pd.read_html(url3)
    table = tables[0]
    table.columns = ['', 'Mars']
    table.set_index('', inplace=True)
    html_table = table.to_html()

### Mars Hemispheres
    url4 = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    url_main = "https://astrogeology.usgs.gov"
    browser.visit(url4)

    hrefs = []
    links = []
    titles = []
    hemisphere_image_urls = []


    html4 = browser.html
    soup = BeautifulSoup(html4, 'html.parser')
    results = soup.find_all('div', class_ = "description")

    for result in results:
        hrefs.append(url_main + result.find('a')['href'])

    for href in hrefs:
        browser.visit(href)
        html5 = browser.html
        soup = BeautifulSoup(html5, 'html.parser')
        image = soup.find('li')
        header = soup.find('h2', class_ = 'title')
        titles.append(header.text)    
        links.append(image.find('a')['href'])
    
    for title, link in zip(titles, links):
        hemisphere_image_urls.append(dict([("title", title), ("img_url", link)]))
    
    html_dict = {}    
    html_dict['n_title'] = news_title
    html_dict['n_paragraph'] = news_paragraph
    html_dict['full_image'] = full_img
    html_dict['html_table'] = html_table
    html_dict['img_urls'] = hemisphere_image_urls

    browser.quit()
    
    return html_dict

        # html_dict.append(dict([("n_title",news_title), dict([("n_paragraph", news_paragraph)]), dict([("full_image",full_img)]), dict([("html_table", html_table)]), hemisphere_image_urls)
