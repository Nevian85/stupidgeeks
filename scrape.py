import csv
import requests
from bs4 import BeautifulSoup
import os

os.system('cls')  # For Windows
os.system('clear')  # For Linux/OS X

print("###################################")
print("#                                 #")
print("#   Stupid Geeks Scan N' Scrape   #")
print("#                                 #")
print("###################################")
print("")
print("Press enter to exit")
print("")



def loadSoup(target_url):
	headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0"}
	response = requests.get(target_url, headers=headers)
	html = response.content

	return BeautifulSoup(html, features="html.parser")

def scanAndScrape():
	query = input("Scan Barcode: ")
	type(query)

	if query == "":
		return

	pc_url = 'https://www.pricecharting.com/search-products?type=videogames&q='+ str(query)
	pc_soup = loadSoup(pc_url)
	genre = pc_soup.find('td', attrs={'itemprop': 'genre'})
	if genre is not None:
		genre = genre.text.strip()
		loose_price = pc_soup.find('td', attrs={'id': 'used_price'}).text.strip()
		cib_price = pc_soup.find('td', attrs={'id': 'complete_price'}).text.strip()
		nib_price = pc_soup.find('td', attrs={'id': 'new_price'}).text.strip()
		gs_url = pc_soup.find('a', attrs={'data-affiliate': 'GameStop'})
		title = pc_soup.find("meta", attrs={'itemprop': 'name'})
		title = title["content"]
		platform = pc_soup.find("meta", attrs={'itemprop': 'gamePlatform'})
		platform = platform["content"]

		if gs_url is not None:
			gs_pid = gs_url["href"].split("%2F")[-1]
			if len(gs_pid) is 8:
				formatted_gs_pid = gs_pid
			else:
				formatted_gs_pid = f'1{gs_pid:0>7}'

		if gs_url is not None and len(formatted_gs_pid) is 8:
			gs_trade_url = 'https://www.gamestop.com/trade/details/?pid='+ str(formatted_gs_pid)
			gs_soup = loadSoup(gs_trade_url)
			print(gs_soup)
			print(gs_trade_url)
			gs_name = gs_soup.find('h1', attrs={'class': 'product-name h2'}).text.strip()
			gs_trade = gs_soup.select("#trade-values-1 > div > div.grid-i1.col-sm-6.col-12 > ul > li:nth-of-type(2) > div.pull-right > span")
			gs_trade = gs_trade[0].text.strip()
		else:
			gs_name = "N/A"
			gs_trade = "N/A"
			gs_url = "N/A"

		print(title,platform,query,genre,loose_price,cib_price,nib_price,gs_name,formatted_gs_pid,gs_trade)
		print("")
		GameData = ["=\"" + query + "\"",title,platform,genre,loose_price,cib_price,nib_price,gs_name,formatted_gs_pid,gs_trade]

		outfile = open("./games.csv", "a", newline='')
		writer = csv.writer(outfile)
		writer.writerow(GameData)
	else:
		print("Unknown UPC")
		outfile = open("./games.csv", "a", newline='')
		writer = csv.writer(outfile)
		writer.writerow(["Uknown UPC"])
	scanAndScrape()

# Initializes the script
scanAndScrape()
