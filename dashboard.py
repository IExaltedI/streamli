import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('day.csv', delimiter=",")
df['dteday'] = pd.to_datetime(df['dteday'])

st.title('Day Data Dashboard')

st.sidebar.title('Filter by Date')
start_date = st.sidebar.date_input('Start date', df['dteday'].min())
end_date = st.sidebar.date_input('End date', df['dteday'].max())

filtered_df = df[(df['dteday'] >= pd.to_datetime(start_date)) & (df['dteday'] <= pd.to_datetime(end_date))]

average_count_df_weather = filtered_df.groupby('weathersit')['cnt'].mean().reset_index()
average_count_df_weather.columns = ['weathersit', 'average_count']
weather_mapping = {1: "Sunny", 2: "Cloudy", 3: "Rain"}
average_count_df_weather['weathersit'] = average_count_df_weather['weathersit'].replace(weather_mapping)
ordered_categories_weather = ["Sunny", "Cloudy", "Rain"]
average_count_df_weather['weathersit'] = pd.Categorical(average_count_df_weather['weathersit'], categories=ordered_categories_weather, ordered=True)
average_count_df_weather = average_count_df_weather.sort_values(by='weathersit')

average_count_df_day = filtered_df.groupby('workingday')['cnt'].mean().reset_index()
average_count_df_day.columns = ['workingday', 'average_count']
day_mapping = {0: "Holiday", 1: "Workday"}
average_count_df_day['workingday'] = average_count_df_day['workingday'].replace(day_mapping)
ordered_categories_day = ["Holiday", "Workday"]
average_count_df_day['workingday'] = pd.Categorical(average_count_df_day['workingday'], categories=ordered_categories_day, ordered=True)
average_count_df_day = average_count_df_day.sort_values(by='workingday')

st.write('## Users Based on Weather')

fig_weather, ax_weather = plt.subplots(figsize=(10, 6))
ax_weather.bar(average_count_df_weather['weathersit'], average_count_df_weather['average_count'], color='skyblue')
ax_weather.set_xlabel('Weather Situation')
ax_weather.set_ylabel('Average User Count')
ax_weather.set_title('Average Users Based on Weather')
ax_weather.set_xticks(average_count_df_weather['weathersit'])
ax_weather.set_xticklabels(average_count_df_weather['weathersit'], rotation=45)
plt.tight_layout()
st.pyplot(fig_weather)

st.write('## Users Based on WorkDay')

fig_day, ax_day = plt.subplots(figsize=(10, 6))
ax_day.bar(average_count_df_day['workingday'], average_count_df_day['average_count'], color='skyblue')
ax_day.set_xlabel('Type of Day')
ax_day.set_ylabel('Average User Count')
ax_day.set_title('Average Users Based on Day')
ax_day.set_xticks(average_count_df_day['workingday'])
ax_day.set_xticklabels(average_count_df_day['workingday'], rotation=45)
plt.tight_layout()
st.pyplot(fig_day)

st.write('## Data Overview')
st.dataframe(filtered_df)

st.write('## Summary Statistics')
st.write(filtered_df.describe())