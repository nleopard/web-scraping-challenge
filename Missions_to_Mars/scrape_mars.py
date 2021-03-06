from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import time
import lxml



def init_browser():
    # Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": 'chromedriver'}
    return Browser("chrome", **executable_path, headless=False)


def scrape():

    # # NASA Mars News

    browser = init_browser()

    #assign url to variable
    url = "https://mars.nasa.gov/news/"

    #pull up the website to pull information
    browser.visit(url)

    #read the html website
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")


    article = soup.find("li", class_='slide')

    news_title = article.find("div", attrs = {"class":"content_title"}).text

    news_p = article.find("div", class_ ="article_teaser_body").text


    print(news_title)
    print(news_p)


    # # JPL Mars Space Images - Featured Image


    #assign url to variable
    mars_pic_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"

    #pull up the website to pull information
    browser.visit(mars_pic_url)

    #read the html website
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")


    image = soup.find("a", class_="button fancybox")["data-fancybox-href"]

    featured_image_url = "https://www.jpl.nasa.gov" + image

    #print(featured_image_url)

#############################################################################################

    # # Mars Weather


    #save the mars twitter website in a variable
    mars_twitter_url = "https://twitter.com/marswxreport?lang=en"
        
    #pull up the website to pull information
    browser.visit(mars_twitter_url)
    time.sleep(1)

    #read the html website
    html_twitter = browser.html
    soup = BeautifulSoup(html_twitter, "html.parser")


    #work through the different sections to find our tweet

    main = soup.find("main", attrs = {"role":"main","class":"css-1dbjc4n r-16y2uox r-1wbh5a2"})

    div = main.find("div", attrs = {"class":"css-1dbjc4n r-14lw9ot r-1tlfku8 r-1ljd8xs r-13l2t4g r-1phboty r-1jgb5lz r-1ye8kvj r-13qz1uu r-184en5c"})

    article = div.find("article", attrs = {"role":"article","class":"css-1dbjc4n r-1loqt21 r-16y2uox r-1wbh5a2 r-1ny4l3l r-1udh08x r-1j3t67a r-o7ynqc r-6416eg"})

    div_2 = article.find("div", attrs = {"dir":"auto","class":"css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0"})

    mars_weather = div_2.find("span", attrs = {"class":"css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0"}).text

    #print(mars_weather)

##################################################################################################

    # # Mars Facts



    # Visit Mars facts url 
    facts_url = 'http://space-facts.com/mars/'

    # Use Panda's `read_html` to parse the url
    mars_facts = pd.read_html(facts_url)

    # Find the mars facts DataFrame in the list of DataFrames as assign it to `mars_df`
    mars_df = mars_facts[0]

    # Assign the columns `['Description', 'Value']`
    mars_df.columns = ['Description','Value']

    # Set the index to the `Description` column without row indexing
    mars_df.set_index('Description', inplace=True)

    # Save html code to folder Assets
    data = mars_df.to_html()



    # # Mars Hemispheres



    #save the mars twitter website in a variable
    mars_hemisphere_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
        
    #pull up the website to pull information
    browser.visit(mars_hemisphere_url)
    time.sleep(1)

    #read the html website
    html_mars_hemisphere = browser.html
    soup = BeautifulSoup(html_mars_hemisphere, "html.parser")



    #search through the main div to grab the four images and titles
    div = soup.find_all('div', class_ = 'item')

    #create empty dictionary
    hemisphere_image_urls = []

    #create main url, to add the img url to
    main_url = 'https://astrogeology.usgs.gov'



    #loop through the four hemispheres and store the title and img url

    for x in div:
        #find the title
        title = x.find('h3').text
        
        #get the link to the full image
        partial_url = x.find('a', class_ = "itemLink product-item")["href"]
        
        #pull up the website to pull information
        browser.visit(main_url + partial_url)
        
        #read the html website
        partial_url = browser.html
        
        #parse it
        soup = BeautifulSoup(partial_url, "html.parser")
        
        #get the full image link
        img_url = main_url + soup.find('img', class_ = "wide-image")["src"]
        
        #append it to the empty dictionary hemisphere_image_urls
        hemisphere_image_urls.append({'title': title, "img_url": img_url})
        

    #disply the dictionary
    hemisphere_image_urls



    # Create empty dictionary for all Mars Data.
    mars_facts_data = {
     
    }

    # Append news_title and news_paragraph to mars_data.
    mars_facts_data['news_title'] = news_title
    mars_facts_data['news_p'] = news_p

    # Append featured_image_url to mars_data.
    mars_facts_data['featured_image_url'] = featured_image_url

    # Append mars_weather to mars_data.
    mars_facts_data['mars_weather'] = mars_weather

    # Append mars_facts to mars_data.
    mars_facts_data['mars_facts'] = data

    # Append hemisphere_image_urls to mars_data.
    mars_facts_data['hemisphere_image_urls'] = hemisphere_image_urls

    return mars_facts_data