from urllib.parse import unquote
from src.shared.lambdaHelper import LambdaHelper
import traceback
from src.shared.generalWrapper import GeneralWrapper
from datetime import datetime
import pandas as pd
import numpy as np
import h5py as h5
import os
import urllib.request
import re
import requests
import time
from collections import Counter
from src.shared.database import Database

def lambda_handler(event, context):
    query = LambdaHelper.getPathParam(event, 'proxy')
    term= LambdaHelper.getQueryStringParam(event, 'term', LambdaHelper.valueTypeString, '')
    term = unquote(term)
    return drugShotSearch(term)

def query_ncbi(searchterm, api_key):
    countMax = 1000000
    pagestep = 1000000
    going = True
    i = 0
    pmids = []
    while going:

        url = ("https://eutils.ncbi.nlm.nih.gov"+
            "/entrez/eutils/esearch.fcgi"+
            "?db=pubmed&term="+searchterm+
            "&retstart="+str(i*pagestep)+
            "&retmax="+str(pagestep)+
            "&api_key="+api_key)
        
        page = requests.get(url).text
        pmids = pmids + re.findall(r'Id>(.*?)<', page)
        if i==0:
            countMax = int(re.findall(r'Count>(.*?)<', page)[0])
        if i*pagestep > countMax:
            going = False

        i += 1
    return np.array(pmids).astype(int)
    
    
def search(term):
    searchterm = term
    dbConnection = (Database())
    db = dbConnection.db
    existedSearchResult = db.drugshot_search.find_one({'search_term' : searchterm}, {'_id' : 0, 'search_term' : 1, 'PubMedID_count' : 1, 'drug_count' : 1, 'return_size' : 1, 'query_time' : 1})
    if not (existedSearchResult is None):
        return existedSearchResult
    stime = time.time()
    api_key = 'b3306b67e2b30d79ca1c776ceb0047d0a508'
    #print ('before query ' + datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])
    queryResult = query_ncbi(searchterm, api_key)
    #print ('after query ' + datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])
    autorif = pd.read_csv('/mnt/drugshot/AutoRIF.tsv.gz',sep = '\t',usecols = ['name','PMID']).set_index('PMID')
    #print ('after reading data ' + datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])
    autorif_counts = dict(Counter(autorif['name']))
    #print ('after defining autorif_counts ' + datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])
    associated_drug_counts = autorif.loc[ list(set(autorif.index).intersection(set(queryResult)))]
    #print ('after associated_drug_counts ' + datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])
    total_counts = autorif_counts
    drug_counts = dict(Counter(associated_drug_counts.iloc[:,0]))
    drug_count = {}
    return_size = 0
    for (key, value) in drug_counts.items():
        return_size = return_size+1
        drug_count[str(key)] = [value, value/total_counts[key]]

    response = {'search_term': searchterm,
                'PubMedID_count': len(queryResult),
                'drug_count': drug_count,
                'return_size': return_size,
                'query_time': time.time()-stime
                }
    db.drugshot_search.insert_one(response)
    if '_id' in response:
        del response['_id']
    #print ('end ' + datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])
    return response

def drugShotSearch(term):
    try:
        result = search(term)
        return GeneralWrapper.successResult(result)
    except Exception as e:
        traceback.print_exc()
        return GeneralWrapper.generalErrorResult(e)
