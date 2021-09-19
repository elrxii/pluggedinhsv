# Created by elr 
# on 12/13/2020

# This is a job-scraping program where I scrape the latest monitor prices on newegg.com.
#TODO: Database is created and linked, data is scraping properly and being saved to .csv and db.  Now work on frontend


import requests
import os
import sqlite3 
from bs4 import BeautifulSoup
from csv import writer

from createDB import *

checkDatabaseExists()
conn = connectToDB()
connObj = conn.cursor()

with open('jobs.csv', 'w') as csv_file:  # write to csv
    csv_writer = writer(csv_file)
    fileHeaders = ['CompanyName', 'JobTitle', 'DatePosted', "Location", "Link"]
    csv_writer.writerow(fileHeaders)

    urlArray = (
        ["https://www.indeed.com/jobs?q=software+engineer&l=Huntsville%2C+AL&sort=date&start={}", #hsv
        "https://www.indeed.com/jobs?q=software+enginner&l=Chicago%2C+IL&sort=date&start={}", #chicago
        "https://www.indeed.com/jobs?q=software+engineer&l=Austin%2C+TX&sort=date&start={}", #Austin, Tx
        "https://www.indeed.com/jobs?q=software+engineer&l=Raleigh%2C+NC&sort=date&start={}", #Raleigh, Tx
        "https://www.indeed.com/jobs?q=software+engineer&l=Denver%2C+CO&sort=date&start={}", #Raleigh, Tx
        "https://www.indeed.com/jobs?q=software+engineer&l=Nashville%2C+TN&sort=date&start={}"] #Nashville

    )

    clickLinkArray =(
        [
            "https://www.indeed.com/jobs?q=software%20engineer&l=Huntsville%2C%20AL&advn={}&vjk={}", #hsv
            "https://www.indeed.com/jobs?q=software%20engineer&l=Chicago%2C%20IL&advn={}&vjk={}", #chicago
            "https://www.indeed.com/jobs?q=software%20engineer&l=Austin%2C%20TX&advn={}&vjk={}", #austin
            "https://www.indeed.com/jobs?q=software%20engineer&l=Raleigh%2C%20NC&advn={}&vjk={}", #raleigh
            "https://www.indeed.com/jobs?q=software%20engineer&l=Denver%2C%20CO&advn={}&vjk={}", #raleigh
            "https://www.indeed.com/jobs?q=software%20engineer&l=Nashville%2C%20TN&advn={}&vjk={}" #raleigh
        ] 
)

    for index, link in enumerate(urlArray):
        for i in range(0,40,10):
            url = link.format(i)
            response = requests.get(url)  # must read 200 which means successfully connected to website
            src = response.content  # contains the source-code of the website
            soup = BeautifulSoup(src, 'html.parser')

            jobTitle = {"class": "jobTitle"}
            companyTitle = {"class": "companyName"}
            datePosted = {"class": "date"}
            location = {"class": "companyLocation"}
            applyLink = {"class": "tapItem"}

            titleArray = soup.find_all(attrs=jobTitle)
            companyArray = soup.find_all(attrs=companyTitle)
            datePostedArray = soup.find_all(attrs=datePosted)
            locationArray = soup.find_all(attrs=location)
            linkArray = soup.find_all(attrs=applyLink)

            for i, (a,b,c,d,e) in enumerate(zip(titleArray, companyArray, datePostedArray, locationArray, linkArray)):
                companyName = b.get_text()
                jobName = a.get_text()
                postDate = c.get_text()
                jobLocation = d.get_text()
                redirect_link = 'https://indeed.com'+ e['href']

                csv_writer.writerow([companyName, jobName,postDate, jobLocation, redirect_link])
                connObj.execute('''INSERT INTO Jobs(company_name, job_title, date_posted, location, link)  
                                   VALUES (?,?,?,?,?)''', (companyName, jobName,postDate, jobLocation, redirect_link))

conn.commit()
conn.close()
