from dotenv import load_dotenv
from facebook_client import FacebookClient
from gaia_gps_client import GaiaGpsClient
from file_manager import FileManager

import os

load_dotenv()
groupId = os.getenv('FACEBOOK_GROUP_ID')
facebookEmail = os.getenv('FACEBOOK_USERNAME')
facebookPassword = os.getenv('FACEBOOK_PASSWORD')

filesBaseDirectory = os.getcwd()+'/files/'

fileManager = FileManager(filesBaseDirectory)
fileManager.removeSpacesFromFileNames(groupId)
fileManager.emptyDirectory(groupId)

folderForGroup = filesBaseDirectory+groupId
facebookClient = FacebookClient(facebookEmail, facebookPassword)
groupFiles = facebookClient.getFilesForGroup(groupId, folderForGroup)

for groupFile in groupFiles:
    print(groupFile.filename+" : "+groupFile.originalPostUrl)

gaiaGpsEmail = os.getenv('GAIAGPS_USERNAME')
gaiaGpsPassword = os.getenv('GAIAGPS_PASSWORD')

gaiaGpsClient = GaiaGpsClient(gaiaGpsEmail, gaiaGpsPassword)
gaiaGpsClient.importFromLocalFiles(folderForGroup, groupId)
