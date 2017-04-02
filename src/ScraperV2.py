#############################
##Project Site 'Cyclone" Scraper v2
##This thing Scrapes everthing from the CSE 232 site Videos, Worksheets, Lecture Notes, and Project Files
##You need to supply your CSE user name and Password 
#############################

################################################################################################################

###Checking dependensies

import os
try:
	import requests 
	print ("Request library is good!! ")
	print()
except:
	print("Request Library not found. Trying to install it. If not successfull then try it manually")
	os.system('pip install requests')
	
try:
	print("Importing other libraries")
	from requests.auth import HTTPBasicAuth
	from urllib.parse import urljoin
	import msvcrt as m
	print()
except:
	print("Just get those libraries man!!!")

try:
	from bs4 import BeautifulSoup
	print("BeautifulSoup library is good!! ")
	print()
except:
	print("BeautifulSoup Library not found. Trying to install it. If not successfull then try it manually")
	os.system('pip install beautifulsoup4')
	
import re
import requests 
from bs4 import BeautifulSoup #getting the beasutiful soup library
from requests.auth import HTTPBasicAuth
from urllib.parse import urljoin
import sys
import msvcrt as m
import posixpath
import urllib.parse
	

################################################################################################################

################################################################################################################
UNAME=""
PASSWORD=""
################################################################################################################

################################################################################################################

###Actual Code

baseURL='http://www.cse.msu.edu/~cse232/'
basePath=os.path.dirname(os.path.abspath(__file__))

def returnBeautifiedObject(link,USERNAME='',PASS=''):
	requestObject=requests.get(link,auth=HTTPBasicAuth(USERNAME,PASS))
	return BeautifulSoup(requestObject.text,"html.parser")

def downloadFiles(URL,PATH,book_name=''):
	if book_name=='':
		book_name=URL.split('/')[-1]
		
	os.chdir(PATH)
	
	print("Downloading: "+book_name+" ...")
	with open(book_name, 'wb') as book:
		a = requests.get(URL,auth=HTTPBasicAuth(UNAME,PASSWORD))
		for block in a.iter_content(512):
			if not block:
				break
			book.write(block)
	
def subFolderFileDownloader(URL,folderPath):	
	tempBeautifiedObject=returnBeautifiedObject(URL,UNAME,PASSWORD)
	for link in tempBeautifiedObject.find_all('a'):
		if not os.path.exists(folderPath):
			os.makedirs(folderPath)
		if ".txt" in link['href'] or ".pdf" in link['href'] or ".cpp" in link['href'] or ".h" in link['href']:
			downloadFiles(URL+link['href'],folderPath)	
	
def getWorksheets(beautifiedBaseObject):
	worksheetURL=''
	worksheetFolderPath=os.path.dirname(os.path.abspath(__file__))+'\Worksheets'
	if not os.path.exists(worksheetFolderPath):
		os.makedirs(worksheetFolderPath)
	
	for link in beautifiedBaseObject.find_all('a'):
		if 'Worksheets' in urljoin(baseURL,link['href']):
			worksheetURL=urljoin(baseURL,link['href'])
	worksheetHTMLObject=requests.get(worksheetURL)
	completedWorksheetURL=''
	beautifiedWorksheetHTMLObject=BeautifulSoup(worksheetHTMLObject.text,"html.parser")	
	
	for link in beautifiedWorksheetHTMLObject.find_all('a',href=True):
		if (".pdf" in link['href'] or ".cpp" in link['href']):
			completedWorksheetURL=worksheetURL+'/'+link['href']
			book_name = completedWorksheetURL.split('/')[-1]
			book_name=book_name[:1]+'orksheet'+book_name[1:]
			worksheetName=book_name
			worksheetFilePath=worksheetFolderPath+"\\"+book_name.split('.',1)[0]	
			if not os.path.exists(worksheetFilePath):
				os.makedirs(worksheetFilePath)
			downloadFiles(completedWorksheetURL,worksheetFilePath,book_name)
	

def getLabs(beautifiedBaseObject):
	labBaseURLList=[]	
	labFolderpath=os.path.dirname(os.path.abspath(__file__))+'\Labs'
	if not os.path.exists(labFolderpath):
		os.makedirs(labFolderpath)  
	
	for link in beautifiedBaseObject.find_all('a'):
		if 'week' in link['href'] and '.pdf' not in link['href']:
			labBaseURLList.append(urljoin(baseURL,link['href']))
	labBaseURLList.pop(0)	#deleting the URL without week number
	tempBeautifiedObject=None
	beautifiedLabObject=None
	
	for URL in labBaseURLList:
		tempBeautifiedObject=returnBeautifiedObject(URL,UNAME,PASSWORD)
		for link in tempBeautifiedObject.find_all('a'):
			if ('lab' in link['href'] and 'Weekly' in link['href']):
				beautifiedLabObject=returnBeautifiedObject(link['href'],UNAME,PASSWORD)
				for labLink in beautifiedLabObject.find_all('a'):
					if (".pdf" in labLink['href'] or ".cpp" in labLink['href'] or ".h" in labLink['href'] or "gdbinit" in labLink['href'] or '.txt' in labLink['href']):
						labFileURL=link['href']+"/"+ labLink['href']
						if not os.path.exists(labFolderpath+"\\"+URL.split('/')[-2]):
							os.makedirs(labFolderpath+"\\"+URL.split('/')[-2])
						labFilePath=labFolderpath+"\\"+URL.split('/')[-2]
						downloadFiles(labFileURL,labFilePath)

						
def getReadings(beautifiedBaseObject):
	readingBaseURLList=[]
	readingFolderPath=os.path.dirname(os.path.abspath(__file__))+'\\Readings'
	if not os.path.exists(readingFolderPath):
		os.makedirs(readingFolderPath) 
		
	for link in beautifiedBaseObject.find_all('a'):
		if 'week' in link['href'] and '.pdf' not in link['href']:
			readingBaseURLList.append(urljoin(baseURL,link['href']))
	readingBaseURLList.pop(0)	#deleting the URL without week number
	tempBeautifiedObject=None
	beautifiedReadingObject=None
	
	for URL in readingBaseURLList:
		tempBeautifiedObject=returnBeautifiedObject(URL,UNAME,PASSWORD)
		for link in tempBeautifiedObject.find_all('a'):
			if ('reading' in link['href']):
				beautifiedReadingObject=returnBeautifiedObject(link['href'],UNAME,PASSWORD)
				for readingLink in beautifiedReadingObject.find_all('a'):
					if (".pdf" in readingLink['href'] or ".cpp" in readingLink['href'] or ".h" in readingLink['href'] or '.txt' in readingLink['href']):
						readingFileURL=link['href']+"/"+readingLink['href']
						if not os.path.exists(readingFolderPath+"\\"+URL.split('/')[-2]):
							os.makedirs(readingFolderPath+'\\'+URL.split('/')[-2])
						readingFilePath=readingFolderPath+'\\'+URL.split('/')[-2]
						downloadFiles(readingFileURL,readingFilePath)
						
						
def getVideos(beautifiedBaseObject):
	videoBaseURLList=[]
	videoFolderPath=os.path.dirname(os.path.abspath(__file__))+'\\Videos'
	if not os.path.exists(videoFolderPath):
		os.makedirs(videoFolderPath)
	
	for link in beautifiedBaseObject.find_all('a'):
		if 'week' in link['href'] and '.pdf' not in link['href']:
			videoBaseURLList.append(urljoin(baseURL,link['href']))
	videoBaseURLList.pop(0)	#deleting the URL without week number
	tempBeautifiedObject=None
	beautifiedVideoObject=None

	for URL in videoBaseURLList:
		tempBeautifiedObject=returnBeautifiedObject(URL,UNAME,PASSWORD)
		for liLink in tempBeautifiedObject.find_all('a'):
			if ('video' in liLink['href'] and '.mp4' in liLink['href']):
				temp=URL[:-URL.index('/')]
				if not os.path.exists(videoFolderPath+"\\"+URL.split('/')[-2]):
					os.makedirs(videoFolderPath+"\\"+URL.split('/')[-2])
				videoFilePath=videoFolderPath+"\\"+URL.split('/')[-2]
				videoFileURL=temp[:temp.rfind('/')]+"/"+liLink['href']
				bookName=liLink.text.strip()+".mp4"
				bookName=bookName.replace('\n','').replace('\t','')
				bookName=re.sub(' +',' ',bookName).capitalize()
				bookName=re.sub('[^a-zA-Z0-9 \n\.]', '', bookName)
				downloadFiles(videoFileURL,videoFilePath,bookName)
				print()
			
			
def getProjects(beautifiedBaseObject):
	projectBaseURLList=[]
	projectFolderPath=os.path.dirname(os.path.abspath(__file__))+'\\Projects'
	if not os.path.exists(projectFolderPath):
		os.makedirs(projectFolderPath)
	
	for link in beautifiedBaseObject.find_all('a'):
		if 'week' in link['href'] and '.pdf' not in link['href']:
			projectBaseURLList.append(urljoin(baseURL,link['href']))
	projectBaseURLList.pop(0)	#deleting the URL without week number
	tempBeautifiedObject=None
	beautifiedProjectObject=None
	
	for URL in projectBaseURLList:
		tempBeautifiedObject=returnBeautifiedObject(URL,UNAME,PASSWORD)
		for projectBaseLink in tempBeautifiedObject.find_all('a'):
			if 'project' in projectBaseLink['href'] and 'pdf' not in projectBaseLink['href']:
				projectBeautifiedObject=returnBeautifiedObject(projectBaseLink['href'],UNAME,PASSWORD)
				for link in projectBeautifiedObject.find_all('a'):
					if ".txt" in link['href'] or ".pdf" in link['href'] or ".cpp" in link['href'] or ".h" in link['href']:
						if not os.path.exists(projectFolderPath+"\\"+URL.split('/')[-2]):
							os.makedirs(projectFolderPath+"\\"+URL.split('/')[-2])
						projectFilePath=projectFolderPath+"\\"+URL.split('/')[-2]
						projectFileURL=projectBaseLink['href']+"/"+link['href']
						downloadFiles(projectFileURL,projectFilePath)
					if 'test' in link['href']:  #for getting the test files
						if not os.path.exists(projectFolderPath+"\\"+URL.split('/')[-2]+"\\"+"tests"):
							os.makedirs(projectFolderPath+"\\"+URL.split('/')[-2]+"\\"+"tests")
						testFilePath=projectFolderPath+"\\"+URL.split('/')[-2]+"\\"+"tests"
						testFileURL=projectBaseLink['href']+"/"+link['href']
						print()
						subFolderFileDownloader(testFileURL,testFilePath)
				print()
					
def menu():
	print("The list of choices are as follows. Choose the ones you like one by one. Don't worry you will get future chances (just as in life!!): \n")
	print("1. All the worksheets!\n")
	print("2. All the Lab files!\n")
	print("3. All the Lecture slides!\n")
	print("4. All the videos! (be carefull the total size is over 8 gigs!)\n")
	print("5. All the Project Files!\n")
	print("q. Nothing fam. Just get me out of here!\n")
	
def main():
	print("Welcome to CSE232 Scraper!!!!!!\n")
	menu()	
	userInput=(input("So what do you want (not in life. What do you want right now!!!): "))
	print()
	beautifiedBaseObject=returnBeautifiedObject(baseURL)
	while(True):
		if(userInput=='1'):
			print("Alright lets get those worksheets!!!\n")
			getWorksheets(beautifiedBaseObject)
			os.chdir(basePath)
			print()
			print('Alright the worsksheets are downloaded in the \"Worksheets\" folder. See if you want anything else!\n' )
			menu()
			userInput=(input("Do you need anything else????: "))
			print('\n\n')
		elif(userInput=='2'):
			print("Alright lets get those lab files!!!\n")
			getLabs(beautifiedBaseObject)
			os.chdir(basePath)
			print()
			print('Alright the Lab Files are downloaded in the \"Labs\" folder. See if you want anything else!\n' )
			menu()
			userInput=(input("Do you need anything else????: "))
			print('\n\n')
		elif(userInput=='3'):
			print("Alright lets get those lecture slides!!!\n")
			getReadings(beautifiedBaseObject)
			os.chdir(basePath)
			print()
			print('Alright the Leture Notes are downloaded in the \"Readings\" folder. See if you want anything else!\n' )
			menu()
			userInput=(input("Do you need anything else????: "))
			print('\n\n')
		elif(userInput=='4'):
			print("Alright lets get those videos!!!. Again this will take a lot of time. Professor Punch used a good camera lol\n")
			getVideos(beautifiedBaseObject)
			os.chdir(basePath)
			print()
			print('Alright the Videos are downloaded in the \"Videos\" folder. See if you want anything else!' )
			menu()
			userInput=(input("Do you need anything else????: "))
			print('\n\n')
		elif(userInput=='5'):
			print("Alright lets get those project files!!!\n")
			getProjects(beautifiedBaseObject)
			os.chdir(basePath)
			print()
			print('Alright Project Files are downloaded in the \"Projects\" folder. See if you want anything else!\n' )
			menu()
			userInput=(input("Do you need anything else????: "))
			print('\n\n')
		elif(userInput=='q'):
			print('\n\n')
			print("Alright fam! Take care! Be happy! Live long and prosper!!!!!!!!!!!!!")
			print('\n')
			inp=input("BTW do you want to delete this scraper file so that your credentials don't get into wrong hands???? (y/n): ")
			if inp=='y':
				os.remove(os.path.basename(sys.argv[0]))
			print('\n\n')
			break
		else:
			print("Seriously fam, Seriously. Pick one of the choices will ya!!\n")
			os.chdir(basePath)
			menu()
			print("Let's try this again\n")
			userInput=(input("Do you need anything else????: "))
			print('\n\n')
		
	
if __name__ == "__main__":
    main()



































