import pandas as pd
import numpy as np
import plotly.express as px
from utils import get_single_answer_distribution, get_multiple_answer_distribution
from openpyxl import load_workbook


df_pap = pd.read_excel('../data/pap.xlsx')
df = pd.read_excel('../data/online.xlsx')

possible_answers = pd.read_excel('../data/possible_answers.xlsx')

# ---------- Pre-processing data --------------------------------------

dict_replace = {'Sécurité': 'Prévention et sécurité',
                'Emplois et services': 'Vie économique',
                'Famille, enfance, éducation': 'Famille, enfance, jeunesse',
                'Environnement': 'Environnement et écologie'}


df_all = pd.concat((df_pap, df))
df_all["Votre quartier"] = df_all["Votre quartier"].replace({'Bois de Verrières / Coulée Verte': 'Coulée Verte'})
df_all["Votre tranche d'âge"] = df_all["Votre tranche d'âge"].replace({'18-24': '18-34', '25-34': '18-34', 'Moins de 18 ans': '18-34'})
df_all["Votre quartier"] = df_all["Votre quartier"].replace({'Antonypole': 'Les Rabats'})

themes = [ 
    "Transports et mobilité",        
    "Environnement et écologie",   
    "Aménagement de la ville",       
    "Logement",                      
    "Sports, loisirs et culture",    
    "Santé",                         
    "Prévention et sécurité",        
    "Démocratie locale",             
    "Vie économique",                
    "Famille, enfance, jeunesse",
          ]

df_all[themes] = 0

cols = [col for col in df.columns if (col.startswith('Quel autre thème') or col.startswith('Quel premier thème souhaitez') or col.startswith('Quel autre thème'))]

for index, row in df_all.iterrows():
    for col in cols:
        if row[col] in themes:
            df_all.loc[index, row[col]] = 1


def write_formatted_table(out, path, col_width=12):
    writer = pd.ExcelWriter(path, engine="xlsxwriter")
    out.style.highlight_max(color='yellow').highlight_max(color='pink', axis=1).to_excel(writer, float_format='%.0f', header=False, startrow=1)
    wrap_format = writer.book.add_format({'text_wrap': True})
    worksheet = writer.sheets["Sheet1"]
    worksheet.set_column(0, 0, 17)
    worksheet.set_column(1, 15, col_width, wrap_format)
    # Add a header format.
    header_format = writer.book.add_format(
        {
            "bold": True,
            "text_wrap": True,
            "fg_color": "#D7E4BC",
            "border": 1,
        }
    )
    # Write the column headers with the defined format.
    for col_num, value in enumerate(out.columns.values):
        worksheet.write(0, col_num + 1, value, header_format)
    writer.close()



path = 'who_answered_what_quartier.xlsx'
out = df_all[themes + ["Votre quartier"]].groupby("Votre quartier").mean()
write_formatted_table(100 * out, path)

out = df_all[themes + ["Votre tranche d'âge"]].groupby("Votre tranche d'âge").mean()
write_formatted_table(100 * out, 'who_answered_what_age.xlsx')
