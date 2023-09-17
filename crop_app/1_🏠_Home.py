import streamlit as st
import geopandas as gpd
import pandas as pd
import geopy
import requests
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import boto3


from streamlit_option_menu import option_menu
import plost

from authenticate import AuthenticateUser

access_key = 'AKIAVAPWN6G7EL3FJKAE'
secret_key = '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'
bucket_name = 'sldpweather'


st.set_page_config(
    page_title = "Crop Recommendation",
    page_icon = "🌾"
)

with open('styles.css') as f:
    st.markdown(f"<style>{f.read()}</style>""", unsafe_allow_html=True)

s3_client = boto3.client(
    's3',
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key
)

try:
    # List all objects in the bucket
    response = s3_client.list_objects(Bucket=bucket_name)

    # Extract pickle file names
    pickle_files = [obj['Key'] for obj in response.get('Contents', []) if obj['Key'].endswith('.pkl')]
    first_parts = [file.split('_')[0] for file in pickle_files]

    # Remove duplicates
    unique_first_parts = list(set(first_parts))
except:
    st.error('Database connection problem')
    
null_list = ['']

city = ""
#theme
# Apply custom CSS for dark theme
def set_dark_theme():
    st.markdown(
        """
        <style>
        body {
            color: white;
            background-color: #262730;
        }
        .stAlert {
            color: white;
            background-color: #4e5055;
        }
        /* Add more CSS styles for other Streamlit components as needed */
        </style>
        """,
        unsafe_allow_html=True
    )

# Call the function to apply the dark theme
set_dark_theme()
#st.header("Get The Optimal Crop For Your Location")
st.metric("","Get The Optimal Crop For Your Location")
auth = AuthenticateUser()
auth.authUser()



if auth.authentication_status:

    st.markdown(
        """
        <style>
        div[data-baseweb="tab-list"]{
            display: none;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


    #sidebar progress bar
    bar = st.sidebar.progress(0)

    st.sidebar.write("""
            
            
            """)

    st.sidebar.write("""
            
            
            """)
    # Select City
    try:
        city = st.sidebar.selectbox("Enter Your City",options=(null_list+ unique_first_parts))
    except:
        st.error("Database connection problem")

    if city != "":
        bar.progress(25)
        
    # file uploader
    
    #csv_file=st.sidebar.file_uploader("Upload your csv file:",type=["csv"])


    #map
    col0,col00 = st.columns((9.9999,0.0001))
    col1,col2 = st.columns(2)
    with col0:
        lat = 7.8774
        lon = 80.7003
        try:
            geolocator = Nominatim(user_agent="GTA Lookup")
            geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
            if city != "":
                location = geolocator.geocode(""+", "+city+", "+""+", "+"")

                lat = location.latitude
                lon = location.longitude

            map_data = pd.DataFrame({'lat': [lat], 'lon': [lon]})
            st.map(map_data)
            col1.metric("latitude",lat)
            col2.metric("longitude",lon)
        except:
            st.error("Couldn't load the map")

    st.sidebar.write("""
            
            
            """)

    # number of months
    pH_value=st.sidebar.number_input("Enter pH value of the area:")

    if pH_value != 0 and city != "":
        bar.progress(50)

    
    start_month = st.sidebar.selectbox("Enter start month",options=('','01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12'))
    
    if pH_value != 0 and city != "" and start_month:
        bar.progress(75)
        
    end_month = st.sidebar.selectbox("Enter end month",options=('','01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12'))
    if pH_value != 0 and city != "" and start_month and end_month:
        bar.progress(100)
    
    
    col3,col4,col5,col6 = st.columns(4)
    col7,col8 = st.columns(2)
    col9,col10,col11 = st.columns(3)
    col12,col13 = st.columns(2)
    
    temp = None
    humi = None
    rain = None
    pH = None
    crop = None
    tempd = None
    
    
    
    def btn_click():
            # Define the base URL of the API
        base_url = 'http://127.0.0.1:5000/weather'

        # Define the parameters
        params = {
            'location': city,
            'pH': pH_value,
            'start_month': start_month,
            'end_month': end_month
        }

        # Send the GET request
        response = requests.get(base_url, params=params)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Process the response data
            try:
                data = response.json()
            except:
                st.error("Response Error")
            # Do something with the data
            temp = data['Average temp']
            humi = data['Average humi']
            rain = data['Average rain']
            pH = data['pH value']
            crop = data['Suitable crop']
            tempd = pd.read_json(data['tempd'])
            humid = pd.read_json(data['humid'])
            raind = pd.read_json(data['raind'])
            col3.metric("Average Temperature 🌡️", f'{temp}℃')
            col4.metric("Average Humidity 💧", f'{humi}%')
            col5.metric("Average Rainfall 🌧️", f'{rain}mm')
            col6.metric("pH value", pH)
            if crop:
                col7.metric("Suitable crop", crop)
            else:
                col12.warning("Suitable crop not found.")
            with col9:
                plost.line_chart(data=tempd,x="Date",y="TEMP")
            with col10:
                plost.line_chart(data=humid,x="Date",y="HUMI")
            with col11:
                plost.line_chart(data=raind,x="Date",y="RAIN")
        else:
            
            # Request was not successful
            col12.warning("Suitable crop not found.")
    if pH_value and city and start_month and end_month:    
        btn=st.sidebar.button("Get Crop",on_click=btn_click)
    
    