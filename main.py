from dotenv import load_dotenv
from facebook_client import FacebookClient
from file_manager import FileManager

import os

load_dotenv()
groupId = os.getenv('FACEBOOK_GROUP_ID')
email = os.getenv('FACEBOOK_USERNAME')
password = os.getenv('FACEBOOK_PASSWORD')

filesBaseDirectory = os.getcwd()+'/files/'

fileManager = FileManager(filesBaseDirectory)

fileManager.emptyDirectory(groupId)

folderForGroup = filesBaseDirectory+groupId
facebookClient = FacebookClient(email, password)
facebookClient.getFilesForGroup(groupId, folderForGroup)
