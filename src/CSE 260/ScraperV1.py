#############################
##Project Site 'Cyclone" Scraper v1
##This thing Scrapes everthing from the CSE 260 Lecture Notes, Sample tests, and Homework assignments
##You need to supply the CSE 260 Password that professor gave us
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

baseURL='http://www.cse.msu.edu/~cse260/cse260cn/'
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

def getLectures(beautifiedBaseObject):
	LectureBaseURLList=[]
	LectureFolderPath=os.path.dirname(os.path.abspath(__file__))+'\\Lecture'
	
	if not os.path.exists(LectureFolderPath):
		os.makedirs(LectureFolderPath) 
		
	for link in beautifiedBaseObject.find_all('a'):
		if 'lecture' in link['href'] and "Sample" not in link['href']:
			LectureBaseURLList.append(urljoin(baseURL,link['href']))
			
	for URL in LectureBaseURLList:
		downloadFiles(URL,LectureFolderPath)
		
def getSampleTests(beautifiedBaseObject):
	SamTestsBaseURLList=[]
	SamTestsFolderPath=os.path.dirname(os.path.abspath(__file__))+'\\Sample Tests'
	
	if not os.path.exists(SamTestsFolderPath):
		os.makedirs(SamTestsFolderPath) 
	
	for link in beautifiedBaseObject.find_all('a'):
		if 'lecture' in link['href'] and "Sample" in link['href']:
			SamTestsBaseURLList.append(urljoin(baseURL,link['href']))
	
	for URL in SamTestsBaseURLList:
		downloadFiles(URL,SamTestsFolderPath)
		
		
def getHomework(beautifiedBaseObject):
	HomeworkBaseURLList=[]
	HomeworkFolderPath=os.path.dirname(os.path.abspath(__file__))+'\\Homework Assignments'
	
	if not os.path.exists(HomeworkFolderPath):
		os.makedirs(HomeworkFolderPath) 
		
	for link in beautifiedBaseObject.find_all('a'):
		if 'homework' in link['href']:
			HomeworkBaseURLList.append(urljoin(baseURL,link['href']))
	
	for URL in HomeworkBaseURLList:
		downloadFiles(URL,HomeworkFolderPath)
		
def menu():
	print("The list of choices are as follows. Choose the ones you like one by one. Don't worry you will get future chances (just as in life!! :-)): \n")
	print("1. All the lecture notes!\n")
	print("2. All the Sample test files!\n")
	print("3. All the Homework files!\n")
	print("q. Nothing fam. Just get me out of here!\n")
	
def main():
	print("Welcome to CSE260 Scraper!!!!!!\n")
	menu()	
	userInput=(input("So what do you want (not in life. What do you want right now!!!): "))
	print()
	UNAME="cse260"
	PASSWORD=input("Please enter password for CSE260 account that Professor gave us(Hint: Discrete Math Is Good for ME): ")
	beautifiedBaseObject=returnBeautifiedObject(baseURL,UNAME,PASSWORD)
	while(True):
		if(userInput=='1'):
			print("Alright lets get those Lecture files!!!\n")
			getLectures(beautifiedBaseObject)
			os.chdir(basePath)
			print()
			print('Alright the lecture notes are downloaded in the \"Lecture\" folder. See if you want anything else!\n' )
			menu()
			userInput=(input("Do you need anything else????: "))
			print('\n\n')
		elif(userInput=='2'):
			print("Alright lets get those Sample test files!!!\n")
			getSampleTests(beautifiedBaseObject)
			os.chdir(basePath)
			print()
			print('Alright the Sample test files are downloaded in the \"Sample Tests\" folder. See if you want anything else!\n' )
			menu()
			userInput=(input("Do you need anything else????: "))
			print('\n\n')
		elif(userInput=='3'):
			print("Alright lets get those Homework files!!!\n")
			getHomework(beautifiedBaseObject)
			os.chdir(basePath)
			print()
			print('Alright the Homework files are downloaded in the \"Homework Assignments\" folder. See if you want anything else!\n' )
			menu()
			userInput=(input("Do you need anything else????: "))
			print('\n\n')
		elif(userInput=='q'):
			print('\n\n')
			print("Alright fam! Take care! Be happy! Live long and prosper!!!!!!!!!!!!!")		
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