from connection import Connection
import pandas as pd
import pickle
from datetime import datetime

class WeatherForecast:
    
    def cal_temp(self,location,start_month,end_month):
        aws = Connection()
        
        print('thread temp')
        date_str = '2021-12-01'
        date = datetime.strptime(date_str, '%Y-%m-%d')
        current_date = datetime.now()

        # Calculate the number of months
        months = (current_date.year - date.year) * 12 + (current_date.month - date.month) + 12

        #print("Number of months:", months)
        
        file_name = f'{location}_temp.pkl'
        
        try:
            # retrieve the object from S3 as bytes
            response = aws.s3.get_object(Bucket=aws.bucket_name, Key=file_name)
            data = response['Body'].read()
        except Exception as e:
            return None

        # load the pickle data
        model = pickle.loads(data)

        # Make predictions for the future dates
        forecast = model.get_forecast(steps=months)

        # Extract the predicted values and confidence intervals
        predicted_values = forecast.predicted_mean
        ci = forecast.conf_int()
        
        
        # Get the current year and month
        current_year = datetime.now().year
        current_month = datetime.now().month
        current_date = datetime.now()

        series = pd.Series(predicted_values[current_date:])
        
        # Find rows where the month is '08' and the date is after the current year and month
        filtered_data1 = series[(series.index.month == int(start_month))]
        filtered_data2 = series[(series.index.month == int(end_month))]
        
        if filtered_data1.index.max() > filtered_data2.index.max():
            return None
        else:
            mean_range = series.loc[filtered_data1.index.max():filtered_data2.index.max()]
            mean_value = mean_range.mean()
            mean_temp = round(mean_value, 1)
            print(mean_range)
            df = mean_range.reset_index()
            df.columns = ['Date', 'TEMP']
            
            return mean_temp,df
        
    def cal_humi(self,location,start_month,end_month):
        aws = Connection()
        
        print('thread humi')
        date_str = '2021-12-01'
        date = datetime.strptime(date_str, '%Y-%m-%d')
        current_date = datetime.now()

        # Calculate the number of months
        months = (current_date.year - date.year) * 12 + (current_date.month - date.month) + 12

        #print("Number of months:", months)
        
        file_name = f'{location}_humi.pkl'
        
        try:
            # retrieve the object from S3 as bytes
            response = aws.s3.get_object(Bucket=aws.bucket_name, Key=file_name)
            data = response['Body'].read()
        except Exception as e:
            return None

        # load the pickle data
        model = pickle.loads(data)

        # Make predictions for the future dates
        forecast = model.get_forecast(steps=months)

        # Extract the predicted values and confidence intervals
        predicted_values = forecast.predicted_mean
        
        # Get the current year and month
        current_year = datetime.now().year
        current_month = datetime.now().month
        current_date = datetime.now()

        series = pd.Series(predicted_values[current_date:])
        # Find rows where the month is '08' and the date is after the current year and month
        filtered_data1 = series[(series.index.month == int(start_month))]
        filtered_data2 = series[(series.index.month == int(end_month))]
        if filtered_data1.index.max() > filtered_data2.index.max():
            return None
        else:
            mean_range = series.loc[filtered_data1.index.max():filtered_data2.index.max()]
            mean_value = mean_range.mean()
            mean_humi = round(mean_value, 1)
            print(mean_range)
            df = mean_range.reset_index()
            df.columns = ['Date', 'HUMI']
            
            return mean_humi,df
        
    def cal_rain(self,location,start_month,end_month):
        aws = Connection()
        
        print('thread rain')
        date_str = '2021-12-01'
        date = datetime.strptime(date_str, '%Y-%m-%d')
        current_date = datetime.now()

        # Calculate the number of months
        months = (current_date.year - date.year) * 12 + (current_date.month - date.month) + 12

        #print("Number of months:", months)
        
        file_name = f'{location}_rain.pkl'
        
        try:
            # retrieve the object from S3 as bytes
            response = aws.s3.get_object(Bucket=aws.bucket_name, Key=file_name)
            data = response['Body'].read()
        except Exception as e:
            return None

        # load the pickle data
        model = pickle.loads(data)
        # Make predictions for the future dates
        forecast = model.get_forecast(steps=months)

        # Extract the predicted values and confidence intervals
        predicted_values = forecast.predicted_mean
        
        # Get the current year and month
        current_year = datetime.now().year
        current_month = datetime.now().month
        current_date = datetime.now()

        series = pd.Series(predicted_values[current_date:])
        rain_data_df = pd.DataFrame({'Rain Data': series})
        rain_data_df['Month'] = series.index.month

        # Find rows where the month is '08' and the date is after the current year and month
        filtered_data1 = series[(series.index.month == int(start_month))]
        filtered_data2 = series[(series.index.month == int(end_month))]
        if filtered_data1.index.max() > filtered_data2.index.max():
            return None
        else:
            mean_range = series.loc[filtered_data1.index.max():filtered_data2.index.max()]
            mean_value = mean_range.mean()
            mean_rain = round(mean_value, 1)
            print(mean_range)
            df = mean_range.reset_index()
            df.columns = ['Date', 'RAIN']
            
            return mean_rain,df