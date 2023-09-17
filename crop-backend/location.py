import pandas as pd
import pickle
from connection import Connection
import os
import statsmodels.api as sm
from statsmodels.tsa.statespace.sarimax import SARIMAX

class LocationModel:
    
    def create_temp_model(self,df,location):
        aws = Connection()
        model = SARIMAX(df['TEMP'], order=(0, 1, 1), seasonal_order=(1, 1, 0, 12))
        results = model.fit()
        bucket_name = 'sldpweather'
        file_name = f'{location}_temp.pkl'
        
        with open(file_name, 'wb') as f:
            pickle.dump(results, f)

        # Upload the pickle file to S3
        aws.s3.upload_file(file_name, bucket_name, file_name)
        os.remove(file_name)
    ########################################################################
    def create_rain_model(self,df,location):
        aws = Connection()
        model = SARIMAX(df['RAINFALL'], order=(1, 0, 1), seasonal_order=(1, 1, 0, 12))
        results = model.fit()
        bucket_name = 'sldpweather'
        file_name = f'{location}_rain.pkl'
        with open(file_name, 'wb') as f:
            pickle.dump(results, f)

        # Upload the pickle file to S3
        aws.s3.upload_file(file_name, bucket_name, file_name)
        os.remove(file_name)
    ########################################################################
    def create_humi_model(self,df,location):
        aws = Connection()
        model = SARIMAX(df['RH2M'], order=(0, 0, 1), seasonal_order=(1, 1, 0, 12))
        results = model.fit()
        bucket_name = 'sldpweather'
        file_name = f'{location}_humi.pkl'
        with open(file_name, 'wb') as f:
            pickle.dump(results, f)

        # Upload the pickle file to S3
        aws.s3.upload_file(file_name, bucket_name, file_name)
        os.remove(file_name)