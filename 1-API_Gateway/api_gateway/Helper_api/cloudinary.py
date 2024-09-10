import cloudinary
import cloudinary.uploader
import os
from dotenv import load_dotenv


load_dotenv('.env')

def uploadCloudinaryFile(file):
    print('Cloudinary upload: ', os.getenv('CLOUD_API_KEY'))
    cloudinary.config(
        cloud_name= os.getenv('CLOUD_NAME'),
        api_key= os.getenv('CLOUD_API_KEY'),
        api_secret= os.getenv('CLOUD_API_SECRET')
    )
    upload_result = cloudinary.uploader.upload(file)
    file_url = upload_result['url']
    return file_url