import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import streamlit as st

st.markdown("""
    <style>
    .big-font {
        font-size: 32px;
        font-weight: bold;
        color: seagreen;
        text-align: center;
    }
    .small-font {
        font-size: 21px;
        color: #757575;
        text-align: center;
    }
    </style>
    <div class="big-font">Bike Share Data Analysis Dashboard 🚲</div>
""", unsafe_allow_html=True)

st.markdown(
    """
    <div style="text-align: justify;">
        <p>Bike-sharing systems are modernized bike rental services where the entire process, including membership, rental, and return, is automated. Users can conveniently rent bikes from one location and return them to another. With over 500 programs and 500,000 bicycles globally, these systems are gaining significant attention for their positive impact on traffic management, environmental sustainability, and public health.</p>
        <p>This dashboard provides insights into various aspects of bike-sharing usage, including the count of rides by weekday, which highlights peak days for bike-sharing activities, and the count of rides by season, showcasing seasonal variations in usage. Additionally, it explores seasonal trends in casual and registered bikeshare usage during 2012, offering a deeper look into user behavior across different seasons. Lastly, the dashboard examines the user count by weather condition, shedding light on how weather impacts bike-sharing participation. Together, these insights reveal patterns and trends that contribute to a better understanding of sustainable urban mobility.</p>
    </div>
    """,
    unsafe_allow_html=True
)

# ---- load dataset -------
df = pd.read_csv("https://raw.githubusercontent.com/hakansyukur23/Proyek-Analisis-Data-Bike-Sharing-Dataset/main/Bike-sharing-dataset/day_df_clean.csv")
df['dteday'] = pd.to_datetime(df['dteday'])

# ---- create helper functions ---
def create_monthly_users_df(df):
    monthly_users_df = df.resample(rule='M', on='dteday').agg({
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum"
    })
    monthly_users_df.index = monthly_users_df.index.strftime('%b-%y')
    monthly_users_df = monthly_users_df.reset_index()
    monthly_users_df.rename(columns={
        "dteday": "yearmonth",
        "cnt": "total_rides",
        "casual": "casual_rides",
        "registered": "registered_rides"
    }, inplace=True)
    
    return monthly_users_df

def create_seasonly_users_df(df):
    seasonly_users_df = df.groupby("season").agg({
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum"
    })
    seasonly_users_df = seasonly_users_df.reset_index()
    seasonly_users_df.rename(columns={
        "cnt": "total_rides",
        "casual": "casual_rides",
        "registered": "registered_rides"
    }, inplace=True)
    
    seasonly_users_df = pd.melt(seasonly_users_df,
                                      id_vars=['season'],
                                      value_vars=['casual_rides', 'registered_rides'],
                                      var_name='type_of_rides',
                                      value_name='count_rides')
    
    seasonly_users_df['season'] = pd.Categorical(seasonly_users_df['season'],
                                             categories=['Spring', 'Summer', 'Fall', 'Winter'])
    
    seasonly_users_df = seasonly_users_df.sort_values('season')
    
    return seasonly_users_df

def create_weekday_users_df(df):
    weekday_users_df = df.groupby("weekday").agg({
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum"
    })
    weekday_users_df = weekday_users_df.reset_index()
    weekday_users_df.rename(columns={
        "cnt": "total_rides",
        "casual": "casual_rides",
        "registered": "registered_rides"
    }, inplace=True)
    
    weekday_users_df = pd.melt(weekday_users_df,
                                      id_vars=['weekday'],
                                      value_vars=['casual_rides', 'registered_rides'],
                                      var_name='type_of_rides',
                                      value_name='count_rides')
    
    weekday_users_df['weekday'] = pd.Categorical(weekday_users_df['weekday'],
                                             categories=['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])
    
    weekday_users_df = weekday_users_df.sort_values('weekday')
    
    return weekday_users_df
#---- ! ------
min_date = df["dteday"].min()
max_date = df["dteday"].max()

# ----- SIDEBAR -----
#input logo
with st.sidebar:
    # add capital bikeshare logo
    st.image("https://raw.githubusercontent.com/hakansyukur23/Proyek-Analisis-Data-Bike-Sharing-Dataset/main/Image/Bike_Logo.png")

with st.sidebar:
    st.sidebar.header("Filter:")

    # mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label="Seasonal Trends: Filtering by Date", min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

st.sidebar.subheader('About the Data')
st.sidebar.write(
    """
    The bike-sharing rental process is highly correlated with environmental and seasonal factors. For example, weather conditions, precipitation, day of the week, season, hour of the day, and more can influence rental behavior. 
    The core dataset consists of a two-year historical log from the Capital Bikeshare system in Washington D.C., USA, corresponding to the years 2011 and 2012. This dataset is publicly available at [Capital Bikeshare System Data](http://capitalbikeshare.com/system-data).
    The data has been aggregated on both a two-hourly and daily basis, and relevant weather and seasonal information has been extracted and added. Weather data has been sourced from [FreeMeteo](http://www.freemeteo.com).
    """
)


#-----------------------------------------------------
# hubungkan filter dengan main_df

main_df = df[
    (df["dteday"] >= str(start_date)) &
    (df["dteday"] <= str(end_date))
]

monthly_users_df = create_monthly_users_df(main_df)
weekday_users_df = create_weekday_users_df(main_df)
seasonly_users_df = create_seasonly_users_df(main_df)
#-----------------------------------------------------

# ----- MAINPAGE -----
st.markdown('<h3 style="color:White;">Seasonal Trends in Casual and Registered Bikeshare Usage During 2012</h3>', unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)

with col1:
    total_all_rides = main_df['cnt'].sum()
    st.metric("Total Rides", value=total_all_rides)
with col2:
    total_casual_rides = main_df['casual'].sum()
    st.metric("Total Casual Rides", value=total_casual_rides)
with col3:
    total_registered_rides = main_df['registered'].sum()
    st.metric("Total Registered Rides", value=total_registered_rides)

#-------- Seasonal Trend chart ------
fig = px.line(monthly_users_df,
              x='yearmonth',
              y=['casual_rides', 'registered_rides'],
              color_discrete_sequence=["palegreen", "darkgreen"],
              markers=True
              ).update_layout(xaxis_title='', yaxis_title='Total Rides')

st.plotly_chart(fig, use_container_width=True)

st.markdown("""
- September is the month with the highest total trips for both casual and registered riders.
- January and February marks the lowest months with total trips of the year.
""")

#  ---- bikeshare rider by seasons -----
st.markdown('<h3 style="color:seagreen;">Count of bikeshare rides by season</h3>', unsafe_allow_html=True)
seasonly_users_df = create_seasonly_users_df(df)

# martric
columns = st.columns(len(seasonly_users_df['season'].unique()))

for i, (season, group) in enumerate(seasonly_users_df.groupby('season')):
    with columns[i]:
        # Menghitung total jumlah rides untuk musim tersebut
        total_rides = group['count_rides'].sum()
        st.metric(f"Season {season}", value=total_rides)
#---- ~~ ----

# ---- riders by season ----
fig1 = px.bar(seasonly_users_df,
              x='season',
              y=['count_rides'],
              color='type_of_rides',
              color_discrete_sequence=["palegreen", "darkgreen"]
              ).update_layout(xaxis_title='', yaxis_title='Total Rides')
st.plotly_chart(fig1, use_container_width=True)
st.markdown("""
- Fall is the season with the highest total trips for both casual and registered riders.
""")

# ---- Rides by weekday ----
st.markdown('<h3 style="color:seagreen;">Count of bikeshare rides by weekday</h3>', unsafe_allow_html=True)
fig2 = px.bar(weekday_users_df,
              x='weekday',
              y=['count_rides'],
              color='type_of_rides',
              color_discrete_sequence=["palegreen", "darkgreen"]
              ).update_layout(xaxis_title='', yaxis_title='Total Rides')
st.plotly_chart(fig2, use_container_width=True)
st.markdown("""
- Member riders dominates the trip during weekday. The number of trips gradually decrease after Tuesday, and reach its lowest on Sunday
- Casual riders have relatively low usage during weekdays, but their trips significantly increase over the weekend.
- In conclusion, member riders tend to rent bikes on weekdays, while casual riders prefer to rent bikes on weekends.
""")

# ----- rides by weather -----
st.markdown('<h3 style="color:seagreen;">Number of Bike Users Based on Weather Conditions</h3>', unsafe_allow_html=True)
weather_users_df = df.groupby('weathersit').agg({
    'cnt': 'sum' 
}).reset_index()

fig2 = px.bar(weather_users_df,
              x='weathersit',
              y='cnt',
              color='weathersit',  # Warna berdasarkan kondisi cuaca
              color_discrete_sequence= ["#539d47", "#a8d08d", "#7bbf6b"],
              labels={'cnt': 'Total Rides', 'weathersit': 'Kondisi Cuaca'}
              ).update_layout(xaxis_title='', yaxis_title='Total Rides')

st.plotly_chart(fig2, use_container_width=True)

st.markdown("""
- The pattern of bicycle rentals by weather shows that the most bicycle users are during clear weather.
""")




