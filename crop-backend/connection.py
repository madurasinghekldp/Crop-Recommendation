from pymongo import MongoClient
import boto3

class Connection:
    def __init__(self):
        access_key = 'AKIAVAPWN6G7EL3FJKAE'
        secret_key = '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'
        self.s3 = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key)

        # specify the bucket and file names        
        self.bucket_name = 'sldpweather'
    

        client = MongoClient("mongodb+srv://dulan:dulan@crops.3nnglyt.mongodb.net/?retryWrites=true&w=majority")
        db = client.get_database("crop_db")
        self.records = db.crop_records
        self.record_list = list(self.records.find())