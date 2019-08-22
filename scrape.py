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


headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0"}

def scanAndScrape():
	query = input("Scan Barcode: ")
	type(query)

	if query == "":
		return

	PriceChartingURL = 'https://www.pricecharting.com/search-products?type=videogames&q='+ str(query)
	response = requests.get(PriceChartingURL, headers=headers)
	html = response.content

	PriceChartingsoup = BeautifulSoup(html, features="html.parser")
	genre = PriceChartingsoup.find('td', attrs={'itemprop': 'genre'})
	if genre is not None:
		genre = genre.text.strip()
		loose_price = PriceChartingsoup.find('td', attrs={'id': 'used_price'}).text.strip()
		cib_price = PriceChartingsoup.find('td', attrs={'id': 'complete_price'}).text.strip()
		nib_price = PriceChartingsoup.find('td', attrs={'id': 'new_price'}).text.strip()
		GameStopURL = PriceChartingsoup.find('a', attrs={'data-affiliate': 'GameStop'})
		if GameStopURL is not None:
			GameStopURL = GameStopURL["href"].split("%2F")[-1]
			GS_PIDLength=len(GameStopURL)
			if GS_PIDLength is 6:
				GameStopURL = '10'+ str(GameStopURL)
			elif GS_PIDLength is 5:
				GameStopURL = '100'+ str(GameStopURL)
			GS_PIDLength=len(GameStopURL)
		title = PriceChartingsoup.find("meta", attrs={'itemprop': 'name'})
		title = title["content"]
		platform = PriceChartingsoup.find("meta", attrs={'itemprop': 'gamePlatform'})
		platform = platform["content"]
		if GameStopURL is not None and GS_PIDLength is 8:
			GameStopTradeURL = 'https://www.gamestop.com/trade/details/?pid='+ str(GameStopURL)
			GS_Response = requests.get(GameStopTradeURL, headers=headers)
			GS_html = GS_Response.content
			GameStopsoup = BeautifulSoup(GS_html, features="html.parser")
			gs_name = GameStopsoup.find('h1', attrs={'class': 'product-name h2'}).text.strip()
			gs_trade = GameStopsoup.select("#trade-values-1 > div > div.grid-i1.col-sm-6.col-12 > ul > li:nth-of-type(2) > div.pull-right > span")
			gs_trade = gs_trade[0].text.strip()
		else:
			gs_name = "N/A"
			gs_trade = "N/A"
			GameStopURL = "N/A"
		print(title,platform,query,genre,loose_price,cib_price,nib_price,gs_name,GameStopURL,gs_trade)
		print("")
		GameData = ["=\"" + query + "\"",title,platform,genre,loose_price,cib_price,nib_price,gs_name,GameStopURL,gs_trade]


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
