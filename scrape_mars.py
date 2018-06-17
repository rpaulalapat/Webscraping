
def scrape():
	# Dependencies
	from bs4 import BeautifulSoup
	import requests
	
	results_dict ={}
	
	#scrape news from Mars news portal
	url = "https://mars.nasa.gov/news"
	response = requests.get(url)
	soup = BeautifulSoup(response.text, 'html.parser')
	news_title = soup.find('div', class_='content_title').a.text
	news_p = soup.find('div', class_="rollover_description_inner").text
	results_dict['news_title'] = news_title
	results_dict['news_p'] = news_p
	
	#scrape image from JPL Mars Space Images - Featured Image
	from splinter import Browser
	executable_path = {'executable_path': 'C:/Users/rpaul/Software/chromedriver.exe'}
	browser = Browser('chrome', **executable_path, headless=False)
	url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
	browser.visit(url)
	html = browser.html
	soup = BeautifulSoup(html, 'html.parser')
	#go to FULL IMAGE page
	browser.click_link_by_partial_text('FULL IMAGE')
	html = browser.html
	soup = BeautifulSoup(html, 'html.parser')
	result = soup.find('a', class_ = "button fancybox")
	featured_image_url = 'https://www.jpl.nasa.gov/'+ result['data-fancybox-href']
	results_dict["featured_image"] = featured_image_url

	#scrape mars weather from twitter page for mars
	url = "https://twitter.com/marswxreport?lang=en"
	response = requests.get(url)
	soup = BeautifulSoup(response.text, 'html.parser')
	latest_tweet_container = soup.find('div', class_="js-tweet-text-container")
	mars_weather = latest_tweet_container.p.text
	mars_weather = mars_weather.split('@')[0]
	results_dict['mars_weather'] = mars_weather

	#get mars profile data and display as HTML table
	import pandas as pd
	url = 'https://space-facts.com/mars/'
	tables = pd.read_html(url)
	marsprofile_df = tables[0]
	marsprofile_df.columns = ['Attribute','Value']
	html_table = marsprofile_df.to_html(index=False)
	html_table.replace('\n', '')
	results_dict['mars_profile_table'] = html_table

	#get all the hemisphere images
	main_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
	hemispheres = ['Cerberus Hemisphere Enhanced', 'Schiaparelli Hemisphere Enhanced',
               'Syrtis Major Hemisphere Enhanced', 'Valles Marineris Hemisphere Enhanced']
	hemisphere_image_urls = []
	for hem in hemispheres:
    		hem_image_data = {}
    		browser.visit(main_url)
    		browser.click_link_by_partial_text(hem)
    		hem_html = browser.html
    		soup = BeautifulSoup(hem_html, 'html.parser')
    		image_url = soup.select_one("div.downloads").ul.li.a['href']
    		hem_image_data = {
            				'title': hem,
            				'img_url': image_url
            			}
    		hemisphere_image_urls.append(hem_image_data)
			
	results_dict['hemisphere_image_urls'] = hemisphere_image_urls

	return results_dict




	