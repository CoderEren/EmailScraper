from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import re
from bs4 import BeautifulSoup
import ssl
import smtplib
import requests

sent_emails = []

sender = 'YOUR_EMAIL'
password = 'YOUR_PASSWORD'

body = """ *** PASTE YOUR EMAIL TEMPLATE - HERE IS AN EXAMPLE *** Hey, I was looking for dentists in your area and I noticed that you have a great website, but sadly it's buried deep in page 5 of Google search results.

I'm not selling anything but you should check out this tool that can help your website rank higher on Google so you can get more customers and increase your earnings.

This tool also has many other functionalities that will help you analyse your competitors' websites so you can rank higher than them on Google.
Here it is: https://bit.ly/3ahze0k

If you have any questions, feel free to reply back and I will help you :)

Thank you.
Yours sincerely."""

message = 'Subject: {}\n\n {}'.format(
    'Get More Customers By Ranking Higher',
    body)

context = ssl.create_default_context()
port = 465
host = "smtp.gmail.com"

mail_server = smtplib.SMTP_SSL(host=host, port=port, context=context)
mail_server.login(sender, password)

link_extensions = ['', 'contact', 'contact-us', 'contact.html', 'contact-us.html']

def check_email(emails):
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    regex2 = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$' #"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z0-9-.]+"
    for email in emails:
        # Check if the text is an email address
        if(re.search(regex,email) or re.search(regex2, email)):  
            print("Valid Email")
            print("\t" + email)
            if email not in sent_emails:
                sendemail(email)
                sent_emails.append(email)
            print(sent_emails)
            return True
            break
        else:
            print("Invalid Email")
            if len(email) <= 195:
                print("\t" + email)
            else:
                pass

def sendemail(email):
    receiver = email
    # Send an email
    mail_server.sendmail(sender, receiver, message)
    print("Email successfully sent to {}!".format(receiver))
    time.sleep(2)

def validurl(link):
    # Check the validity of the URL. In this case, we only want to scrape the homepages of websites.
    pattern = "(https://|http://)+(|www.)+[a-zA-Z0-9.-]+.(com|net|co|org|us|info|biz|me)+(|/)"
    p = re.compile(pattern)
    if(re.fullmatch(p, link)):
            for extension in link_extensions:
                try:
                    source = requests.get(link + extension, timeout=10)
                    soup = BeautifulSoup(source.text, 'lxml')
                    print("Looking for emails in " + link + extension)
                    # Look for emails on the website
                    find_emails = soup.body.findAll(text=re.compile('@')) #instead of re.findall
                    check_email(find_emails)
                    if check_email(find_emails):
                        break
                except:
                    pass
    else:
            print("False")

# Path of the chrome driver
PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)

start_count = ['0', '10', '20', '30', '40', '50', '60', '70', '80', '90', '100', '110', '120', '130', '140']

# This is the main for loop. It looks for URLs in the search results. It can look at the page 1 - 15 of search results.
for num in start_count:
    driver.get("https://www.google.com/search?q=dentists+in+washington&start=" + num)
    driver.implicitly_wait(5)
    parentElement = driver.find_elements_by_class_name("yuRUbf")
    for element in parentElement:
        elementList = element.find_element_by_tag_name("a")
        link = elementList.get_attribute("href")
        print(link)
        validurl(link)
    

print(sent_emails)
print("Finished scraping for emails!")
driver.quit()
