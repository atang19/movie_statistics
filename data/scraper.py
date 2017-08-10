"""
Author: Andy Tang
Email: andy.tang62@gmail.com

IMDB Web Scraper
"""

import requests
from BeautifulSoup import BeautifulSoup
import csv

def append_data(url, overall_list):
	response = requests.get(url)
	html = response.content
	soup = BeautifulSoup(html)
	main_list = soup.find('div', attrs={'class': 'lister-list'})

	for row in main_list.findAll('div', attrs={'class': 'lister-item mode-advanced'}):
		good_stuff = row.find('div', attrs={'class': 'lister-item-content'})
		movie_title = good_stuff.find('a').text
		movie_year = good_stuff.find('span', attrs={'class': 'lister-item-year text-muted unbold'}).text
		if good_stuff.find('span', attrs={'class': 'certificate'}) != None:
			certificate = good_stuff.find('span', attrs={'class': 'certificate'}).text
		else:
			certificate = 'NR'
		runtime = good_stuff.find('span', attrs={'class': 'runtime'}).text
		rating_bar = good_stuff.find('div', attrs={'class': 'ratings-bar'})
		imdb_rating = rating_bar.find('strong').text

		paragraphs = good_stuff.findAll('p')
		people_inv = paragraphs[2].findAll('a')
		director = people_inv[0].text
		actors_a = people_inv[1:]
		actors = []
		for actor in actors_a:
			actors.append(actor.text.encode('utf-8'))
		gross = good_stuff.findAll('span', attrs={'name': 'nv'})[1].text
		data_point = [movie_title.encode('utf-8'), movie_year.encode('utf-8'), certificate.encode('utf-8'), runtime.encode('utf-8'), gross.encode('utf-8'), imdb_rating.encode('utf-8'), director.encode('utf-8')]
		data_point.extend(actors)

		overall_list.append(data_point)

	return overall_list


if __name__ == "__main__":
	filename = 'data'
	my_list = []
	for i in range(1990, 2017):
		url = 'http://www.imdb.com/search/title?year={},{}&title_type=feature&sort=boxoffice_gross_us,desc'.format(str(i), str(i))
		my_list = append_data(url, my_list)
	with open(filename, 'wb') as myfile:
		    wr = csv.writer(myfile)
		    for datapoint in my_list:
		    	wr.writerow(datapoint)

