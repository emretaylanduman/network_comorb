import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df_disease_mirna = pd.read_excel('dis_mirna_counts.xlsx')

search_values = ['neoplasms', 'cancer','blastoma','carcinoma','tumor','leukemia','lymphoma','sarcoma','melanoma','myeloma']

df_disease_mirna["Disease Type"]=''
for i in range(len(df_disease_mirna['Disease'])):
  lis_dis_n = df_disease_mirna['Disease'][i].split(' ')
  for k in lis_dis_n:
    if k.lower() in search_values:
      df_disease_mirna['Disease Type'][i]='Cancer'
    else:
      df_disease_mirna['Disease Type'][i]='Other Diseases'      

box_plot = sns.boxplot(x=df_disease_mirna['Disease Type'], y=df_disease_mirna['mirna'],showfliers= False, order= ['Cancer','Other Diseases'], width= 0.25, linewidth=0.5)
medians = df_disease_mirna.groupby(['Disease Type'])['mirna'].median()
vertical_offset = df_disease_mirna['mirna'].median() * 0.05

for xtick in box_plot.get_xticks():
    box_plot.text(xtick,medians[xtick] + vertical_offset,medians[xtick], 
            horizontalalignment='center',color='k')
    

box_plot.set(ylabel='Number of miRNA')
plt.savefig("boxplot_median.png",dpi=300) 

df_rest = df_rep.drop(df_cancer.index)

df_rep = df_rep.rename({'similarity': 'reproduced'}, axis='columns')
df_cancer = df_cancer.rename({'similarity': 'only_cancer'}, axis='columns')
df_rest= df_rest.rename({'reproduced': 'removed_cancer'}, axis='columns')

scr = df_rep["reproduced"].plot.hist(weights = np.ones_like(df_rep.index) / len(df_rep.index),color='b',title='Reproduced')
scr.set_xlabel('Score')

scr = df_cancer["only_cancer"].plot.hist(weights = np.ones_like(df_cancer.index) / len(df_cancer.index),color='r',title='Only Cancer')
scr.set_xlabel('Score')

scr = df_rest["removed_cancer"].plot.hist(weights = np.ones_like(df_rest.index) / len(df_rest.index),color='g',title='Without Cancer')
scr.set_xlabel('Score')
