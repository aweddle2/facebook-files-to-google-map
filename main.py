from dotenv import load_dotenv
from facebook_client import FacebookClient

import os

load_dotenv()

groupId = os.getenv('FACEBOOK_GROUP_ID')
email = os.getenv('FACEBOOK_USERNAME')
password = os.getenv('FACEBOOK_PASSWORD')

facebookClient = FacebookClient(email, password)
facebookClient.getFilesForGroup(groupId)
