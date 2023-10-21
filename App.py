import streamlit as st
import pandas as pd
import Preprocessor
import Medals
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff

df_summer = pd.read_csv('Summer_Data.csv')
df_region = pd.read_csv('regions.csv')

df = Preprocessor.preprocess(df_summer, df_region)

st.sidebar.title('Olympics Data Analysis')

st.sidebar.image('https://www.sportzcraazy.com/wp-content/uploads/2018/08/Olympics-Games.jpg')

Menu_bar = st.sidebar.radio(
    'Select Your Choice',
    ('Medal Tally', 'Overall Analysis', 'Country-Wise Analysis', 'Athlete-Wise Analysis')
)

# st.dataframe(df)

if Menu_bar == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    years, countries = Medals.country_years_list(df)
    year_selected = st.sidebar.selectbox('Select Year', years)
    country_selected = st.sidebar.selectbox('Select Country Name', countries)

    medal_tally = Medals.fetch_year_country(df, year_selected, country_selected)

    if country_selected == 'Overall' and year_selected == 'Overall':
        st.title('Overall Medal Tally')
    if country_selected != 'Overall' and year_selected == 'Overall':
        st.title(country_selected + ' Overall Performance')
    if country_selected == 'Overall' and year_selected != 'Overall':
        st.title('Medal Tally in ' + str(year_selected) + ' Olympics')
    if country_selected != 'Overall' and year_selected != 'Overall':
        st.title(country_selected + ' Performance in ' + str(year_selected) + ' Olympics')

    st.table(medal_tally)

if Menu_bar == "Overall Analysis":
    edition = df['Year'].unique().shape[0] - 1
    city = df['City'].unique().shape[0]
    event = df['Event'].unique().shape[0]
    sport = df['Sport'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nation = df['region'].unique().shape[0]

    st.title('Top Statistics')

    col1, col2, col3 = st.columns(3)

    with col1:
        st.header('Editions')
        st.header(edition)

    with col2:
        st.header('Hosts')
        st.header(city)

    with col3:
        st.header('Events')
        st.header(event)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header('Sports')
        st.header(sport)

    with col2:
        st.header('Athletes')
        st.header(athletes)

    with col3:
        st.header('Nations')
        st.header(nation)

    nations_over_year = Medals.participating_data_over_time(df, 'region')
    fig = px.line(nations_over_year, x="Edition", y="region", title='Nations Over Time')
    st.header('Participating Nations Over Year')
    st.plotly_chart(fig)

    events_over_year = Medals.participating_data_over_time(df, 'Event')
    fig = px.line(events_over_year, x="Edition", y="Event", title='Events Over Time')
    st.header('Participating Events Over Year')
    st.plotly_chart(fig)

    athletes_over_year = Medals.participating_data_over_time(df, 'Name')
    fig = px.line(athletes_over_year, x="Edition", y="Name", title='Athletes Over Time')
    st.header('Participating Athletes Over Year')
    st.plotly_chart(fig)

    st.header('Number of Events Over Time based on Every Sport')
    fig, ax = plt.subplots(figsize=(30, 30))
    new_df = df.drop_duplicates(['Year', 'Event', 'Sport'])
    ax = sns.heatmap(
        new_df.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype(int),
        annot=True)
    st.pyplot(fig)

    st.header('Top Successful Athletes')
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')
    selected_sport = st.selectbox('Select a Sport', sport_list)

    x = Medals.most_successful(df, selected_sport)
    st.table(x)

if Menu_bar == 'Country-Wise Analysis':
    st.sidebar.title('Country-Wise Analysis')
    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()
    region_selected = st.sidebar.selectbox('Select a Country', country_list)

    final_df = Medals.country_year_medalTally(df, region_selected)
    fig = px.line(final_df, x="Year", y="Medal", title='Medals Over Time')
    st.header(region_selected + ' Medal Tally Over Year')
    st.plotly_chart(fig)

    pt = Medals.country_event_heatmap(df, region_selected)
    fig, ax = plt.subplots(figsize=(20, 20))
    ax = sns.heatmap(pt, annot=True)
    st.header(region_selected + ' Excels in the Following Sports')
    st.pyplot(fig)

    most10_df = Medals.most_successful_country_wise(df, region_selected)
    st.header('Top 10 Athletes of ' + region_selected)
    st.table(most10_df)


if Menu_bar == 'Athlete-Wise Analysis':
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()
    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist',
                                                'Bronze Medalist'], show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=800, height=400)
    st.header('Distribution of Age')
    st.plotly_chart(fig)

    x = []
    name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']

    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=800, height=600)
    st.header("Distribution of Age wrt Sports(Gold Medalist)")
    st.plotly_chart(fig)

    st.header("Men Vs Women Participation Over the Years")
    final = Medals.men_vs_women(df)
    fig = px.line(final, x="Year", y=["Male", "Female"])
    fig.update_layout(autosize=False, width=800, height=600)
    st.plotly_chart(fig)
