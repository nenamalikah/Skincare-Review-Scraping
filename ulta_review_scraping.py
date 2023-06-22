#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 22 01:27:55 2023

@author: nenabeecham
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By 
import pandas as pd
import time

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


##### Set up the driver and open the product page #####
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
url= 'https://www.ulta.com/p/clarifying-lotion-1-very-dry-dry-xlsImpprod10791735?sku=2153911'

driver.get(url)
driver.maximize_window()

##### Define a function to extract information from reviews #####
def extract_page_data(driver, product):
    """ The following function extracts the text, title, date, location
    verification status, upvotes, and downvotes for each review.""" 
    
    all_page_review_text = []
    all_page_review_title = []
    all_page_review_dates = []
    all_page_review_locations = []
    all_page_review_verified= []
    all_review_upvotes = []
    all_review_downvotes = []
    
    ##### Extract all reviews from the page #####
    whole_review = driver.find_elements(By.CLASS_NAME, 'pr-review')
    for review in whole_review:
        review = review.text.split("\n")
        if review[4] != "Verified Buyer":
            all_page_review_verified.append('No')
        else:
            all_page_review_verified.append('Yes')
      
    # Iterate through each review and get the upvotes and downvotes
    for review in whole_review:
        review = review.text.split("\n")
        all_review_upvotes.append(review[-1].split(' ')[0])
        all_review_downvotes.append(review[-1].split(' ')[1])
    
    # Iterate through each review and get the location
    for review in whole_review:
        review = review.text.split("\n")
        all_page_review_locations.append(review[3])
        
    # Locate all review elements on the current page
    page_review_text = driver.find_elements(By.XPATH, '//p[@class="pr-rd-description-text"]')
    # Iterate through the list of reviews
    for review in page_review_text:
        # Extract the text content of each review
        single_review = review.text
        # Add the extracted text content to the page_output list
        all_page_review_text.append(single_review)
        
    # Locate all review titles on the current page 
    page_review_titles = driver.find_elements(By.XPATH, '//h5[@class="pr-rd-review-headline pr-h2"]')
    # Iterate through the list of titles
    for title in page_review_titles:
        # Extract the text content of each title
        single_title = title.text
        # Add the extracted title to the list of all titles
        all_page_review_title.append(single_title)
    
    # Locate all review dates on the current page
    page_review_dates = driver.find_elements(By.XPATH, '//p[@class="pr-rd-details pr-rd-author-submission-date"]')
    # Iterate through the list of dates
    for date in page_review_dates:
        # Extract the date of each review
        single_date = date.text
        # Add the extracted date to the list of all dates
        all_page_review_dates.append(single_date)

    return all_page_review_dates, all_page_review_title,  all_page_review_locations, all_page_review_verified, all_page_review_text, all_review_upvotes, all_review_downvotes
    


start = time.time()

total_titles = [] 
total_text = [] 
total_dates = [] 
total_upvotes = [] 
total_downvotes = []
total_locations = [] 
total_verified = [] 

##### Iterate through the first 300 pages of reviews and extract their information #####
for page_num in range(300):

    page_review_dates, page_review_title,  page_review_locations, page_review_verified, page_review_text, page_review_upvotes, page_review_downvotes = extract_page_data(driver, product='Multi-Vitamin Thermafoliant')

    total_titles.append(page_review_title)
    total_text.append(page_review_text)
    total_upvotes.append(page_review_upvotes)
    total_locations.append(page_review_locations)
    total_dates.append(page_review_dates)
    total_downvotes.append(page_review_downvotes)
    total_verified.append(page_review_verified)
        
    next_page = driver.find_element(By.XPATH,'//*[@id="yotpo-reviews-e453ce3f-3f92-4a9a-8bae-115a02522c43"]/nav/div/a[11]').click()
    
    print(f'Page {page_num} complete.')
    next_page = driver.find_element(By.CLASS_NAME,"pr-rd-pagination-btn.pr-rd-pagination-btn--next").click()
    time.sleep(10)
    
end = time.time()

total_time = end - start
total_time/60 # Print the time it took all review information to be extracted


##### Combine all of the review information into a single dataframe #####
df_reviews = []
df_titles = []
df_locations = []
df_dates = []
df_verified = []
df_upvotes = []
df_downvotes = []

for List in total_text:
    for single_review in List:
        df_reviews.append(single_review)
        
for titles in total_titles:
    for single_title in titles:
        df_titles.append(single_title)
        
for locations in total_locations:
    for single_loc in locations:
        df_locations.append(single_loc)
        
for dates in total_dates:
    for single_date in dates:
        df_dates.append(single_date)
        
for status in total_verified:
    for single_status in status:
        df_verified.append(single_status)
        
for upvote in total_upvotes:
    for single_upvote in upvote:
        df_upvotes.append(single_upvote)
        
for downvote in total_downvotes:
    for single_downvote in downvote:
        df_downvotes.append(single_downvote)
        
 
final_data = pd.DataFrame({'Review_Title':df_titles, 'Review_Text':df_reviews, 'Verified_Buyer':df_verified, 'Review_Date':df_dates, 
                         'Review_Location':df_locations, 'Review_Upvotes':df_upvotes, 'Review_Downvotes':df_downvotes})
final_data['Product'] = 'Multi-Vitamin Thermafoliant'
final_data['Brand'] = 'Dermalogica'
final_data['Scrape_Date'] = '3/27/2023'
final_data.head()

##### Close the webpage and quit the driver #####
driver.close()
driver.quit()