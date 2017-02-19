# Project-Site-Scraper
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

