import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

pop_cmr = pd.read_excel('icd_populated.xlsx')
ko_df = pd.read_excel('ko-supp.xlsx')

clis = list(ko_df['ICD9 for D1'])
c_pop = list(pop_cmr['ICD-9 (Disease)'])

iad0 = []
iad1 = []
iad2 = []
iad3 = []
scr = []

for i in pop_cmr['ICD-9 (Disease)']:
  if i not in clis:
    continue
  else:
    ind = [index for index, value in enumerate(clis) if value == i] #Find all indexes of the searched disease in literature disease-list
    icd_d2 = ko_df['ICD9 for D2'][ind] # Finding the indexes of the corresponding comorbid diseases with i
    rr_d2 = ko_df['RR'][ind]
    dsc_d1 = ko_df['description'][ind]
    dsc_d2 = ko_df['description.1'][ind]
    for i2 in icd_d2:
      if i2 in c_pop:
        indx = [index for index, value in enumerate(icd_d2) if value == i2]
        for k in indx:
  
          iad0.append(list(dsc_d1)[k])
          iad1.append(i)        
          iad2.append(list(icd_d2)[k])
          iad3.append(list(dsc_d2)[k])
          scr.append(list(rr_d2)[k])
final = pd.DataFrame(zip(iad0, iad1, iad2, iad3, scr),columns=['Disease-1','ICD-1','ICD-2','Disease-2','RR'])
final = final.drop_duplicates(subset=['Disease-1','ICD-1','ICD-2','Disease-2','RR'], keep=False)
multi_chec = ko_df[ko_df['ICD9 for D1'].isin(pop_cmr['ICD-9 (Disease)']) & ko_df['ICD9 for D2'].isin(pop_cmr['ICD-9 (Disease)'])] # Alternative function that makes the same thing with above
list_icd = list(pop_cmr['ICD-9 (Disease)'])
list_dis = list(pop_cmr['Disease'])	


for i in range(len(final)):
  ind1 = list_icd.index(list(final['ICD-1'])[i])
  ind2 = list_icd.index(list(final['ICD-2'])[i])
  final['Disease-1'][i] = list_dis[ind1]
  final['Disease-2'][i] = list_dis[ind2]
final_ovr_15 = final[final.RR>1.5]
df_o15 = final_ovr_15.pivot_table(index='Disease-1', columns='Disease-2', values='RR')


fig, ax = plt.subplots(figsize=(65,35))   
fig = sns.clustermap(df_o15,cmap="flare", xticklabels=True, yticklabels=True, linewidths=0.1, linecolor='black', vmin=1.5, vmax=20)
ax.figure.savefig("disease_heatmap_modified.pdf", dpi=600) 
