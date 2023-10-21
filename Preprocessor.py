import pandas as pd


def preprocess(df_summer,df_region):

    # Merge with region df
    df_summer = df_summer.merge(df_region, on='NOC', how='left')

    # dropping duplicates

    # df_summer.drop_duplicates(inplace=True)

    # adding total medals columns in dataframe

    df_summer = pd.concat([df_summer, pd.get_dummies(df_summer['Medal'])], axis=1)

    return df_summer
