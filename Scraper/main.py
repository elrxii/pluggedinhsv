# Created by elr 
# on 12/13/2020

# This is a job-scraping program where I scrape the latest monitor prices on newegg.com.
#TODO: Why are only some clickable links showing for hsv?  Remember, I only have clickable links working for hsv right now


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
        "https://www.indeed.com/jobs?q=software+engineer&l=Austin%2C+TX&sort=date&start={}"] #Austin, Tx
    )

    clickLinkArray =(
        [
            "https://www.indeed.com/jobs?q=software%20engineer&l=Huntsville%2C%20AL&advn={}&vjk={}", #hsv
            "https://www.indeed.com/jobs?q=software%20engineer&l=Chicago%2C%20IL&advn={}&vjk={}", #chicago
            "https://www.indeed.com/jobs?q=software%20engineer&l=Austin%2C%20TX&advn={}&vjk={}", #austin
        ] 
)

    for link in urlArray:
        for i in range(0,40,10):
            url = link.format(i)
            response = requests.get(url)  # must read 200 which means successfully connected to website
            src = response.content  # contains the source-code of the website
            soup = BeautifulSoup(src, 'html.parser')

            jobTitle = {"class": "jobtitle"}
            companyTitle = {"class": "company"}
            datePosted = {"class": "result-link-bar"}
            location = {"class": "recJobLoc"}
            applyLink = {"class": "jobsearch-SerpJobCard"}


            titleArray = soup.find_all(attrs=jobTitle)
            companyArray = soup.find_all(attrs=companyTitle)
            datePostedArray = soup.find_all(attrs=datePosted)
            locationArray = soup.find_all(attrs=location)
            linkArray = soup.find_all(attrs=applyLink)

            for i, (a,b,c,d,e) in enumerate(zip(titleArray, companyArray, datePostedArray, locationArray, linkArray)):
                companyName = b.get_text()
                jobName = a.get_text()
                postDate = c.find("span").get_text()
                jobLocation = d["data-rc-loc"]


                if (e.has_attr("data-empn")):
                    empn = e["data-empn"]
                    jk = e["data-jk"]
                    if (i < len(clickLinkArray)):
                        clickableLink = clickLinkArray[i].format(empn, jk) # these contain the ids for the to go straight to job link
                else:
                    clickableLink = None;
                csv_writer.writerow([companyName, jobName,postDate, jobLocation, clickableLink])
                connObj.execute('''INSERT INTO Jobs(company_name, job_title, date_posted, location, link)  
                                   VALUES (?,?,?,?,?)''', (companyName, jobName,postDate, jobLocation, clickableLink))

conn.commit()
conn.close()
