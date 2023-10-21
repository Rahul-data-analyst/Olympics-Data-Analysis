import numpy as np


# def medal_tally(df_summer):
#     medals_tally = df_summer.drop_duplicates(
#         subset=['Team', 'NOC', 'Games', 'Year', 'Season', 'City', 'Sport', 'Event', 'Medal'])
#
#     medals_tally = medals_tally.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
#                                                                                                   ascending=False).reset_index()
#
#     medals_tally['Total'] = medals_tally['Gold'] + medals_tally['Silver'] + medals_tally['Bronze']
#
#     return medals_tally


def country_years_list(df_summer):
    years = df_summer['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')

    countries = np.unique(df_summer['region'].dropna().values).tolist()
    countries.sort()
    countries.insert(0, 'Overall')

    return years, countries


def fetch_year_country(df_summer, years, countries):
    df_YC = df_summer.drop_duplicates(
        subset=['Team', 'NOC', 'Games', 'Year', 'Season', 'City', 'Sport', 'Event', 'Medal'])
    flag = 0

    if years == 'Overall' and countries == 'Overall':
        fetch_df = df_YC
    if years == 'Overall' and countries != 'Overall':
        flag = 1
        fetch_df = df_YC[df_YC['region'] == countries]
    if years != 'Overall' and countries == 'Overall':
        fetch_df = df_YC[df_YC['Year'] == int(years)]
    if years != 'Overall' and countries != 'Overall':
        fetch_df = df_YC[(df_YC['Year'] == int(years)) & (df_YC['region'] == countries)]

    if flag == 1:
        x = fetch_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year').reset_index()

    else:
        x = fetch_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
                                                                                       ascending=False).reset_index()
    x['Total'] = x['Gold'] + x['Silver'] + x['Bronze']

    return x


def participating_nations_over_time(df_summer):
    nations_over_year = df_summer.drop_duplicates(['Year', 'region'])['Year'].value_counts().reset_index().sort_values(
        'Year')
    nations_over_year.rename(columns={'Year': 'Edition', 'count': 'No. of Countries'}, inplace=True)

    return nations_over_year


def participating_data_over_time(df_summer, col):
    events_over_year = df_summer.drop_duplicates(['Year', col])['Year'].value_counts().reset_index().sort_values(
        'Year')
    events_over_year.rename(columns={'Year': 'Edition', 'count': col}, inplace=True)

    return events_over_year


def most_successful(df_summer, sport):
    temp_df = df_summer.dropna(subset=['Medal'])

    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]

    x = temp_df['Name'].value_counts().reset_index().head(15).merge(df_summer, how='left')[
        ['Name', 'count', 'Sport', 'region']].drop_duplicates('Name')
    x.rename(columns={'count': 'Medals', 'region': 'Country'}, inplace=True)
    return x


def country_year_medalTally(df_summer, country):
    new_df = df_summer.dropna(subset='Medal')
    new_df = new_df.drop_duplicates(
        subset=['Team', 'NOC', 'Games', 'Year', 'Season', 'City', 'Sport', 'Event', 'Medal'])
    new_df = new_df[new_df['region'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()

    return final_df


def country_event_heatmap(df_summer, country):
    new_df = df_summer.dropna(subset='Medal')
    new_df = new_df.drop_duplicates(
        subset=['Team', 'NOC', 'Games', 'Year', 'Season', 'City', 'Sport', 'Event', 'Medal'])
    final_df = new_df[new_df['region'] == country]
    pt = final_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0)

    return pt


def most_successful_country_wise(df_summer, country):
    temp_df = df_summer.dropna(subset=['Medal'])

    temp_df = temp_df[temp_df['region'] == country]

    x = temp_df['Name'].value_counts().reset_index().head(10).merge(df_summer, how='left')[
        ['Name', 'count', 'Sport']].drop_duplicates('Name')
    x.rename(columns={'count': 'Medals'}, inplace=True)
    return x


def men_vs_women(df_summer):
    athlete_df = df_summer.drop_duplicates(subset=['Name', 'region'])

    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

    final = men.merge(women, on='Year', how='left')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)

    final.fillna(0, inplace=True)

    return final
