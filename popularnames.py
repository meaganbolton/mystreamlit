import pandas as pd
import plotly.express as px
import streamlit as st

st.title('Popular Name Trends')

url = 'https://raw.githubusercontent.com/meaganbolton/-Unveiling-Insights-Exploring-Data-Science-Job-Market-Dynamics/main/df_glassdoor.csv'
df = pd.read_csv(url)

# Get the list of all unique cities and states
all_cities = df['City'].unique()
all_states = df['State'].unique()

# Create radio buttons for selecting cities or states
chart_type = st.radio("Select Chart Type", ('Cities', 'States'))

# Create select box for pay rate
pay_rate = st.selectbox("Pay Rate", ('Hourly', 'Yearly'))

if chart_type == 'Cities':
    # Filter cities based on selected pay rate
    if pay_rate == 'Hourly':
        available_cities = df[df['Pay rate'] == 'Hourly']['City'].unique()
    else:
        available_cities = df[df['Pay rate'] == 'Yearly']['City'].unique()

    # Create checkboxes for selecting cities
    selected_cities = st.multiselect('Select cities', available_cities, default=available_cities)

    # Filter data for the selected cities
    city_df = df[df['City'].isin(selected_cities)]

    # Check if city_df is empty
    if city_df.empty:
        st.write("No data found for the selected cities. Please select other cities.")
    else:
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
else:
    # Filter states based on selected pay rate
    if pay_rate == 'Hourly':
        available_states = df[df['Pay rate'] == 'Hourly']['State'].unique()
    else:
        available_states = all_states

    # Create checkboxes for selecting states
    selected_states = st.multiselect('Select states', available_states, default=available_states)

    # Filter data for the selected states
    state_df = df[df['State'].isin(selected_states)]

    # Check if state_df is empty
    if state_df.empty:
        st.write("No data found for the selected states. Please select other states.")
    else:
        # Calculate average, min, and max salaries for each state
        state_salary_stats = state_df[['State', 'Salary_Min', 'Salary_Max']].groupby('State').mean().reset_index()

        # Plotting the bar chart for states
        fig = px.bar(state_salary_stats, 
                     y='State', 
                     x=['Salary_Min', 'Salary_Max'], 
                     orientation='h',
                     barmode='group',
                     labels={'value': 'Salary ($)', 'variable': 'Statistic'},
                     title=f'Salary Comparison for Selected States ({pay_rate} pay rate)',
                     color_discrete_map={'Salary_Min': 'red', 'Salary_Max': 'blue'},
                     )

        # Show the bar chart for states
        st.plotly_chart(fig)
