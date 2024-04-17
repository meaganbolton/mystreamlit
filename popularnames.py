import pandas as pd
import plotly.express as px
import streamlit as st

st.title('Popular Name Trends')


# url = 'https://github.com/esnt/Data/raw/main/Names/popular_names.csv'
url = 'https://raw.githubusercontent.com/meaganbolton/-Unveiling-Insights-Exploring-Data-Science-Job-Market-Dynamics/main/df_glassdoor.csv'
df = pd.read_csv(url)


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
# Plotting the bar chart
fig = px.bar(city_salary_stats, 
             y='City', 
             x=['mean', 'min', 'max'], 
             orientation='h',
             barmode='group',
             labels={'value': 'Salary ($)', 'variable': 'Statistic'},
             title=f'Salary Comparison for {city}',
             color_discrete_map={'mean': 'blue', 'min': 'red', 'max': 'green'},
             )

# Show the bar chart
st.plotly_chart(fig)
#########################################################################################
# name_df = df[df['City']==name]

# st.header(f'{name} over time')

# tab1, tab2 = st.tabs(['Female','Male'])

# with tab1:
#     plot_df = name_df[name_df['sex']=='F']
#     fig_f = px.line(data_frame=plot_df, x='year', y='n')
#     st.plotly_chart(fig_f)

# with tab2: 
#     plot_df = name_df[name_df['sex']=='M']
#     fig_m = px.line(data_frame=plot_df, x='year', y='n')
#     st.plotly_chart(fig_m)

# with st.sidebar:

#     year = st.slider('Choose a year', 1910, 2021)
#     st.header(f'Top names by {year}')
#     year_df = df[df['year']==year]
#     tab3, tab4 = st.tabs(['Girls','Boys'])


#     with tab3:
#         girls_names = year_df[year_df.sex=='F'].sort_values('n', ascending=False).head(5)['name']
#         girls_names.index = [1,2,3,4,5]
#         st.dataframe(girls_names)
#     with tab4:
#         boys_names = year_df[year_df.sex=='M'].sort_values('n', ascending=False).head(5)['name']
#         boys_names.index = [1,2,3,4,5]
#         st.dataframe(boys_names)

