# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.10.3
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

from functools import partial
import pandas as pd
from pyrfume import get_cids, from_cids

# +
behavior_1 = pd.read_excel('DravnieksGrid.xlsx', sheet_name='App', index_col=0)

def fix(s):
    return s.replace("'", "").replace('Arnine', 'Amine')

behavior_1.index = behavior_1.index.map(fix)
behavior_1.columns = behavior_1.columns.map(fix)

behavior_2 = pd.read_excel('DravnieksGrid.xlsx', sheet_name='Use', index_col=0)#.set_index('CAS')
behavior_2.index = behavior_2.index.map(fix)
behavior_2.columns = behavior_2.columns.map(fix)
# -

raw = pd.read_excel('Dravnieks_molecules.xlsx').set_index('Name')
raw['Conc'] = raw.index.map(lambda x: 'low' if 'low' in x.lower() else 'high')

raw.loc['Hexenal-trans1', 'CID'] = 5281168
raw.loc['Sandiff', 'CID'] = 103005
raw.loc['Tetraquinone', 'CID'] = 5424
raw.loc['PhenylEthanolhighconc', 'CID'] = 6054
raw.loc['PhenylEthanollowconc', 'CID'] = 6054
raw.loc['Diola', 'CID'] = 78484
#raw.loc['MethylAcetaldehydeDiAce', 'CID'] = 8503 # Speculative

behavior_1.index = behavior_1.index.map(raw['CID'].xs)
behavior_2.index = behavior_2.index.map(raw['CID'].xs)
behavior_1 = behavior_1[behavior_1.index.notnull()]
behavior_2 = behavior_2[behavior_2.index.notnull()]
behavior_1.index = behavior_1.index.astype(int)
behavior_2.index = behavior_2.index.astype(int)
behavior_1.to_csv('behavior_1.csv')
behavior_2.to_csv('behavior_2.csv')

molecules = pd.DataFrame(from_cids(behavior_1.index.tolist())).set_index('CID')
molecules.to_csv('molecules.csv')



