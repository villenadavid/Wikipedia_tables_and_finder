# -*- coding: utf-8 -*-
"""
Created on Tue Mar  1 00:52:16 2022

@author: div
"""

import pandas as pd
import difflib

table_df = pd.read_csv('out.csv', delimiter='\t', header=None, names=['names', 'summary'] )

user_string = input("Please enter a string (maximum 4 words):\n")
words_to_find = user_string.split()

word1 = words_to_find[0]
word2 = words_to_find[1]
word3 = words_to_find[2]
word4 = words_to_find[3]

print('Procesing ... \n')



table_df['names_split'] = ''
table_df['summary_split'] = ''
table_df['score1'] = '0'
table_df['score2'] = '0'
table_df['score3'] = '0'
table_df['score4'] = '0'
table_df['final_score'] = '0'

table_df['summary'] = table_df['summary'].astype(str)


for index, row in table_df.iterrows():                              # Interact per row
    row['summary_split'] = row['summary'].split()
    row['names_split'] = row['names'].split()
    
    for x in row['names_split'] + row['summary_split']:             # intereact per word
        aux1 = difflib.SequenceMatcher(None, x, word1).ratio()
        row['score1'] = str(max(aux1, float(row['score1'])))
        
        aux2 = difflib.SequenceMatcher(None, x, word2).ratio()
        row['score2'] = str(max(aux2, float(row['score2'])))
        
        aux3 = difflib.SequenceMatcher(None, x, word3).ratio()
        row['score3'] = str(max(aux3, float(row['score3'])))
        
        aux4 = difflib.SequenceMatcher(None, x, word4).ratio()
        row['score4'] = str(max(aux4, float(row['score4'])))
    
    row['final_score'] = str(float(row['score1'])+float(row['score2'])+float(row['score3'])+float(row['score4']))

max_index = table_df['final_score'].astype(float).idxmax()    

print(f'You entered the words: {words_to_find[0:4]} and the best match is:\n{table_df["names"][max_index]}\nWith a score of: {table_df["final_score"][max_index]}')


 