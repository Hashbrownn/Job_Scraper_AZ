
from __future__ import unicode_literals

#importing required libraries
import bs4
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
import re
from collections import OrderedDict


def amazon_job(number_page):
    """
    retrieve job title, job location, job posting date, and job link from every page in 
    https://amazon.jobs.

    Arguments:
    number_page -- Number of pages that one wish to retrive the data from.

    Return:
    s -- A tuple including all the job infromation for each job in each page
    """
    job_title=[]
    location=[]
    posting_date=[]
    job_link=[]
    for i in range(number_page):


        driver = webdriver.Chrome()
        # driver=webdriver.PhantomJS(executable_path=r'C:\Users\Bat\Downloads\phantomjs-2.1.1-windows\bin\phantomjs')
        
        #There are 10 job postings in each page. Therefore, job pages URL can be updated
        #by muliplying the counter ("i") by 10.
        URL= 'https://www.amazon.jobs/en/search?offset="+str(10*i)+"&result_limit=10&sort=recent&job_type=Full-Time&cities[]=Hyderabad%2C%20Telangana%2C%20IND&cities[]=Bengaluru%2C%20Karnataka%2C%20IND&loc_query=India&base_query=&city=&country=IND&region=&county=&query_options=&'
        driver.get(URL)
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        driver.quit()      

        # print(soup)
        # print([td.find('h3').text for td in soup.findAll("div", {"class": "job-tile"})])

        job_title.append([td.find('h3').text for td in soup.findAll("div", {"class": "job-tile"})])
        location.append([td.text.split('|', 1)[0] for td in soup.findAll("div", {"class": "location-and-id"})]) 
        posting_date.append([re.sub('Posted ', '', td.text) for td in soup.findAll("h2", {"class": "posting-date"})])
        job_link.append(['https://www.amazon.jobs'+td.find('a').get('href') for td in soup.findAll("div", {"class": "job-tile"})])
           
        # print(job_title)
        # print(job_link)
    return job_title,location,posting_date,job_link


job = amazon_job(1)

print(job)

def make_list(job):
    """
    put all the job data in alist that can be used to create a DataFrame

    Arguments:
    job_list -- A tuple containing job title, job location, job posting date, and job link .

    Return:
    s -- A list containing job information
    """
    t=[]
    for i in job:
        for b in i:
            for c in b:
                t.append(c)
    return t


#make a list of all job data
job_list=make_list(job)
len(job_list)
print(job_list)

#Create a dataframe from the job information list
def make_dataframe(job_list):
    """
    ceate a dataframe from the job_list
    
    Arguments:
    job_list -- A tuple containing job title, job location, job posting date, and job link .

    Return:
    df -- A dataframe containing each job description, basic qualification and preferred qualification.
    """
    
    l=int(len(job_list)/4)
    df=pd.DataFrame(OrderedDict({'Title': job_list[:l], 'location': job_list[l:2*l], 'Posting_date':job_list[2*l:3*l], 'job_link': job_list[3*l:]}) )
    
    return df


#DataFrame containing job title, job location, job posting date, and job link.
df1 = make_dataframe(job_list)

def job_description(job_list):
    """
    retrieving job description, basic qualification and preferred qualification.
    we get the job link from the previous job_list and then this function goes to every posted job
    page to get each job description, basic qualification and preferred qualification.

    Arguments:
    job_list -- A tuple containing job title, job location, job posting date, and job link .

    Return:
    job_information -- A list containing each job description, basic qualification and preferred qualification.
    """
    
    l=int(len(job_list)/4)
    job_link=job_list[3*l:]
    job_information=[]
    
    for x in range(l):
        driver = webdriver.Chrome()
        # driver=webdriver.PhantomJS()
        URL=job_link[x]
        driver.get(URL)
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        driver.quit()
        
        job_information.append([h3.next_sibling.text for h3 in soup.findAll("h3")])
        
    return job_information

job_description=job_description(job_list)

#create a dataframe from the job description, basic qualification and preferred qualification
df2=pd.DataFrame(job_description, columns={'DESCRIPTION','BASIC QUALIFICATIONS','PREFERRED QUALIFICATIONS'})

#combining the two dataframes and save them in a csv file
result = pd.concat([df1[['Title','location','Posting_date']], df2[['DESCRIPTION','BASIC QUALIFICATIONS','PREFERRED QUALIFICATIONS']]], axis=1, join='inner')
result.to_csv('full_job_amazon.csv')

# ful_job=amazon_job(1)
# ful_job=make_list(ful_job)
# df1=make_dataframe(ful_job)
# ful_job_de=job_description(ful_job)
# df2=pd.DataFrame(ful_job_de, columns=['DESCRIPTION','BASIC QUALIFICATIONS','PREFERRED QUALIFICATIONS'])

# df2.to_csv('job_link_des.csv')

# result = pd.concat([df1[['Title','location','Posting_date']], df2[['DESCRIPTION','BASIC QUALIFICATIONS','PREFERRED QUALIFICATIONS']]], axis=1, join='inner')
# result.to_csv('full_job_amazon_new.csv')

