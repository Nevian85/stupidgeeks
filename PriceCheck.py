import csv
import requests
from bs4 import BeautifulSoup
import os
import mysql.connector
from datetime import date
from datetime import datetime

vgdb = mysql.connector.connect(
  host="**.**.**.**",
  user="********",
  passwd="********",
  database="videogames"
)

os.system('cls')  # For Windows
os.system('clear')  # For Linux/OS X

print("###################################")
print("#                                 #")
print("#   Stupid Geeks Price Check      #")
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
	query = input("Scan QRcode: ")
	type(query)
	
	if query == "":
		return
	
	querycursor = vgdb.cursor()
	
	querysql = "SELECT * FROM inventory WHERE SKU=%s"
	qSKU = (str(query),)
	querycursor.execute(querysql, qSKU)
	queryresult = querycursor.fetchall()

	for data in queryresult:
		gencursor = vgdb.cursor()
		genericsql = "SELECT * FROM genericvideogamedata WHERE id=%s"
		sku = data[0]
		gid = data[1]
		pid = (gid,)
		gencursor.execute(genericsql, pid)
		genresult = gencursor.fetchall()
		for genQ in genresult:
			platform = genQ[1]
			consoleID = genQ[2]
			title = genQ[3]
			loose_price = genQ[4]
			cib_price = genQ[5]
			nib_price = genQ[6]
			upc = genQ[7]
			genre = genQ[8]
			releasedate = genQ[9]
			releaseyear = datetime.strptime(releasedate, '%m/%d/%Y')
			codeID = genQ[10]
			description = genQ[11]
			developer = genQ[12]
			publisher = genQ[13]
			LastDatePriceUpdate = genQ[14]

		today = date.today()
		uday = today.strftime("%m/%d/%Y")
		if LastDatePriceUpdate != uday:
			pc_url = 'https://www.pricecharting.com/game/'+str(gid)
			pc_soup = loadSoup(pc_url)
			genre = pc_soup.find('td', attrs={'itemprop': 'genre'})
			if genre is not None:
				genre = genre.text.strip()
				loose_price = pc_soup.find('td', attrs={'id': 'used_price'}).text.strip()
				cib_price = pc_soup.find('td', attrs={'id': 'complete_price'}).text.strip()
				nib_price = pc_soup.find('td', attrs={'id': 'new_price'}).text.strip()
			updatesql = "UPDATE genericvideogamedata SET `loose-price`=%s, `cib-price`=%s, `new-price`=%s, `LastDatePriceUpdate`=%s WHERE id=%s"
			updateid=(loose_price.replace("$",""),cib_price.replace("$",""),nib_price.replace("$",""),uday,gid)
			gencursor.execute(updatesql, updateid)
			vgdb.commit()
			print(gencursor.rowcount, "record/s updated")
		print("")
		print("")
		print("")
		print("")
		print("")
		print("")
		print(str(title)+" ("+str(platform)+", "+str(releaseyear.strftime("%Y"))+") - "+str(genre)+" - "+str(codeID))
		print("")
		print("Title: "+str(title))
		print("System: "+str(platform))
		print("Genre: "+str(genre))
		print("Release Date: "+str(releasedate))
		print("Developer: "+str(developer))
		print("Publisher: "+str(publisher))
		print("CodeID: "+str(codeID))
		print("")
		print("--------------------")
		print("")
		print("Description:")
		print(str(description)+"")
		print("")
		print("")
		print("Recommended Loose Price: "+str(loose_price))
		print("Recommended CIB Price: "+str(cib_price))
		print("Recommended New Price: "+str(nib_price))
		print("")
		print("UPC: "+str(upc))
		print("")
		print("SKU: "+str.upper(sku))
		print("")
		print("")
		print("Press enter to exit")
		print("")
	scanAndScrape()

# Initializes the script
scanAndScrape()
