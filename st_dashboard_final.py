import streamlit as st
import pandas as pd
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from streamlit_keplergl import keplergl_static
from keplergl import KeplerGl
from datetime import datetime as dt
from numerize.numerize import numerize
from PIL import Image

########################### Initial settings for the dashboard ####################################################


st.set_page_config(page_title = 'Citi Bike Strategy Dashboard', layout='wide')
st.title("Citi Bike Strategy Dashboard")

# Define side bar
st.sidebar.title("Aspect Selector")
page = st.sidebar.selectbox('Select an aspect of the analysis',
  ["Intro page","Weather component and bike usage",
   "Most popular stations",
    "Interactive map with aggregated bike trips", "Recommendations"])

########################## Import data ###########################################################################################

df_1 = pd.read_csv('reduced_data_to_plot_7.csv', index_col = 0)
top20 = pd.read_csv('top20.csv', index_col = 0)
df = df_1.iloc[::50]
######################################### DEFINE THE PAGES #####################################################################


### Intro page

if page == "Intro page":
    st.markdown("#### This dashboard aims to provide helpful insights into the expansion challenges Citi Bike currently faces.")
    st.markdown("As bike sharing continues to grow in popularity across New York City, Citi Bike has experienced a dramatic rise in ridership since its launch in 2013, particularly following the Covid-19 pandemic. While this increase reflects the company’s success in promoting sustainable and convenient urban mobility, it has also revealed critical distribution challenges. Stations often face imbalances, with some frequently running out of bikes while others become overcrowded with returns.") 
    st.markdown("As the lead analyst, my goal is to identify the root causes of these distribution issues. This includes determining whether they are driven by high volume, seasonal patterns, or location-specific demand by analyzing Citi Bike usage trends throughout the year 2022. Based on this analysis, I will provide data-informed strategies to improve bike availability and enhance the overall user experience. To support these recommendations, I created the Citi Bike Strategy Dashboard, an interactive tool that presents key insights and trends in a format that is accessible for analysts and actionable for the business development team.")

    st.markdown("This analysis will look at the potential reasons behind this. The dashboard is separated into 4 sections:")
    st.markdown("- Weather component and bike usage")
    st.markdown("- Most popular stations")
    st.markdown("- Interactive map with aggregated bike trips")
    st.markdown("- Recommendations")
    st.markdown("The dropdown menu on the left 'Aspect Selector' will take you to the different aspects of the analysis our team looked at.")

    myImage = Image.open("citi_bike_photo.jpg") #source: https://www.google.com/search?sca_esv=6a81f2bd04fd845e&sxsrf=AHTn8zpLysIAcT1ZcBFCE1yc9Hycjw2UTg:1744070361115&q=generic+bike+share+company+photo&udm=2&fbs=ABzOT_CWdhQLP1FcmU5B0fn3xuWpA-dk4wpBWOGsoR7DG5zJBpcx8kZB4NRoUjdgt8WwoMtdeCpyMPmJ4aXMZgMKl7hTzBR3LltgTwklBktqxzBdAiQgFp3DWkZ7-IOB24IfWUDMTX_L_SWWFutIxpNqrWfbCsrqB7h1AruEUgucGvio7oeIF8Vd6jhIB81y3GAB2152aoVVRmm5wJqLEbP3oS6L-gSKFg&sa=X&ved=2ahUKEwi7q9mykMeMAxXnSTABHcEjGKcQtKgLegQIEBAB&biw=767&bih=791&dpr=1.25#vhid=ihqeVwWMuKGoYM&vssid=mosaic
    st.image(myImage)

 ### Create the dual axis line chart page 
    
elif page == 'Weather component and bike usage':

    fig_2 = make_subplots(specs = [[{"secondary_y": True}]])

    fig_2.add_trace(
    go.Scatter(x = df['date'], y = df['bike_rides_daily'], name = 'Daily bike rides', marker={'color': df['bike_rides_daily'],'color': 'blue'}),
    secondary_y = False
    )

    fig_2.add_trace(
    go.Scatter(x=df['date'], y = df['avgTemp'], name = 'Daily temperature', marker={'color': df['avgTemp'],'color': 'red'}),
    secondary_y=True
    )

    fig_2.update_layout(
    title = 'Daily bike trips and temperatures in 2022',
    height = 400
    )

    st.plotly_chart(fig_2, use_container_width=True)
    st.markdown("The chart presents a dual-axis time series where Citi Bike ride volume, which follows a U shape, is plotted alongside daily temperature, which follows an inverted-U shape. Bike usage increases as temperatures cool down specifically in winter and spring. Usage then declines sharply during the summer heat, and rises slightly again in the fall. This inverse correlation suggests that riders tend to avoid biking in very hot weather, and instead prefer moderate conditions. The data shows that Citi Bike demand is not only sensitive to temperature but is highest within a specific comfort range. This insight has important implications for operations, demand forecasting, and decisions around system expansion.")

### Most popular stations page

    # Create the season variable #

elif page == 'Most popular stations':
    
    # Create the filter on the side bar
    
    with st.sidebar:
        season_filter = st.multiselect(label= 'Select the season',     options=df['season'].unique(),
    default=df['season'].unique())

    df1 = df.query('season == @season_filter')
    
      # Define the total rides
    total_rides = float(df1['bike_rides_daily'].count())    
    st.metric(label = 'Total Bike Rides', value= numerize(total_rides))
    
      # Bar chart

    df1['value'] = 1 
    df_groupby_bar = df1.groupby('start_station_name', as_index = False).agg({'value': 'sum'})
    top20 = df_groupby_bar.nlargest(20, 'value')
    fig = go.Figure(go.Bar(x = top20['start_station_name'], y = top20['value']))

    fig = go.Figure(go.Bar(x = top20['start_station_name'], y = top20['value'], marker={'color':top20['value'],'colorscale': 'Blues'}))
    fig.update_layout(
    title = 'Top 20 most popular bike stations in New York',
    xaxis_title = 'Start stations',
    yaxis_title ='Sum of trips',
    width = 900, height = 600
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("The top five most popular Citi Bike stations are all located in Manhattan, a borough known for its high density and centrality in New York City. These stations include W 13th St and 5th Ave in the Chelsea neighborhood, W 31st St and 7th Ave in Midtown near Penn Station, W St and Chambers St near Tribeca and the Financial District, 6th Ave and Canal St in the SoHo area, and 6th Ave and W 33rd St in Midtown, close to the Empire State Building. The concentration of these popular stations in Manhattan aligns with the high demand for bike-sharing services in central, densely populated areas. This suggests that Citi Bike usage is heavily influenced by the accessibility and proximity to key commercial and residential hubs in the city.")

elif page == 'Interactive map with aggregated bike trips': 

    ### Create the map ###

    st.write("Interactive map showing aggregated bike trips over New York")

    path_to_html = "New York Bike Trips Aggregated.html" 

    # Read file and keep in variable
    with open('New York Bike Trips Aggregated.html', encoding='utf-8') as f:
        html_data = f.read()


    ## Show in webpage
    st.header("Aggregated Bike Trips in New York")
    st.components.v1.html(html_data,height=1000)
    st.markdown("After applying a filter to the map to focus on the most common trips in New York City, it quickly became clear that Manhattan stood out as the busiest zone. The density of trips in and around Manhattan was significantly higher compared to other boroughs. This isn’t too surprising, considering Manhattan is the city’s economic and cultural hub, home to major business districts like Midtown and the Financial District, world-famous landmarks, and a high population density during work hours.")
    st.markdown("Additional research supports this: Manhattan attracts millions of commuters and tourists daily, making it a hotspot for taxi and ride-sharing activity. Areas like Times Square, Central Park, and Grand Central Terminal naturally generate heavy traffic due to their popularity and central location. The combination of tourism, business travel, and limited parking availability likely contributes to the high volume of trips in this area.")
   
else:
    
    st.header("Conclusions")
    bikes = Image.open("Citi_bike_photo_final.jpg") #source : https://www.google.com/search?sca_esv=4af4262072247b83&sxsrf=AHTn8zrT5xI72UIicHtXuf8TZ32wvf-L_Q:1744081395537&q=bike+share+company+photo&udm=2&fbs=ABzOT_CWdhQLP1FcmU5B0fn3xuWpA-dk4wpBWOGsoR7DG5zJBr9f-W3h_R3HVJ-z4uJntm7S42ilFcJ4Lp_1EvpfsHF6XArBqCAi1YaF_O-xJJYmFtiC0wjZI2wNVJWXYUJXrSOuWxhDK_X21r598RBk-pchR_vru9WFzTAhstBrQ3oE263T-6qBqX3pRcYAmGs-j7kn6OJlO_D62THoIqUZMNuAiq-G2Q&sa=X&ved=2ahUKEwixj6nAuceMAxVQRTABHcIhNGMQtKgLegQIEBAB&biw=1536&bih=791&dpr=1.25#vhid=pI-HSek5Miz50M&vssid=mosaic
    
    st.markdown("The analysis presented in this dashboard reveals critical insights into Citi Bike usage patterns, highlighting key factors that influence demand and station performance. The dual-axis time series chart demonstrates an inverse correlation between daily bike rides and temperature, showing that bike usage, interestingly,  tends to rise during colder temperatures in winter and spring and declines during extreme heat. This suggests that Citi Bike demand is most robust when the weather in a comfortable if not cold temperature, offering important implications for demand forecasting, resource allocation, and planning.")
    st.markdown("Further investigation of the top five most popular stations shows that they are all located in Manhattan, a high-density area with significant business, tourism, and residential activity. Stations like W 13th St and 5th Ave, W 31st St and 7th Ave, and 6th Ave and Canal St stand out as key hubs, with demand driven by accessibility to major commercial and tourist districts. This trend further emphasizes the importance of strategic station placement in areas with high foot traffic and proximity to key city landmarks.")
    st.markdown("The map analysis also confirms that Manhattan is the busiest zone in the city, with a higher concentration of trips compared to other boroughs. Given the city's role as a cultural and economic center, commuters and tourists generate heavy demand for bike-sharing services, particularly in areas like Times Square, Central Park, and Grand Central Terminal.")
    st.markdown("### Recommendations:")
    st.markdown("Expand Coverage in Popular Areas: Since the demand for Citi Bike is highest in Manhattan, it is recommended to increase the number of stations in key tourist and business districts, particularly around areas like Times Square, Grand Central, and the Financial District. This would help alleviate bike shortages at popular locations and support higher ridership in high-demand zones.")
    st.markdown("Optimize Bike Distribution for Seasonal Trends: Given the strong relationship between temperature and bike usage, it’s advisable to optimize bike distribution and station management based on seasonal patterns. During winter and spring, bike availability should be increased to meet the higher demand, while during summer and fall, bike numbers can be adjusted to match the lower demand in those months.")
    st.markdown("Invest in Infrastructure for Off-Peak Periods: In addition to peak demand periods, more effort should be put into ensuring that stations in less densely populated areas have adequate bikes during off-peak times. This will help balance the usage across the boroughs and minimize congestion at popular stations while ensuring that less crowded areas are well-served.")
    st.markdown("Focus on User Experience and Accessibility: Enhancing the user experience by providing clearer real-time data on bike availability and improving the accessibility of stations in high-traffic areas will ensure that users can more easily find bikes and docks when needed. This could include better signage, mobile app features, or notifications regarding bike availability.")


