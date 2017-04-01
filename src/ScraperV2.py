#############################
##Project Site 'Cyclone" Scraper v2
##This thing Scrapes everthing from the CSE 232 site videos, examples code, presentations, and project files
##
#############################

################################################################################################################

###Checking dependensies
import re
import requests 
from bs4 import BeautifulSoup #getting the beasutiful soup library
from requests.auth import HTTPBasicAuth
from urllib.parse import urljoin
import os
import msvcrt as m
# try:
	# print("Importing other libraries")
	# from requests.auth import HTTPBasicAuth
	# from urllib.parse import urljoin
	# import os
	# import msvcrt as m
# except:
	# print("Just get those libraries man!!!")
	
# try:
	# import requests 
	# print ("Request library is good!! ")
# except:
	# print("Request Library not found. Trying to install it. If not successfull then try it manually")
	# os.system('pip install requests')

# try:
	# from bs4 import BeautifulSoup
	# print("BeautifulSoup library is good!! ")
# except:
	# print("BeautifulSoup Library not found. Trying to install it. If not successfull then try it manually")
	# os.system('pip install beautifulsoup4')
	

	

################################################################################################################

################################################################################################################
UNAME="sharmay4"
PASSWORD="D@rkL0rd"
################################################################################################################

################################################################################################################

###Actual Code

baseURL='http://www.cse.msu.edu/~cse232/'

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
def downloadVideos(URL,PATH,book_name=''):
	
		
	r=requests.get(URL)
	print("Downloading: "+book_name+" ...")
	f=open(book_name,'wb');
	print ("Donloading.....")
	for chunk in r.iter_content(chunk_size=255): 
		if chunk: # filter out keep-alive new chunks
			f.write(chunk)
	print ("Done")
	f.close()
	
	
	
def getWorksheets(beautifiedBaseObject):
	worksheetURL=''
	worksheetFolderPath=os.path.dirname(os.path.abspath(__file__))+'\worksheets'
	#print(worksheetFolderPath)	
	if not os.path.exists(worksheetFolderPath):
		os.makedirs(worksheetFolderPath)
	
	for link in beautifiedBaseObject.find_all('a'):
		if 'Worksheets' in urljoin(baseURL,link['href']):
			worksheetURL=urljoin(baseURL,link['href'])
	worksheetHTMLObject=requests.get(worksheetURL)
	completedWorksheetURL=''
	#print(worksheetURL+'/'+'w1.cpp')
	beautifiedWorksheetHTMLObject=BeautifulSoup(worksheetHTMLObject.text,"html.parser")	
	
	for link in beautifiedWorksheetHTMLObject.find_all('a'):
		if (".pdf" in link['href'] or ".cpp" in link['href']):
			completedWorksheetURL=worksheetURL+'/'+link['href']
			book_name = completedWorksheetURL.split('/')[-1]
			book_name=book_name[:1]+'orksheet'+book_name[1:]
			worksheetName=book_name
			worksheetFilePath=worksheetFolderPath+"\\"+book_name.split('.',1)[0]	
			if not os.path.exists(worksheetFilePath):
				os.makedirs(worksheetFilePath)
			downloadFiles(completedWorksheetURL,worksheetFilePath,book_name)
			# print("Downloading: "+book_name+" ...")
			# with open(book_name, 'wb') as book:
				# a = requests.get(completedWorksheetURL)
				# for block in a.iter_content(512):
					# if not block:
						# break
					# book.write(block)

	

def getLabs(beautifiedBaseObject):
	labBaseURLList=[]	
	labFolderpath=os.path.dirname(os.path.abspath(__file__))+'\labs'
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
						#downloadFiles(labFileURL,labFilePath)

						
def getReadings(beautifiedBaseObject):
	readingBaseURLList=[]
	readingFolderPath=os.path.dirname(os.path.abspath(__file__))+'\\readings'
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
	videoFolderPath=os.path.dirname(os.path.abspath(__file__))+'\\videos'
	if not os.path.exists(videoFolderPath):
		os.makedirs(videoFolderPath)
	
	for link in beautifiedBaseObject.find_all('a'):
		if 'week' in link['href'] and '.pdf' not in link['href']:
			videoBaseURLList.append(urljoin(baseURL,link['href']))
	videoBaseURLList.pop(0)	#deleting the URL without week number
	tempBeautifiedObject=None
	beautifiedVideoObject=None
	dtDict={}
	ulLinkSet=set()
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
				#print(videoFileURL)
				#print(videoFilePath)
				#print(bookName)
				#print()
				downloadFiles(videoFileURL,videoFilePath,bookName)
				
		
		
		
	#print(ulLinkSet)
beautifiedBaseObject=returnBeautifiedObject(baseURL)		
#basestHTMLRequestObject=requests.get('http://www.cse.msu.edu/~cse232/')
#beautifiedbasestHTMLRequestObject=BeautifulSoup(basestHTMLRequestObject.text,"html.parser")
#print(beautifiedbasestHTMLRequestObject)
#getWorksheets(beautifiedbasestHTMLRequestObject)
#getLabs(beautifiedBaseObject)
getVideos(beautifiedBaseObject)



































