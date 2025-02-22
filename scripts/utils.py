import pandas as pd
import numpy as np
import plotly.express as px


def get_single_answer_distribution(df_all, col, answer, mode='quartier'):
    """
    Parameters
    ----------

    df_all: pd.DataFrame
        The original dataframe
    col: str
        A column of df_all, corresponding to a multiple-choice question
    answer: str
        One of the answers of col
    """
    df = pd.DataFrame(df_all.dropna(subset=[col]))
    df[answer] = 0
    for index, row in df.iterrows():
        if answer in row[col]:
            df.loc[index, answer] = 1
    if mode == 'quartier':
        return(df[[answer, "Votre quartier"]].groupby("Votre quartier").mean().reset_index().sort_values(by=answer, ascending=False))
    else:
        return(df[[answer, "Votre tranche d'âge"]].groupby("Votre tranche d'âge").mean().reset_index())


def get_multiple_answer_distribution(df_all, col, answers, mode='quartier'):
    """
    Parameters
    ----------

    df_all: pd.DataFrame
        The original dataframe
    col: str
        A column of df_all, corresponding to a multiple-choice question
    """
    col = col.replace("\xa0", " ")
    df = pd.DataFrame(df_all.dropna(subset=[col]))
    df[answers] = 0
    for index, row in df.iterrows():
        for answer in answers:
            if answer in row[col]:
                df.loc[index, answer] = 1
    if mode == 'quartier':
        return(df[answers + ["Votre quartier"]].groupby("Votre quartier").mean())
    else:
        return(df[[answer, "Votre tranche d'âge"]].groupby("Votre tranche d'âge").mean().reset_index())


def plot_answers(df, col):
    fig = px.bar(df, x=col, orientation='h')
