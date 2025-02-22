# ScrapPaper

![bdge_star](https://img.shields.io/github/stars/rafsanlab/ScrapPaper?style=social)
![bdge_fork](https://img.shields.io/github/forks/rafsanlab/ScrapPaper?style=social) 
![bdge_twtr](https://img.shields.io/twitter/follow/rafsanlab?style=social) 

![test](/img/abstract.png)

## About this project
ScrapPaper is a web scrapping method to extract journal information from PubMed and Google Scholar using Python script. Users need to install Python 3 and required modules, and run the `scrappaper.py` script. Refer to the published paper for detailed instruction. This side project was completed on March 8, 2022 by @rafsanlab. Follow me on Twitter: https://twitter.com/rafsanlab

### Paper to cite:
Rafsanjani, M. R. (2022). ScrapPaper: A web scrapping method to extract journal information from PubMed and Google Scholar search result using Python. In bioRxiv (p. 2022.03.08.483427). https://doi.org/10.1101/2022.03.08.483427

## System Requirement
* Python (version 3 or above)
* The following Python modules: requests, csv, re, time, random, pandas, sys, bs4
* Operating system (current code was tested on Windows 10)
* Command prompt (if using Windows) / terminal
* Search link of the first page result from PubMed or Google Scholar
* Text editor or spreadsheet software to open the results

## Simplified instructions
1. Download the `scrappaper.py` script and `cd` terminal to the directory.
2. Copy the link from the first search results of PubMed or Google Scholar.
3. Run the code
   '''
   python scrappper.py "https://scholar.google.com/scholar?hl=en&as_sdt=0%2C5&q=biology+&btnG=" --pages 10 > google_scholar_papers.tsv
   '''
5. When finished, open the results using text editor or spreadsheet. 
6. Refer to the published paper for detailed instruction.

## Disclaimer
Web scraping might get you blocked from the server, run at your own risk. So far,
we scrapped 28 pages of Google Scholar results with no issues.
