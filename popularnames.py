import pandas as pd
import plotly.express as px
import streamlit as st

st.title('Popular Name Trends')

url = 'https://raw.githubusercontent.com/meaganbolton/-Unveiling-Insights-Exploring-Data-Science-Job-Market-Dynamics/main/df_glassdoor.csv'
df = pd.read_csv(url)

# Get the list of all unique cities and states
all_cities = df['City'].unique()
all_states = df['State'].unique()

# Create checkboxes for selecting cities
selected_cities = st.multiselect('Select cities', all_cities, default=all_cities)

# Create select box for pay rate
pay_rate = st.selectbox("Pay Rate", ('Hourly', 'Yearly'))

# Filter data for the selected cities
city_df = df[df['City'].isin(selected_cities)]

# Check if city_df is empty
if city_df.empty:
    st.write("No data found for the selected cities. Please select other cities.")
else:
    # Filter data based on pay rate
    city_df = city_df[city_df['Pay rate'] == pay_rate]

    # Calculate average, min, and max salaries for each city
    city_salary_stats = city_df[['City', 'Salary_Min', 'Salary_Max']].groupby('City').mean().reset_index()

    # Plotting the bar chart for cities
    fig = px.bar(city_salary_stats, 
                 y='City', 
                 x=['Salary_Min', 'Salary_Max'], 
                 orientation='h',
                 barmode='group',
                 labels={'value': 'Salary ($)', 'variable': 'Statistic'},
                 title=f'Salary Comparison for Selected Cities ({pay_rate} pay rate)',
                 color_discrete_map={'Salary_Min': 'red', 'Salary_Max': 'blue'},
                 )

    # Show the bar chart for cities
    st.plotly_chart(fig)
