# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import os

# import re
from datetime import datetime
from pathlib import Path
import shutil

# import pandas as pd
# from Bio import Entrez
# from Bio.Entrez import efetch, read
# from tqdm import tqdm
# from bs4 import BeautifulSoup as bs

from functions import *
from specifications import *

# %%
os.makedirs(output_dir, exist_ok=True)

start_time = datetime.now()

# %%
# Scratch work
# extracted_list, retstart = get_fetched_abstract(save_file_name)
# retmax = 50

# pmid_list, pmid_count = search(
#     query=query,
#     retstart=retstart,
#     retmax=retmax)
# retmax = min(retmax, int(pmid_count))
# pmid_list, pmid_count = search(
#     query=query,
#     retstart=retstart,
#     retmax=retmax)

# documents = extract_abstract(
#     pmid_list=pmid_list,
#     extracted_list=extracted_list,
#     save_file_name=save_file_name,
#     retstart=retstart,
#     pmid_count=pmid_count,
#     output_dir=output_dir)

# %%
# Scrape data
save_to_csv_pmid_of_extracted_abstracts(output_dir, save_file_name)

_, N = search(
    query=query,
    entrez_email=entrez_email,
    retstart=retstart,
    sort=sort,
    mindate=duration[0],
    maxdate=duration[1],
    retmax=retmax,
)

N = int(N)
_, counter = list_from_csv(save_file_name)

print(f"Extracting {N - counter:,} abstracts.")

if __name__ == "__main__":
    while counter < N:
        # extracted_list, retstart = list_from_csv(save_file_name)
        extracted_list, _ = list_from_csv(save_file_name)
        retstart += retmax

        # pmid_list, pmid_count = search(query=query,retstart=retstart, retmax=retmax)

        # retmax = min(retmax, int(pmid_count))

        pmid_list, pmid_count = search(
            query=query,
            entrez_email=entrez_email,
            retstart=retstart,
            sort=sort,
            mindate=duration[0],
            maxdate=duration[1],
            retmax=retmax,
        )

        if len([x for x in pmid_list if x not in extracted_list]) < retmax:
            # if there's too much overlap, widen the search space
            pmid_list, pmid_count = search(
                query=query,
                entrez_email=entrez_email,
                retstart=retstart,
                sort=sort,
                mindate=duration[0],
                maxdate=duration[1],
                retmax=2 * retmax,
            )

        n_extracted = extract_abstract(
            pmid_list=pmid_list,
            extracted_list=extracted_list,
            save_file_name=save_file_name,
            retstart=retstart,
            pmid_count=pmid_count,
            output_dir=output_dir,
        )

        counter += n_extracted

        print(f"Extracted {counter:,} out of {N:,}.")

# %%
# Summarize xml files to one csv file
from xml_to_csv import *

# Zip output xml to zip file
zip_files(output_dir, zip_name=f"xml_{folder_name}")
shutil.rmtree(str(output_dir))

# %%
end_time = datetime.now()
print(f"Started: {start_time}")
print(f"Finished: {end_time}")
print("Duration: {}".format(end_time - start_time))
# %%
