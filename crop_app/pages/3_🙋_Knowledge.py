import streamlit as st
import streamlit_authenticator as stauth
from pymongo import MongoClient
import pandas as pd
from st_aggrid import AgGrid, GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder
import requests
import yaml
from yaml.loader import SafeLoader

st.set_page_config(
    page_title = "Crop Recommendation",
    page_icon = "🌾"
)

with open('styles.css') as f:
    st.markdown(f"<style>{f.read()}</style>""", unsafe_allow_html=True)
    
admin=None
try:
    client = MongoClient("mongodb+srv://dulan:dulan@crops.3nnglyt.mongodb.net/?retryWrites=true&w=majority")
    db = client.get_database("crop_db")
    admins = db.admin
except:
    st.error('Database connection problem')


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



try:  
    admin = admins.find_one({'name': username})
except:
    st.error('Database connection problem')

if authentication_status and admin == None:
    st.metric("","Provide your knowledge to improve our system")
    with st.form("knowledge_form"):
        try:
            client = MongoClient("mongodb+srv://dulan:dulan@crops.3nnglyt.mongodb.net/?retryWrites=true&w=majority")
            db = client.get_database("crop_db")
            records = db.user_knowledge
            record_list = list(records.find())
        except:
            st.error('Database connection problem')
            
        
        col1,col2 = st.columns(2)
        col3,col4 = st.columns(2)
        col5,col6 = st.columns(2)
        col7,col8 = st.columns(2)
        col9,col10 = st.columns(2)
        crop_name = col1.text_input("Crop Name")
        temp_min = col3.number_input("Temperature Min")
        temp_max = col4.number_input("Temperature Max")
        rain_min = col5.number_input("Rainfall Min")
        rain_max = col6.number_input("Rainfall Max")
        humi_min = col7.number_input("Humidity Min")
        humi_max = col8.number_input("Humidity Max")
        ph_min = col9.number_input("pH Min")
        ph_max = col10.number_input("pH Max")
        # Every form must have a submit button.
        submitted = st.form_submit_button("Submit")
        # Validate the form inputs after submission.
        
    try:
        if submitted:
            if not crop_name:
                st.error("Please enter Crop Name.")
            elif temp_min is None or temp_max is None:
                st.error("Please enter both Temperature Min and Temperature Max.")
            elif rain_min is None or rain_max is None:
                st.error("Please enter both Rainfall Min and Rainfall Max.")
            elif humi_min is None or humi_max is None:
                st.error("Please enter both Humidity Min and Humidity Max.")
            elif ph_min is None or ph_max is None:
                st.error("Please enter both pH Min and pH Max.")
            else:
                # Process the form data when everything is filled.
                # Add your code here to handle the form submission.
                # For example, you can store the data in a database or display it.
                st.success("Form submitted successfully!")
                ID_list = []
                for item in record_list:
                    ID_list.append(item['ID'])
                    ID_list.sort()
                if records.count_documents({})==0:   
                    new_crop = {
                        'name': crop_name,
                        'temp_min': temp_min,
                        'temp_max': temp_max,
                        'rain_min': rain_min,
                        'rain_max': rain_max,
                        'humi_min': humi_min,
                        'humi_max': humi_max,
                        'pH_min': ph_min,
                        'pH_max': ph_max,
                        'ID': records.count_documents({})+1
                    }
                if records.count_documents({})!=0:   
                    new_crop = {
                        'name': crop_name,
                        'temp_min': temp_min,
                        'temp_max': temp_max,
                        'rain_min': rain_min,
                        'rain_max': rain_max,
                        'humi_min': humi_min,
                        'humi_max': humi_max,
                        'pH_min': ph_min,
                        'pH_max': ph_max,
                        'ID': max(ID_list)+1
                    }
                records.insert_one(new_crop)
    except:
            st.error('Database connection problem')
            
if authentication_status and admin != None:
    st.metric("","Crop Data Viewer and Updater")
    st.header("Add New Data")
    def update_one(sel_row):
        update_crop = {
    
        'name':sel_row[0]["name"],
        'temp_min':float(sel_row[0]["temp_min"]),
        'temp_max':float(sel_row[0]["temp_max"]),
        'rain_min':float(sel_row[0]["rain_min"]),
        'rain_max':float(sel_row[0]["rain_max"]),
        'humi_min':float(sel_row[0]["humi_min"]),
        'humi_max':float(sel_row[0]["humi_max"]),
        'pH_min':float(sel_row[0]["pH_min"]),
        'pH_max':float(sel_row[0]["pH_max"]),
        }
        client = MongoClient("mongodb+srv://dulan:dulan@crops.3nnglyt.mongodb.net/?retryWrites=true&w=majority")
        db = client.get_database("crop_db")
        records = db.crop_records
        records.update_one({"ID": sel_row[0]["ID"]},{'$set': update_crop})
    
    def update_all(sel_row):
        client = MongoClient("mongodb+srv://dulan:dulan@crops.3nnglyt.mongodb.net/?retryWrites=true&w=majority")
        db = client.get_database("crop_db")
        records = db.crop_records
        for i in range(len(sel_row)):
            update_crop = {
    
            'name':sel_row[i-1]["name"],
            'temp_min':float(sel_row[i]["temp_min"]),
            'temp_max':float(sel_row[i]["temp_max"]),
            'rain_min':float(sel_row[i]["rain_min"]),
            'rain_max':float(sel_row[i]["rain_max"]),
            'humi_min':float(sel_row[i]["humi_min"]),
            'humi_max':float(sel_row[i]["humi_max"]),
            'pH_min':float(sel_row[i]["pH_min"]),
            'pH_max':float(sel_row[i]["pH_max"]),
            }
            records.update_one({"ID": sel_row[i]["ID"]},{'$set': update_crop})
    
    def delete_one(sel_row):
        client = MongoClient("mongodb+srv://dulan:dulan@crops.3nnglyt.mongodb.net/?retryWrites=true&w=majority")
        db = client.get_database("crop_db")
        records = db.crop_records
        records.delete_one({"ID": sel_row[0]["ID"]})
    
    def delete_all(sel_row):
        client = MongoClient("mongodb+srv://dulan:dulan@crops.3nnglyt.mongodb.net/?retryWrites=true&w=majority")
        db = client.get_database("crop_db")
        records = db.crop_records
        for i in range(len(sel_row)):
            records.delete_one({"ID": sel_row[i]["ID"]})
    
    # Function to connect to MongoDB and fetch all records
    def fetch_all_records():
        # Replace the following with your MongoDB connection details
        
        client = MongoClient("mongodb+srv://dulan:dulan@crops.3nnglyt.mongodb.net/?retryWrites=true&w=majority")
        db = client.get_database("crop_db")
        records = db.crop_records
        record_list = list(records.find())
        return record_list



    def main():
        st.header("Update Data")
        # Fetch all records from MongoDB
        try:
            records = fetch_all_records()
            
            #st.dataframe(data=records)
            df = pd.DataFrame(records)
            df = df.drop(["_id"],axis=1)
        
            #df["_id"] = df["_id"].str.replace(r"ObjectId\('(.*)'\)", r'\1', regex=True)
            gd = GridOptionsBuilder.from_dataframe(df)
            gd.configure_pagination(enabled=True)
            gd.configure_default_column(editable=True,groupable=True)
            gd.configure_column("ID", editable=False)
            sel_mode = st.radio('Selection Type',options = ['single','multiple'])
            gd.configure_selection(selection_mode = sel_mode, use_checkbox = True)
            gridoptions = gd.build()
            grid_table = AgGrid(df,gridOptions = gridoptions, update_mode = GridUpdateMode.SELECTION_CHANGED,width ='100%',
                                allow_unsafe_jscode=True,theme = 'alpine')
            sel_row = grid_table['selected_rows']
        except:
            st.error('Database connection problem')
        col1,col2 = st.columns(2)
        try:
            if sel_mode == 'single' and len(sel_row) != 0:
                update1 = col1.button("Update One",on_click = lambda:update_one(sel_row))
                delete1 = col2.button("Delete One",on_click = lambda:delete_one(sel_row))
            if sel_mode == 'multiple' and len(sel_row) != 0:    
                update2 = col1.button("Update All",on_click = lambda:update_all(sel_row))
                delete2 = col2.button("Delete All",on_click = lambda:delete_all(sel_row))
        except:
            st.warning("Please select one or more, If you want to update or delete.")
        
        #st.write(sel_row)

    with st.form("knowledge_form"):
        try:
            client = MongoClient("mongodb+srv://dulan:dulan@crops.3nnglyt.mongodb.net/?retryWrites=true&w=majority")
            db = client.get_database("crop_db")
            records = db.crop_records
            record_list = list(records.find())
        except:
            st.error('Database connection problem')
        
        col1,col2 = st.columns(2)
        col3,col4 = st.columns(2)
        col5,col6 = st.columns(2)
        col7,col8 = st.columns(2)
        col9,col10 = st.columns(2)
        crop_name = col1.text_input("Crop Name")
        temp_min = col3.number_input("Temperature Min")
        temp_max = col4.number_input("Temperature Max")
        rain_min = col5.number_input("Rainfall Min")
        rain_max = col6.number_input("Rainfall Max")
        humi_min = col7.number_input("Humidity Min")
        humi_max = col8.number_input("Humidity Max")
        ph_min = col9.number_input("pH Min")
        ph_max = col10.number_input("pH Max")
        # Every form must have a submit button.
        submitted = st.form_submit_button("Submit")
        # Validate the form inputs after submission.
    
    try:
        if submitted:
            if not crop_name:
                st.error("Please enter Crop Name.")
            elif temp_min is None or temp_max is None:
                st.error("Please enter both Temperature Min and Temperature Max.")
            elif rain_min is None or rain_max is None:
                st.error("Please enter both Rainfall Min and Rainfall Max.")
            elif humi_min is None or humi_max is None:
                st.error("Please enter both Humidity Min and Humidity Max.")
            elif ph_min is None or ph_max is None:
                st.error("Please enter both pH Min and pH Max.")
            else:
                # Process the form data when everything is filled.
                # Add your code here to handle the form submission.
                # For example, you can store the data in a database or display it.
                st.success("Form submitted successfully!")
                ID_list = []
                for item in record_list:
                    ID_list.append(item['ID'])
                    ID_list.sort()
                if records.count_documents({})==0:   
                    new_crop = {
                        'name': crop_name,
                        'temp_min': temp_min,
                        'temp_max': temp_max,
                        'rain_min': rain_min,
                        'rain_max': rain_max,
                        'humi_min': humi_min,
                        'humi_max': humi_max,
                        'pH_min': ph_min,
                        'pH_max': ph_max,
                        'ID': records.count_documents({})+1
                    }
                if records.count_documents({})!=0:   
                    new_crop = {
                        'name': crop_name,
                        'temp_min': temp_min,
                        'temp_max': temp_max,
                        'rain_min': rain_min,
                        'rain_max': rain_max,
                        'humi_min': humi_min,
                        'humi_max': humi_max,
                        'pH_min': ph_min,
                        'pH_max': ph_max,
                        'ID': max(ID_list)+1
                    }
                records.insert_one(new_crop)
    except:
            st.error('Database connection problem')

    if __name__ == "__main__":
        main()
        
def uploadfile(csv_file, location_name):
    # Define the URL of your Flask backend
    url = 'http://127.0.0.1:5000/location'

    # Define the CSV file and text data
    files = {'csv_file': csv_file}
    data = {'location': location_name}

    # Make a POST request to the Flask backend
    response = requests.post(url, files=files, data=data)
    if response.status_code == 201:
        st.success("New location added successfully.")
    else:
        st.error("Something went wrong.")
    
# file uploader
if authentication_status:
    st.subheader("Update locations")
    with st.form("Location form"):
        csv_file=st.file_uploader("Upload your csv file:",type=["csv"])
        location_name = st.text_input("Enter correct location name")
        
        submitted = st.form_submit_button("Submit")
        if submitted:
            try:
                response = uploadfile(csv_file, location_name)
            except:
                st.error("Something went wrong while uploading.")
            
            