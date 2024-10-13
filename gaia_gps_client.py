from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
from os import listdir
from os.path import isfile, join


class GaiaGpsClient():
    username = ''
    password = ''
    gaiaGpsUrl = 'https://www.gaiagps.com/'
    driver = None
    wait = None

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def __login(self):

        options = ChromeOptions()
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-popup-blocking")

        self.driver = Chrome(options)
        self.wait = WebDriverWait(self.driver, timeout=10)

        self.driver.get(self.gaiaGpsUrl)

        time.sleep(1)

        loginButton = self.driver.find_element(
            By.XPATH, '//button[contains(text(), "Log In") and @type="button"]')
        loginButton.click()

        time.sleep(1)

        emailElement = self.driver.find_element(By.ID, 'login-email')
        emailElement.send_keys(self.username)

        passElement = self.driver.find_element(By.ID, 'login-password')
        passElement.send_keys(self.password)

        secondLoginButton = self.driver.find_element(
            By.XPATH, '//button[contains(text(), "Log In") and @type="submit"]')
        secondLoginButton.click()

        time.sleep(10)

    def importFromLocalFiles(self, path: str, gaiaGpsFolderName: str):
        self.__login()

        self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//span[contains(text(), "Saved Items")]')))

        # TODO Better error handling here
        # Lets check there's a GaiaGS folder of the correct name
        # Click Saved Items
        savedItemsSpan = self.driver.find_element(
            By.XPATH, '//span[contains(text(), "Saved Items")]')
        savedItemsSpan.click()

        # Wait for the animation to run
        time.sleep(2)

        self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//span[contains(text(), "'+gaiaGpsFolderName+'")]')))

        folderNameSpan = self.driver.find_element(
            By.XPATH, '//span[contains(text(), "'+gaiaGpsFolderName+'")]')
        folderNameSpan.click()

        # If we get here then we can upload
        # We need to import then move

        # Generate the string to send to the upload input
        allFilePaths = ''
        for uploadFile in [f for f in listdir(path) if isfile(join(path, f))]:
            allFilePaths += uploadFile + " \n "

        # Click Select Files
        selectFilesInput = self.driver.find_element(
            By.XPATH, '//input[@type="file"]')
        selectFilesInput.send_keys(allFilePaths)
