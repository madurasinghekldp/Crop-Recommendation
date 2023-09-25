import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader



    
st.set_page_config(
page_title = "Crop Recommendation",
page_icon = "🌾"
)

with open('styles.css') as f:
    st.markdown(f"<style>{f.read()}</style>""", unsafe_allow_html=True)
    
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

st.metric("","Please follow the instructions here")
st.markdown("""
            <style>
button[kind="secondary"]{
        border-color: rgb(0,255,0);
    }
button[kind="secondaryFormSubmit"]{
    border-color: rgb(0,255,0);
}
div[data-testid="stToolbar"]{
        display: none;
    }
footer[class = "css-cio0dv ea3mdgi1"]{
        display: none;
    }
            </style>
            """, unsafe_allow_html=True)

with open('./config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)
    
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)



name, authentication_status, username = authenticator.login("Login","main")

if authentication_status == False:
    st.error("Username/password is incorrect")
if authentication_status == None:
    st.warning("please enter your username and password")
if authentication_status:
    authenticator.logout("Logout","sidebar")
    

if authentication_status:
    st.markdown("""
                <div class="help1">
                <h3>Get Crop Recommendation</h3>
                <p>
                If you have any doubts about using this application, Please follow the instructions below.
                </p>
                <ul>
                <li>Choose your city name from dropdown. If there is no your location, you can create location by following the video below.</li>
                <li>Enter the pH value of your land.</li>
                <li>Enter the starting month of cultivation.</li>
                <li>Enter the ending month of cultivation.</li>
                <li>Click the Get Crop button.</li>
                </ul>
                </div>
                """,unsafe_allow_html=True
                )
    st.markdown("""
                <div class="help2">
                <h3>How to add location to system.</h3>
                <p>
                You can follow the steps in the video to update location data. <a href="https://power.larc.nasa.gov/data-access-viewer/" target="_blank">Get CSV</a>
                </p>
                </div>
                """,unsafe_allow_html=True
                )
    try:
        st.video("https://youtu.be/SHSOr9s6l-M")
    except:
        st.warning("Can not load the video")
