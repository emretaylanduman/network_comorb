import pandas as pd

tm_df = pd.read_table('hsa.tsv', names=['tf', 'mirna','type']) #Transcription factor mirna network
tg_df = pd.read_table('TF_gene_list_human (1)', sep='\t') #Human interactome network

tg_df2 = tg_df[['TF','gene']]
df_tr = tg_df2[tg_df2['TF'].isin(tm_df['tf'])]
df_tr_2 = df_tr[df_tr['gene'].isin(list(tm_df['tf']))]
df_tr_2 = df_tr_2.reset_index()
df_tr_2 = df_tr_2[['TF','gene']]
df_tr_2.to_csv('tf_tf_list.csv',sep='\t')
