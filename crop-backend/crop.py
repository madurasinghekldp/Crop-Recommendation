from connection import Connection
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

class PredictedCrop:
    def get_crop(self,temp_,humi_,rain_,ph_):
        mdb = Connection()
        
        records = mdb.records
        record_list = mdb.record_list

        # Define the input variables (temperature, humidity, ph, rainfall)
        temperature = ctrl.Antecedent(np.arange(0, 51, 0.1), 'temperature')
        humidity = ctrl.Antecedent(np.arange(0, 101, 0.1), 'humidity')
        ph = ctrl.Antecedent(np.arange(0, 11, 0.1), 'ph')
        rainfall = ctrl.Antecedent(np.arange(0, 501, 0.1), 'rainfall')

        temp = temp_
        hum = humi_
        pH = ph_
        rain = rain_
        
        print("pH and temp and rain and hum:",pH,temp,rain,hum)

        crop_dict = {}

        # Define the output variable (crop)
        # Define the output variable (crop)
        output_var_list = [None]*records.count_documents({})

        for index, crop in enumerate(record_list):
            try:
                temperature[crop['name']] = fuzz.trimf(temperature.universe, [crop['temp_min']-0.1,(crop['temp_min']+crop['temp_max'])/2,crop['temp_max']+0.1])
                humidity[crop['name']] = fuzz.trimf(humidity.universe, [crop['humi_min']-0.1,(crop['humi_min']+crop['humi_max'])/2,crop['humi_max']+0.1])
                ph[crop['name']] = fuzz.trimf(ph.universe, [crop['pH_min']-0.1,(crop['pH_min']+crop['pH_max'])/2,crop['pH_max']+0.1])
                rainfall[crop['name']] = fuzz.trimf(rainfall.universe, [crop['rain_min']-0.1,(crop['rain_min']+crop['rain_max'])/2,crop['rain_max']+0.1])
            except:
                continue

            output_var_list[index] = ctrl.Consequent(np.arange(0, 100, 1), crop['name'])
            output_var_list[index]['suitable'] = fuzz.trimf(output_var_list[index].universe, [0, 100, 100])
            output_var_list[index].defuzzify_method = 'som'
            rule = ctrl.Rule(temperature[crop['name']] & ph[crop['name']] & humidity[crop['name']] & rainfall[crop['name']], output_var_list[index]['suitable'])

            # Create the fuzzy control system
            try:
                crop_ctrl = ctrl.ControlSystem([rule])
            except:
                
                continue
            suitability = ctrl.ControlSystemSimulation(crop_ctrl)

            # Replace these values with the actual data from your dataset
            suitability.input['temperature'] = temp
            suitability.input['humidity'] = hum
            suitability.input['ph'] = pH
            suitability.input['rainfall'] = rain
            try:
                suitability.compute()
            except:
                
                continue

            suitability_value = suitability.output[crop['name']]
            #print(f"Suitability of {crop['name']}: ",suitability_value)
            membership = fuzz.interp_membership(output_var_list[index].universe, output_var_list[index].terms['suitable'].mf, suitability_value)
            #print("Membership value: ",membership)
            #output_var_list[index].view(sim=suitability)
            if suitability_value > 0:
                crop_dict[crop['name']] = suitability_value
        try:        
            max_key = max(crop_dict, key=lambda key: crop_dict[key])
            print(max_key)
            return max_key
        except:
            return None