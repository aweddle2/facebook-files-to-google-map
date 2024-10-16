import shutil
import os


class FileManager():
    basePath = ''

    def __init__(self, basePath: str):
        self.basePath = basePath

    def deleteDirectory(self, folderName):
        fullFolderPath = self.basePath+folderName
        shutil.rmtree(fullFolderPath, ignore_errors=True)

    def createDirectory(self, folderName):
        fullFolderPath = self.basePath+folderName
        os.makedirs(fullFolderPath)

    def emptyDirectory(self, folderName):
        self.deleteDirectory(folderName)
        self.createDirectory(folderName)

    def removeSpacesFromFileNames(self, folderName):
        fullFolderPath = self.basePath+folderName
        filenames = os.listdir(fullFolderPath)
        for filename in filenames:
            os.rename(os.path.join(fullFolderPath, filename), os.path.join(
                fullFolderPath, filename.replace(' ', '-')))
