# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import os
import re
from datetime import datetime

import pandas as pd
from tqdm import tqdm
from bs4 import BeautifulSoup as bs

from specifications import output_dir, folder_name, summary_csv_file_name

# %%
# Summarizing extracted documents to csv format
# columns == pmid, authors, publication date, title, abstract

pmids = []
authors = []
# publication_dates = []
pubdates = []
pubdate_years = []
years = []
months = []
days = []
titles = []
abstracts = []
raw_output = []

files = [f for f in os.listdir(output_dir) if f.endswith('xml')]
for file in tqdm(files, desc='Summarizing output to csv.'):
    raw = open(str(output_dir) + '/' + file, encoding='utf-8').read()
    
    soup = bs(raw, features='html.parser')
    
    pmid = file.split('.')[0]

    author = soup.find_all('author')
    for i, info in enumerate(author):
        info = [str(j) for j in info]
        author[i] = ' '.join(info)
    author = ' || '.join(author)



    pubdate = soup.pubdate
    if pubdate is not None:
        pubdate_year = re.findall(r'[0-9]{4}', pubdate.text)[0]
    else:
        pubdate_year = ''
    
    pubmedpubdate = soup.find_all('pubmedpubdate', attrs={'pubstatus':"pubmed"})

    if len(pubmedpubdate) > 0:
        pubmedpubdate = pubmedpubdate[0]
        year = pubmedpubdate.year.text
        month = pubmedpubdate.month.text
        day = pubmedpubdate.day.text
        # pubmedpubdate = f'{pubmedpubdate.year.text}-{pubmedpubdate.month.text}-{pubmedpubdate.day.text}'
    else:
        year = ''
        month = ''
        day = ''

    if soup.title is not None:
        title = soup.title.text
    else:
        # print(raw)
        title = ''
        
    if soup.abstract is not None:
        abstract = soup.abstract.text
    else:
        # print(raw)
        abstract = ''

    pmids.append(pmid)
    authors.append(author)
    pubdates.append(str(pubdate))
    pubdate_years.append(pubdate_year)
    years.append(year)
    months.append(month)
    days.append(day)
    # publication_dates.append(pubmedpubdate)
    titles.append(title)
    abstracts.append(abstract)
    raw_output.append(raw)

        
output_df = pd.DataFrame(
    list(zip(pmids, authors, pubdates, pubdate_years, years, months, days, titles, abstracts, raw_output)),
    columns=['pmid', 'authors', 'pubdate', 'pubdate_year', 'year', 'month', 'day', 'title', 'abstract', 'raw_output']
)

# output_df.to_csv(summary_csv_file_name)

compression_options = dict(method='zip', archive_name=f'summary_{folder_name}.csv')
output_df.to_csv(f'{summary_csv_file_name[:-3]}zip', compression=compression_options)