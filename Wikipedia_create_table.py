# -*- coding: utf-8 -*-
"""
Created on Mon Feb 28 09:40:43 2022

@author: div
"""

import re
import csv
import requests


def find_summary(link):

    url = "https://en.wikipedia.org/w/api.php"
    print(link)
   
    parameters = {
            'action': 'query',
            'format': 'json',
            'titles': link,
            'prop': 'extracts',
            'exintro': 1,
            'explaintext': 1
    }
       
    summary_json = requests.get(url=url, params=parameters).json()
    try:
        webpage_summary = next(iter(summary_json['query']['pages'].values()))['extract']
        return(re.sub('\n', '', webpage_summary))
    except:
        if ('(' or ')') in link:
            link = (re.sub(r'\(.*?\)', '', link))
            return(find_summary(link))
        else:
            return('No webpage available for the the link: ', link)


if __name__ == "__main__":

    url = "https://en.wikipedia.org/w/api.php"
    
    parameters = {
            'action': 'parse',
            'format': 'json',
            'page': 'List_of_companies_of_Canada',
            'prop': 'wikitext',
            'section' : 2
    }
    
    webpage = requests.get(url=url, params=parameters).json()
    wikitext = webpage['parse']['wikitext']['*']
    lines = wikitext.split('}}\n{{Company-list table entry \n')
    
    final_table = []
    
    for line in lines[1:]:
        table_columns = line[2:].split('\n| ')
        if '|' in table_columns[0]:
            link = re.sub("\[\[|\]\]|''|'''", '', table_columns[0]).split('|')
            final_table = [link[1], find_summary(link[0])]                          # format [[link|name]]
        else:
            link = re.sub("\[\[|\]\]|''|'''", '', table_columns[0])
            final_table = [link, find_summary(link)]                                 # Name is simmilar as link
    
        with open('out.csv','a', newline="", encoding='utf-8') as f:
            wr = csv.writer(f,delimiter='\t')
            wr.writerow(final_table)

