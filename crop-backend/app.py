from flask import Flask, request, jsonify, Response, send_file
import pandas as pd

import pickle
from datetime import datetime
import threading
import numpy as np

from weather import WeatherForecast
from crop import PredictedCrop
from location import LocationModel
#import joblib




app = Flask(__name__)



########################################################################

@app.route('/weather',methods=['GET'])
def get_weather_data():
    
    location = request.args.get('location')
    ph = round(float(request.args.get('pH')),1)
    start_month = request.args.get('start_month')
    end_month = request.args.get('end_month')
    
    wf = WeatherForecast()
    temp,temp_data = wf.cal_temp(location, start_month, end_month)
    humi,humi_data = wf.cal_humi(location, start_month, end_month)
    rain,rain_data = wf.cal_rain(location, start_month, end_month)
    
    predicted_crop = None
    # Create the response using the results
    if temp and humi and rain and ph:
        
        pc = PredictedCrop()
        predicted_crop = pc.get_crop(temp, humi, rain, ph)
        
    if predicted_crop:
        response = {
        'Average temp': temp,
        'Average humi': humi,
        'Average rain': rain,
        'pH value': ph,
        'Suitable crop': predicted_crop,
        'tempd': temp_data.to_json(),
        'humid': humi_data.to_json(),
        'raind': rain_data.to_json()
    }
        return jsonify(response)
    else:
        response = {
        'Average temp': temp,
        'Average humi': humi,
        'Average rain': rain,
        'pH value': ph,
        'Suitable crop': None,
        'tempd': temp_data.to_json(),
        'humid': humi_data.to_json(),
        'raind': rain_data.to_json()
    }
        return jsonify(response)
    return "",204



##############################################################

@app.route('/location',methods=['POST'])
def update_location():
    
    file = request.files['csv_file']
    location = request.form['location']
    data = pd.read_csv(file,skiprows=11)
    

    df1 = data.loc[data.PARAMETER == "TS"]
    df1 = pd.melt(df1, id_vars=['YEAR'], value_vars=['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC'], var_name='MONTH', value_name='TEMP')
    df2 = data.loc[data.PARAMETER == "RH2M"]
    df2 = pd.melt(df2, id_vars=['YEAR'], value_vars=['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC'], var_name='MONTH', value_name='RH2M')
    df3 = data.loc[data.PARAMETER == "PRECTOTCORR_SUM"]
    df3 = pd.melt(df3, id_vars=['YEAR'], value_vars=['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC'], var_name='MONTH', value_name='RAINFALL')
    dfn = pd.DataFrame()
    dfn["YEAR"] = df1["YEAR"]
    dfn["MONTH"] = df1["MONTH"]
    dfn["TEMP"] = df1["TEMP"]
    dfn["RH2M"] = df2["RH2M"]
    dfn["RAINFALL"] = df3["RAINFALL"]
    dfn["MONTH"] = dfn["MONTH"].replace({"JAN":"01","FEB":"02","MAR":"03","APR":"04","MAY":"05","JUN":"06","JUL":"07","AUG":"08","SEP":"09","OCT":"10","NOV":"11","DEC":"12"})
    dfn['DATE'] = pd.to_datetime(dfn['YEAR'].astype(str) + '-' + dfn['MONTH'].astype(str), format='%Y-%m')
    dfn = dfn.sort_values(by = "DATE")
    dfn.drop(["YEAR","MONTH"],axis = 1, inplace=True)
    dfn.set_index("DATE",inplace=True)
    df = dfn.loc["2015-12-01":"2021-12-01"]
    lm = LocationModel()
    try:
        lm.create_temp_model(df,location)
        lm.create_rain_model(df,location)
        lm.create_humi_model(df,location)
        return "Successfully created",201
    except Exception as e:
        print(e)
        return "Something went wrong",400

if __name__ == '__main__':
    app.run(debug=True)