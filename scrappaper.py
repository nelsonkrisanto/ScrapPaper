'''
Forked from 'ScrapPaper' by M. R. Rafsanjani.
Update script for Pubmed Summary format.
e.g.: https://pubmed.ncbi.nlm.nih.gov/?term=dengue+virus+primer
'''

print("Initiating... please wait.\n")

import requests
import random
import time
import pandas as pd
from sys import exit
from bs4 import BeautifulSoup
import os

# ===== DEFINE FUNCTIONS =====

search_from, URL_edit = "", ""

def wait():
    print("Waiting for a few secs...")
    time.sleep(random.randrange(1, 6))
    print("Waiting done. Continuing...\n")

def checkPage():
    global search_from
    if "pubmed" in URL_input:
        search_from = "Pubmed"
        print("Input is from: PubMed.\n")
    else:
        print("Page URL undefined.\n")


# ===== GETTING AND SETTING THE URL =====

URL_input = input("Please paste search URL and press Enter:")
URL_ori = URL_input
headers = requests.utils.default_headers()
headers.update({
    'User-Agent': 
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
})
checkPage()

# Check if the CSV file exists and is empty to decide on writing the header later
file_exists = os.path.isfile('scrapped_pubmed.csv')
need_header = not file_exists or os.stat('scrapped_pubmed.csv').st_size == 0

data = []  # Initialize a list to collect data

# ===== MAIN FRAMEWORK =====

# ===== CODE FOR PUBMED =====

if search_from == "Pubmed":

    try:
        # SETTING & GETTING PAGE NUMBER
        page_num = 1
        page_view = 200  # can be change to 10, 20, 50, 100, or 200
        URL_edit = URL_ori + "&page=" + str(page_num) + "&size=" + str(page_view)    
        print("URL : ", URL_edit)

        page = requests.get(URL_edit, headers=headers, timeout=None)
        soup = BeautifulSoup(page.content, "html.parser")
        wait()

        page_total = soup.find("label", class_="of-total-pages").text
        page_total_num = int(''.join(filter(str.isdigit, page_total)))
        print(f"Total page number: {page_total_num}")
        print(f"Results per page: {page_view}.\n")

    except AttributeError:
        print("Opss! ReCaptcha is probably preventing the code from running.")
        print("Please consider running in another time.\n")
        exit()

    wait()

    # EXTRACTING INFORMATION
    for i in range(page_total_num):

        page_num_up = page_num + i
        URL_edit = URL_ori + "&page=" + str(page_num_up) + "&size=" + str(page_view)
        page = requests.get(URL_edit, headers=headers, timeout=None)    

        soup = BeautifulSoup(page.content, "html.parser")
        wait()
        results = soup.find("section", class_="search-results-list")
        job_elements = results.find_all("article", class_="full-docsum")

        for job_element in job_elements:
            title_element = job_element.find("a", class_="docsum-title")
            cit_element = job_element.find("span", class_="docsum-journal-citation full-journal-citation").text.strip()
            link_url = job_element.find("a")["href"]  # Assuming the first 'a' tag is the correct link
            title_element_clean = title_element.text.strip()
            link_url_clean = "https://pubmed.ncbi.nlm.nih.gov" + link_url

            # Collect data
            data.append([title_element_clean, link_url_clean, cit_element])

        wait()

    # Convert collected data to DataFrame and append to CSV, adding header if needed
    df = pd.DataFrame(data, columns=['Title', 'Links', 'References'])
    df.to_csv('scrapped_pubmed.csv', mode='a', header=need_header, index=False)

# END OF PROGRAM

print("Job finished, Godspeed you! Cite us.")
