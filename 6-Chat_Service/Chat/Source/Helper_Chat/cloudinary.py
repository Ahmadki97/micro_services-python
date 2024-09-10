import cloudinary
import cloudinary.exceptions
import cloudinary.uploader
import os
from dotenv import load_dotenv
from Helper_Chat.logHandler import logger


load_dotenv('.env')

def uploadCloudinaryFile(file):
    try:
        print('Cloudinary upload: ', os.getenv('CLOUD_API_KEY'))
        cloudinary.config(
            cloud_name= os.getenv('CLOUD_NAME'),
            api_key= os.getenv('CLOUD_API_KEY'),
            api_secret= os.getenv('CLOUD_API_SECRET')
        )
        upload_result = cloudinary.uploader.upload(file)
        return upload_result
    except cloudinary.exceptions as err:
        logger.error(f"Error while trying to upload file to cloudinary : {str(err)}")