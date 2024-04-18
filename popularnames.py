import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.title('Glassdoor Data Science Jobs Data')

url = 'https://raw.githubusercontent.com/meaganbolton/-Unveiling-Insights-Exploring-Data-Science-Job-Market-Dynamics/main/df_glassdoor.csv'
df = pd.read_csv(url)


with st.sidebar:
    job = st.text_input('Enter a keyword to filter job titles by', value='Data')
    jobDf = df[df['Job Title'].str.lower().str.contains(job.lower())].dropna()
    
    
    jobDf = jobDf.set_index('Job Title')
    print(jobDf)
    st.dataframe(jobDf)


# Get the list of all unique cities and states
all_cities = df['City'].dropna().unique()
all_states = df['State'].dropna().unique()

# Create radio buttons for selecting cities or states
chart_type = st.radio("Select Chart Type", ('Cities', 'States'))

# Create select box for pay rate
pay_rate = st.selectbox("Pay Rate", ('Hourly', 'Yearly'))

if chart_type == 'Cities':
    # Filter cities based on selected pay rate
    if pay_rate == 'Hourly':
        available_cities = df[df['Pay rate'] == 'Hourly']['City'].dropna().unique()

    else:
        available_cities = df[df['Pay rate'] == 'Yearly']['City'].dropna().unique()


    # Create checkboxes for selecting cities
    selected_cities = st.multiselect('Select cities', available_cities, default=available_cities)

    # Filter data for the selected cities
    city_df = df[df['City'].isin(selected_cities)]

    # Check if city_df is empty
    if city_df.empty:
        st.write("No data found for the selected cities. Please select other cities.")
    else:
        # Calculate average, min, and max salaries for each city
        if pay_rate == "Hourly":
            city_df = df[(df['City'].isin(selected_cities)) & (df['Pay rate'] == 'Hourly')]
        else:
            city_df = df[(df['City'].isin(selected_cities)) & (df['Pay rate'] == 'Yearly')]

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
        available_states = df[df['Pay rate'] == 'Hourly']['State'].dropna().unique()
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
        if pay_rate == "Hourly":
            state_df = df[(df['State'].isin(selected_states)) & (df['Pay rate'] == 'Hourly')]
        else:
            state_df = df[(df['State'].isin(selected_states)) & (df['Pay rate'] == 'Yearly')]
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


# Filter out rows with null values in 'State', 'Rating', 'Salary_Min', and 'Salary_Max' columns
filtered_df = df.dropna(subset=['State', 'Rating', 'Salary_Min', 'Salary_Max'])

# Calculate average, min, and max salaries for each state
state_salary_stats = filtered_df.groupby('State').agg({
    'Rating': 'mean',
    'Salary_Min': 'mean',
    'Salary_Max': 'mean'
}).reset_index()

# Create the figure
fig = go.Figure()

# Add bar chart for the minimum salary range
fig.add_trace(go.Box(
    y=filtered_df['State'],
    x=filtered_df['Salary_Min'],
    name='Min Salary',
    orientation='h',
    boxmean = True,
    marker_color='red'
))
print(state_salary_stats)

# Add bar chart for the maximum salary range
fig.add_trace(go.Box(
    y=filtered_df['State'],
    x=filtered_df['Salary_Max'],
    name='Max Salary',
    orientation='h',
    boxmean = True,
    marker_color='blue'
))

# Add box plot for company ratings
fig.add_trace(go.Box(
    y=filtered_df['State'],
    x=filtered_df['Rating'],
    name='Company Ratings',
    orientation='h',
    boxmean=True
))

# Update layout
fig.update_layout(
    title='Company Ratings and Salary Ranges by State',
    xaxis=dict(title='Rating / Salary'),
    yaxis=dict(title='State'),
    barmode='group'
)

# Show the combined chart
st.plotly_chart(fig)


# st.plotly_chart(fig)
filtered_df = df.dropna(subset=['State', 'Estimate', 'Company', 'Salary_Min', 'Salary_Max'])

# Filter out NaN values from the 'State' column
filtered_states = filtered_df['State'].dropna().unique()

# Generate a unique key for the multiselect widget
multiselect_key = "select_states_multiselect"

# Filter states based on selection
selected_states = st.multiselect('Select states', filtered_states, filtered_states, key=multiselect_key)

# Filter data for the selected states
filtered_df = filtered_df[filtered_df['State'].isin(selected_states)]

# Determine the label for Glassdoor estimate and Employer estimate
filtered_df['Estimate_Type'] = filtered_df['Estimate'].apply(lambda x: 'Glassdoor' if 'Glassdoor' in x else 'Employer')

# Create the figure
fig = px.scatter(
    filtered_df,
    x="Salary_Min",
    y="Salary_Max",
    color=filtered_df['Estimate_Type']
)
st.plotly_chart(fig)
