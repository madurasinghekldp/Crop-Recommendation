import streamlit as st
import yaml
from yaml.loader import SafeLoader
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import streamlit_authenticator as stauth

class AuthenticateUser:
    
    def send_email(recipient, subject, body):
        # Replace the following placeholders with your email credentials and settings
        sender_email = 'clagri2023@gmail.com'
        sender_password = 'cqnbrmcxqznmzxxa'
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587  # Or the appropriate port for your email service

        # Create a MIMEText object to represent the email
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient
        msg['Subject'] = subject

        # Attach the body of the email
        msg.attach(MIMEText(body, 'plain'))

        # Connect to the SMTP server and send the email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Use TLS encryption
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient, msg.as_string())
    
    def authUser(self):
        with open('./config.yaml') as file:
            config = yaml.load(file, Loader=SafeLoader)

        self.authenticator = stauth.Authenticate(
            config['credentials'],
            config['cookie']['name'],
            config['cookie']['key'],
            config['cookie']['expiry_days'],
            config['preauthorized']
        )

        

        if 'value' not in st.session_state:
            st.session_state['value'] = ""


        tab1,tab2,tab3 = st.tabs(["Login","Signup","Forgot Password"])

        # login_options = st.selectbox("Select what you need: ",options=("Login","SignUp","Forgot Password"))


        with tab1:
            name, self.authentication_status, username = self.authenticator.login("Login","main")

            if self.authentication_status == False:
                st.error("Username/password is incorrect")
            if self.authentication_status == None:
                st.warning("please enter your username and password")
            if self.authentication_status:
                self.authenticator.logout("Logout","sidebar")


        with tab2:  
            if self.authentication_status == None:      
                try:
                    if self.authenticator.register_user('Register user', preauthorization=False):
                        st.success('User registered successfully')
                        with open('./config.yaml', 'w') as file:
                            yaml.dump(config, file, default_flow_style=False)
                except Exception as e:
                    st.error(e)
                    
                    
        with tab3:      
            if self.authentication_status == None:
                try:
                    username_of_forgotten_password, email_of_forgotten_password, new_random_password = self.authenticator.forgot_password('Forgot password')
                    if username_of_forgotten_password:
                        email_subject = 'Password Reset Request'
                        email_body = f'Hello {username_of_forgotten_password},\n\n'
                        email_body += 'You have requested a password reset. Your new random password is: ' + new_random_password
                        # Code to send the email using your email configuration
                        send_email(email_of_forgotten_password, email_subject, email_body)
                        st.success('New password sent securely')
                        # Random password to be transferred to user securely
                        with open('./config.yaml', 'w') as file:
                            yaml.dump(config, file, default_flow_style=False)
                    else:
                        st.error('Username not found')
                except Exception as e:
                    st.error(e)