# -*- coding: utf-8 -*-
"""
Created on Tue Oct 18 20:39:11 2022

@author: medici
"""

import re
import os
import pandas as pd
from collections import Counter

os.chdir("D:\\DDog\\analysis\\data_cleansing")

path_data = "data\\"
#import pandas as pd
#%%

table = pd.read_csv(path_data+"data.csv")

#%%

f = lambda x: x.split('/')[-1]
table_sub = table[['Path']].applymap(f)
table_sub.to_csv(path_data+"data_reshaped.csv")

#%%
f = lambda x: x.split('/')[:-1]
table_sub = table[['Path']].applymap(f)
table_sub.to_csv(path_data+"data_reshaped.csv")

#%%

df = pd.DataFrame({'col1':['A','B','C'],'col2':['black berry','green apple','red wine'],'col3':['black','green','red']})

#%%
f = lambda x: x.strip()
table_df['clean'] = table_df[['Table']].applymap(f)

#%%
df['col2'] = [a.replace(b, '').strip() for a, b in zip(df['col2'], df['col3'])]

table_df = pd.DataFrame(table)
table_df['Path'] = [a.replace(b, '').strip() for a, b in zip(table_df['Path'],table_df['clean'])]

#%% test 2

def ind(a):
    if(bool(re.search('lsx',a))):
        return "ind_xls"
    elif(bool(re.search('qvd',a))):
        return "nonsensitive"
    else:
        return "not"

table['Ind'] = table[['Path']].applymap(ind)
# bool(re.search('abc','dda bcdesf'))
#[a.replace(b, '').strip() for a, b in zip(table['Path'],table['Clean'])]

#%%

# df['col1'] = df['col1'].replace(0,df['col2'])
table.Path.replace(0,table.Table,inplace=True)

#table['sub_path'] = table['Path'].replace(0,table['Table'])
#%%
# str.isdigit
path = "pong/Pong.hack" # storage
# if @ ( is coupled for a symbol, the it is a symbol, give a value for it based on (
# if it is not coupled, give value from 0

# Symbol dictionary
array_symbol = []
array_symbolJmp = []
array_symbolJmpOri = []
