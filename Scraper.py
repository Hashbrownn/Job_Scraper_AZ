# importing packages
import pandas as pd
import re
import io

from bs4 import BeautifulSoup
from datetime import date, timedelta, datetime
from IPython.core.display import clear_output
from random import randint
import requests
from requests import get
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
from time import time
start_time = time()

from warnings import warn

jd = pd.DataFrame()

# url_ds = "https://www.linkedin.com/jobs/search?keywords=Data%20Scientist&location=India&geoId=102713980&trk=public_jobs_jobs-search-bar_search-submit&redirect=false&position=1&pageNum=0&sortBy=DD"
# url_ba = "https://www.linkedin.com/jobs/search?keywords=Business%20Analyst&location=India&geoId=102713980&trk=public_jobs_jobs-search-bar_search-submit&redirect=false&position=1&pageNum=0&sortBy=DD"
# url_da = "https://www.linkedin.com/jobs/search?keywords=Data%20Analyst&location=India&geoId=102713980&trk=public_jobs_jobs-search-bar_search-submit&redirect=false&position=1&pageNum=0&sortBy=DD"
# url_de = "https://www.linkedin.com/jobs/search?keywords=Data%20Engineer&location=India&geoId=102713980&trk=public_jobs_jobs-search-bar_search-submit&redirect=false&position=1&pageNum=0&sortBy=DD"

no_of_jobs = 100

driver = webdriver.Chrome()
# urls = [url_ds,url_ba,url_da,url_de]

# urls = "https://www.linkedin.com/jobs/search?keywords=Data%20Scientist&location=India&geoId=102713980&trk=public_jobs_jobs-search-bar_search-submit&redirect=false&position=1&pageNum=0&sortBy=DD"
# urls = "https://careers.vmware.com/main/jobs?keywords=Business%20Analyst&page=1&sortBy=posted_date&descending=true"
urls = "https://www.amazon.jobs/en/search?offset=0&result_limit=10&sort=recent&job_type=Full-Time&distanceType=Mi&radius=24km&latitude=&longitude=&loc_group_id=&loc_query=India&base_query=&city=&country=IND&region=&county=&query_options=&"

driver.get(urls)
pageSource = driver.page_source
lxml_soup = BeautifulSoup(pageSource, 'html.parser')

print(lxml_soup)


results = lxml_soup.find(id='main-content')

print(results.prettify())

# job_elems = results.find_all('section', class_='job-results-container')
# print(job_elems)
# for url in urls:


#     driver.get(url)
#     sleep(3)
#     action = ActionChains(driver)
#     # to show more jobs. Depends on number of jobs selected
#     i = 2
#     while i <= (no_of_jobs/100): 
#         driver.find_element_by_xpath('/html/body/main/div/section/button').click()
#         i = i + 1
#         sleep(5)

#     pageSource = driver.page_source
#     lxml_soup = BeautifulSoup(pageSource, 'lxml')

#     # searching for all job containers
#     job_container = lxml_soup.find('ul', class_ = 'jobs-search__results-list')

#     print(job_container)
#     print('You are scraping information about {} jobs.'.format(len(job_container)))

#     job_id = []
#     post_title = []
#     company_name = []
#     post_date = []
#     job_location = []
#     job_desc = []
#     level = []
#     emp_type = []
#     functions = []

#     # for loop for job title, company, id, location and date posted
#     for job in job_container:
        
#         # job title
#         job_titles = job.find("span", class_="screen-reader-text").text
#         post_title.append(job_titles)
        
#         # linkedin job id
#         job_ids = job.find('a', href=True)['href']
#         job_ids = re.findall(r'(?!-)([0-9]*)(?=\?)',job_ids)[0]
#         job_id.append(job_ids)
        
#         # company name
#         company_names = job.select_one('img')['alt']
#         company_name.append(company_names)
        
#         # job location
#         job_locations = job.find("span", class_="job-result-card__location").text
#         job_location.append(job_locations)
        
#         # posting date
#         post_dates = job.select_one('time')['datetime']
#         post_date.append(post_dates)

#     # for loop for job description and criterias
#     for x in range(1,len(job_id)+1):
        
#         # clicking on different job containers to view information about the job
#         job_xpath = '/html/body/main/div/section/ul/li[{}]/img'.format(x)
#         driver.find_element_by_xpath(job_xpath).click()
#         sleep(3)
        
#         # job description
#         jobdesc_xpath = '/html/body/main/section/div[2]/section[2]/div'
#         job_descs = driver.find_element_by_xpath(jobdesc_xpath).text
#         job_desc.append(job_descs)
        
#         # job criteria container below the description
#         job_criteria_container = lxml_soup.find('ul', class_ = 'job-criteria__list')
#         all_job_criterias = job_criteria_container.find_all("span", class_='job-criteria__text job-criteria__text--criteria')
        
#         # Seniority level
#         seniority_xpath = '/html/body/main/section/div[2]/section[2]/ul/li[1]'
#         seniority = driver.find_element_by_xpath(seniority_xpath).text.splitlines(0)[1]
#         level.append(seniority)
        
#         # Employment type
#         type_xpath = '/html/body/main/section/div[2]/section[2]/ul/li[2]'
#         employment_type = driver.find_element_by_xpath(type_xpath).text.splitlines(0)[1]
#         emp_type.append(employment_type)
        
#         # Job function
#         function_xpath = '/html/body/main/section/div[2]/section[2]/ul/li[3]'
#         job_function = driver.find_element_by_xpath(function_xpath).text.splitlines(0)[1]
#         functions.append(job_function)
        
#         x = x+1

#     job_data = pd.DataFrame({'Job ID': job_id,
#     'Date': post_date,
#     'Company Name': company_name,
#     'Post': post_title,
#     'Location': job_location,
#     'Description': job_desc,
#     'Level': level,
#     'Type': emp_type,
#     'Function': functions
#      })

#     # cleaning description column
#     job_data['Description'] = job_data['Description'].str.replace('\n',' ')


#     print(job_data.info())
#     # job_data.head()

#     print(job_data)
#     # job_data.to_csv(r'C:\Users\Bat\Downloads\Jobs_Trial.csv', encoding = 'utf-8')
#     jd = jd.append(job_data)

# print(jd.shape)

# with io.open('C:\\Users\\Bat\\Downloads\\Jobs_Trial_4.csv', 'w' , encoding="utf-8", newline='') as csv_file:
#     jd.to_csv(path_or_buf=csv_file)

# print("file created")


