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




answer_cols = possible_answers.columns

path = 'all_results.xlsx'
writer = pd.ExcelWriter(path, engine="xlsxwriter")

workbook = writer.book
wrap_format = workbook.add_format({'text_wrap': True})

for i, theme in enumerate(answer_cols):
    print(theme)
    list_possible_answers = list(possible_answers[theme].dropna())
    out = 100 * get_multiple_answer_distribution(df_all, theme, list_possible_answers)
    out.style.highlight_max(color='yellow').highlight_max(color='pink', axis=1).to_excel(writer, float_format='%.0f', sheet_name='Sheet_%d' %i, header=False, startrow=2)
    worksheet = writer.sheets['Sheet_%d' %i]
    worksheet.set_column(1, 15, 18, wrap_format)
    worksheet.set_column(0, 0, 17,)
    # Add a header format.
    header_format = writer.book.add_format(
        {
            "text_wrap": True,
            "fg_color": "#D7E4BC",
            "border": 1,
        }
    )
    # Write the column headers with the defined format.
    for col_num, value in enumerate(out.columns.values):
        worksheet.write(1, col_num + 1, value, header_format)
    worksheet.write(0, 0, theme)


writer.close()
