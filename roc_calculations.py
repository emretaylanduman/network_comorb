import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile

import math
import pylab as pl
from pylab import *
import numpy as np
import scikitplot as skplt
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from sklearn.metrics import roc_curve, auc
from scipy import interpolate
from sklearn import metrics

fin_res_cancerless = pd.read_excel('similarity_covid_cancerless2x.xlsx')
fin_res_cancerless_pvt = fin_res_cancerless.pivot_table(index='disease1_name', columns='disease2_name', values='similarity',dropna = False)

daf = daf.drop_duplicates(subset='Score-Similarity', keep="last")
daf.drop(daf.tail(1).index,inplace=True)

dass = daf[daf['Score-Kendall']>0.95] # Highly comorbid and highly correlated
dast = daf[(daf['Score-Pearson']>0.95) & (daf['Score-Similarity']<0.85)]

#Final data obtained from previous codes. Two excel file has been merged by droping the scores of not-comorbid list
#final_limited = pd.read_excel('scores_kendall_limited_cancerless_finalized.xlsx')
#final_full_score = pd.read_excel('all_scores_kendall_limited_cancerless_tf_09.xlsx')
final_full_score_cancerless = pd.read_excel('all_scores_spearman_limited_cancerless_09.xlsx')

#final_full_score_pearson = pd.read_excel('scores_pearson_limited_cancerless_high_low.xlsx')
#final_full_score_spearman = pd.read_excel('scores_spearman_limited_cancerless_high_low.xlsx')
#full_score_without_correction = pd.read_excel('comp_icd_cancerless_cov.xlsx')
#cancerless_tf = pd.read_excel('similarity-covid_cancerless_tf.xlsx')

df_clinical = pd.read_excel('clinical_disease.xlsx')
df_new = pd.read_excel('rev_over_12_RR.xlsx')
 #Adding clinical (4000 RR scored literature comorbidity data) and previously used data from the paper
total_disease = list(set(df_clinical['Disease-1'])) + list(set(df_clinical['Disease-2']))
total_disease2 = list(set(df_new['Disease-1'])) + list(set(df_new['Disease-2'])) + total_disease

# y-scores implemented function of collect_scores also writes the xlsx file as output

def collect_scores2(inp,dis_list,dis_df,name):
  alt_dis_1 = []
  alt_dis_2 = []
  alt_sc = []
  for i in dis_list:
    ind = [index for index, value in enumerate(inp.disease1_name) if value == i]
    for ina in ind:
      pro = inp.disease2_name[ina]
      if pro in dis_list:
        alt_dis_1.append(i)
        alt_dis_2.append(pro)
        alt_sc.append(inp.similarity[ina])
  df = pd.DataFrame(list(zip(alt_dis_1, alt_dis_2,alt_sc)), columns =['Disease-1', 'Disease-2', 'Score'])
  df['y'] = ''
  list1_disease = list(df['Disease-1'])
  list2_disease = list(df['Disease-2'])
  for i in range(len(list1_disease)):
    less_a1 = dis_df['Disease-2'][dis_df['Disease-1'].str.contains(list1_disease[i])]
    less_b1 = dis_df['Disease-1'][dis_df['Disease-2'].str.contains(list1_disease[i])]

    less_x = list(less_b1) + list(less_a1)

    if list2_disease[i] in less_x:
      df['y'][i]='1'
    else:
      df['y'][i]='0'
  df['y'] = pd.to_numeric(df['y'])
  file_name = 'comp_' + str(name) + '.xlsx'
  #df.to_excel(file_name)
  return(df)

cancerless_09 = collect_scores2(final_full_score_cancerless,total_disease2,df_clinical,'reproduced')

def prepare_roc(f_name):
  fname = str(f_name)
  df = pd.read_excel(fname)
  y_true = df['y']
  y_probas = df['Score']
  fpr, tpr, thresholds = roc_curve(y_true, y_probas)
  return(fpr,tpr)

y_true_cancer_full_score = cancerless_09['y']
y_probas_cancer_full_score = cancerless_09['Score']
fpr_full_score, tpr_full_score, thresholds_full_score = roc_curve(y_true_cancer_full_score, y_probas_cancer_full_score)
rep_auc = auc(fpr_full_score,tpr_full_score)
plt.plot(fpr_full_score, tpr_full_score, marker='.', label='Spearman 0.9-C.less-Extended Data (AUC = %0.2f)' % rep_auc)
#plt.plot(fpr_cancer_tf, tpr_cancer_tf, marker='.', label='Cancer-TF')
#plt.plot(fpr_cless, tpr_cless, marker='.', label='Cancerless')

# axis labels
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.plot([0, 1], [0, 1], color='black', linestyle='--')
# show the legend
plt.legend()
# show the plot

plt.show()
