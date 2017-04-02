# Project Site "Cyclone" Scraper

## V2


So I finally completed the Scraper witht the capability to download the Worksheets, Labs, Project Files and Lecture Notes.

To use this you simply need to enter your CSE username and Password in the file once and run the file. Don't worry you will have the option to delete the file after you are done so that other people don't get your credentials. The code does check for some of the dependensies but if it gives an import error than just simply install that library using pip.

What needs to be done:

1. Code for getting sample code files.
2. Add try and catch blocks for errors. 

For advanced users
I also have uploaded the requirements.txt file which you can directly use to install the dependencies. This should get all the dependencies. I suggest using a virtual environment for this so that you don't mess up your site-packages.




##V1

This is basic web-scraper for getting the CSE 232 files.
This script returns all the pdfs, input and output files.

BTW, the script won't run on labs or X2GO client because there is no pip installed and you cannot install it without admin privileges.
pip is automatically installed for python 3.4 and 2.7.9 .
To use this script all you need to do is: 

1. Enter the base url of the project. The highlighted text below is an example of URL that you would need.

![alt tag] (https://github.com/yash1337/Project-Site-Scraper/blob/master/SampleURL.png)

2. Enter your CSE username in the USERNAME variable and password in the PASSWORD variable in the script.
Also copy the script to where you want to save the files to and then run it from there as the script saves the files in the diectory where it is.

At this point of the semester we only happen to have .txt .pdf and .cpp files so that's what I am scrapping right now. If at a further point we have work with diffrent file types then I will add that too. 

Contact me if anything breaks.

DISCLAIMER: I do not store any of the credentials and everything is stored on your local drive. The script also contains code for the deletion of the script upon completion of the scraping. Uncomment that code to make sure nobody reads your credentials after you're done scraping.

Update: The file deletion is not working on some of the computers I tested and working on some so if it does not work then just delete the file manually.

