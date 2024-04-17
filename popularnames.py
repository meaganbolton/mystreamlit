import pandas as pd
import plotly.express as px
import streamlit as st

st.title('Popular Name Trends')


# url = 'https://github.com/esnt/Data/raw/main/Names/popular_names.csv'
df = pd.read_csv("C:/Users/meaga/Stat386Labs/-Unveiling-Insights-Exploring-Data-Science-Job-Market-Dynamics/df_glassdoor.csv")


city = st.text_input('Enter a city', value='Houston')
################################################################333
# Filter data for the selected city
city_df = df[df['City'] == city]

st.header(f'{city} over time')

tab1, tab2 = st.tabs(['City','State'])
# Calculate average, min, and max salaries for each city
city_salary_stats = city_df.groupby('City').agg({'Salary Estimate': ['mean', 'min', 'max']}).reset_index()
with tab1:
    # plot_df = city_df[city_df['sex']=='F']
    fig = px.bar(city_salary_stats, 
                y='City', 
                x=['mean', 'min', 'max'], 
                orientation='h',
                barmode='group',
                labels={'value': 'Salary ($)', 'variable': 'Statistic'},
                title=f'Salary Comparison for {city}',
                color_discrete_map={'mean': 'blue', 'min': 'red', 'max': 'green'},
                )
    st.plotly_chart(fig)
# Calculate average, min, and max salaries for each city
state_salary_stats = city_df.groupby('State').agg({'Salary Estimate': ['mean', 'min', 'max']}).reset_index()
with tab1:
    # plot_df = city_df[city_df['sex']=='F']
    fig = px.bar(state_salary_stats, 
                y='City', 
                x=['mean', 'min', 'max'], 
                orientation='h',
                barmode='group',
                labels={'value': 'Salary ($)', 'variable': 'Statistic'},
                title=f'Salary Comparison for {city}',
                color_discrete_map={'mean': 'blue', 'min': 'red', 'max': 'green'},
                )
    st.plotly_chart(fig)
