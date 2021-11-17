# %%
import os
import re
from datetime import datetime
from pathlib import Path

import pandas as pd
from Bio import Entrez
from Bio.Entrez import efetch, read
from bs4 import BeautifulSoup

# %%
retstart = 0
sort = "pub+date"
duration = ('2016/01/01', '2021/09/30')
# duration = ('2021/07/07', '2021/07/07')
retmax = 1000
query = 'case report'

folder_name = f"pubmed (duration = {duration[0].replace('/', '-')} to {duration[1].replace('/', '-')}, query = '{query}')"

home_dir = Path("/home/is/leanfranzl-y/Python/")
# home_dir = Path('/Users/leanfranzl-y/Documents/Python/')

output_dir = home_dir / f'Data/Output/PubMed_Scraper/{folder_name}/'.replace('//', '/')

save_file_name = str(home_dir) + f'/Data/Output/PubMed_Scraper/pubmed_id_{folder_name}.csv'
summary_csv_file_name = str(home_dir) + f'/Data/Output/PubMed_Scraper/summary_{folder_name}.csv'

entrez_email = 'yao.lean_franzl_lim.yg3@is.naist.jp'