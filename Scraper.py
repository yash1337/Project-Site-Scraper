import requests 
from bs4 import BeautifulSoup #getting the beasutiful soup library
from requests.auth import HTTPBasicAuth
from urllib.parse import urljoin
import os
import msvcrt as m


################################################
baseURL=""
USERNAME=""
PASSWORD=""
################################################

#installing the BeautifulSoup and requests modules
os.system('pip install beautifulsoup4')
os.system('pip install requests')
print()
#getting the HTML file using the request object
requestObject=requests.get(baseURL,auth=HTTPBasicAuth(USERNAME,PASSWORD)) 

#"Beautifying" the HTML file using the html parser
soup=BeautifulSoup(requestObject.text,"html.parser")	

#variables to hold the links
links=[]
small_link=[]

#getting all the <a> HTML tags
for link in soup.find_all('a'):
	small_link.append(link['href'])			#getting the link without the base URL
	links.append(urljoin(baseURL,link['href']))   #joining the base and the relative URL 
	
#getting the links that we are intrested in i.e. .txt .pdf and .cpp
correctRelativeURL=[]
correctCompletedURL=[]
for item in small_link:
	if (".txt" in item or ".pdf" in item or ".cpp" in item):
		correctRelativeURL.append(item)
		
for item in links:
	if (".txt" in item or ".pdf" in item or ".cpp" in item):
		correctCompletedURL.append(item)

#looping through the links, downloading files
for link in correctCompletedURL:
	book_name = link.split('/')[-1]
	print("Downloading: "+book_name+" ...")
	with open(book_name, 'wb') as book:
		a = requests.get(link,auth=HTTPBasicAuth(USERNAME,PASSWORD))
		for block in a.iter_content(512):
			if not block:
				break
			book.write(block)

	
#These lines delete the scraper file. Uncomment them if you don't want the file to be deleted			
#os.remove('Scaper.py')
#print("Scraper File Removed!!!!")
print("\nPress a key to continue...")
m.getch()