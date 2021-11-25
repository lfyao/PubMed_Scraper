# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import os
from zipfile import ZipFile

import pandas as pd
from Bio import Entrez
from Bio.Entrez import efetch, read


# %%
def search(query, entrez_email, mindate, maxdate, retstart=0, sort="pub+date", retmax=100):
    Entrez.email = entrez_email
    handle = Entrez.esearch(db      ='pubmed',
                            retmax  =retmax,
                            retmode ='xml',
                            term    =query,
                            retstart=retstart,
                            sort    =sort,
                            mindate =mindate,
                            maxdate =maxdate)
    search_results = Entrez.read(handle)

    pmid_list=search_results['IdList']
    pmid_count=search_results['Count']
    return pmid_list, pmid_count #returns list of PMID


def fetch_document(pmid):
    handle = efetch(db='pubmed', id=pmid, retmode='text', rettype='xml')#,rettype='abstract')
    return handle.read()


def extract_abstract(pmid_list, extracted_list, save_file_name, retstart, pmid_count, output_dir):
    # extracted_list = pd.read_csv(save_file_name, sep=',',header=None)
    # extracted_list = list(extracted_list[0].astype(str))

    pmid_list = [x for x in pmid_list if x not in extracted_list]

    total = len(pmid_list)

    print(f'Now extracing {total:,}.')

    for counter, id in enumerate(pmid_list, 1):
        if counter % 10 == 0 or counter == total:
            print(f"==> Fetched abstracts {counter:,} out of {total:,}")
            save_to_csv_pmid_of_extracted_abstracts(output_dir=output_dir, save_file_name=save_file_name)

        try:
            xml_abstracts = fetch_document(id)
        
            with open(str(output_dir) + '/' + str(id) + '.xml', "w", encoding='utf-8') as f:
                f.write(str(xml_abstracts, 'UTF-8'))
        
        except:
            print('error')

    return total

def list_from_csv(save_file_name, sep=","):
    try:
        file = pd.read_csv(save_file_name, sep=sep,header=None)
        extracted_list = list(file[0].astype(str))
        return  extracted_list, len(file)
    except Exception:
        return [], 0

def save_to_csv_pmid_of_extracted_abstracts(output_dir, save_file_name):
    pmid_extracted_list = [x[:-4] for x in os.listdir(output_dir) if x.endswith('xml')]
    df = pd.DataFrame(pmid_extracted_list)
    df.to_csv(save_file_name, index=False, sep=',', header=None)
    # extracted_list = pd.read_csv(save_file_name, header=None)


# %%
# Zipping files
def get_all_file_paths(directory):
  
    # initializing empty file paths list
    file_paths = []
  
    # crawling through directory and subdirectories
    for root, directories, files in os.walk(directory):
        for filename in files:
            # join the two strings in order to form the full filepath.
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)
  
    # returning all file paths
    return file_paths        
  
def zip_files(directory, zip_name):
    
    # path to folder which needs to be zipped
    # directory = './python_files'
  
    # calling function to get all file paths in the directory
    file_paths = get_all_file_paths(directory)
  
    # printing the list of all files to be zipped
    # print('Following files will be zipped:')
    # for file_name in file_paths:
    #     print(file_name)
  
    # writing files to a zipfile
    # abs_src = os.path.abspath(directory.parents[0])
    abs_src = str(directory.parents[0])
    # arcname
    
    with ZipFile(str(directory.parents[0]) + '/' + f'{zip_name}.zip', 'w') as zip:
        # writing each file one by one
        for file in file_paths:
            absname = file
            arcname = absname[len(abs_src) + 1:]
            zip.write(absname, arcname)
  
    print(f'All files in "{directory}" zipped successfully!')