import streamlit as st
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth


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

st.metric("","You can change your password any time")

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
    st.sidebar.markdown(f"""
                <div class="help3">
                <h3>You are logged into the system.</h3>
                <p>
                {name},
                </p>
                <p>
                We will guide you for your cultivation.
                </p>
                </div>
                """,unsafe_allow_html=True
                )
    try:
        if authenticator.reset_password(username, 'Reset password'):
            st.success('Password modified successfully')
            with open('./config.yaml', 'w') as file:
                yaml.dump(config, file, default_flow_style=False)
    except Exception as e:
        st.error(e)