from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException

import time
import os
from os import listdir
from os.path import isfile, join


class GaiaGpsClient():
    username = ''
    password = ''
    gaiaGpsUrl = 'https://www.gaiagps.com/'
    driver = None
    wait = None
    actions = None
    fileExtensions = ['.GPX', '.KML', '.KMZ', '.FIT', 'GeoJSON']

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def __login(self):

        options = ChromeOptions()
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-popup-blocking")

        self.driver = Chrome(options)
        self.wait = WebDriverWait(self.driver, timeout=30)
        self.actions = ActionChains(self.driver)

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
        # We need to import then move

        # Generate the string to send to the upload input
        for uploadFile in [f for f in listdir(path) if isfile(join(path, f))]:
            # lets see if the extension can even be uploaded to GaiaGPS
            fileName, fileExtension = os.path.splitext(uploadFile)
            # If it's not then continue to the next file
            if (fileExtension.upper() not in self.fileExtensions):
                continue

            filePath = path + os.sep + uploadFile.replace(' ', '\ ')

            self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, '//span[contains(text(), "Import Data")]')))

            # TODO Better error handling here
            self.driver.find_element(
                By.XPATH, '//span[contains(text(), "Import Data")]').click()

            # Wait for the animation to run
            time.sleep(2)

            # Upload to the hidden input type=file
            self.driver.find_element(
                By.XPATH, '//input[@type="file"]').send_keys(filePath)

            # Wait for the file to be read
            time.sleep(2)

            # If there's a <h5>Large file import</h5> then deal with that
            try:
                self.driver.find_element(
                    By.XPATH, '//h5[contains(text(), "Large file import")]')

                # Import just the tracks
                self.wait.until(EC.element_to_be_clickable(
                    (By.XPATH, '//input[@name="tracks"]')))
                self.driver.find_element(
                    By.XPATH, '//input[@name="tracks"]').click()
                self.wait.until(EC.element_to_be_clickable(
                    (By.XPATH, '//button[contains(text(),"Import")]')))
                self.driver.find_element(
                    By.XPATH, '//button[contains(text(),"Import")]').click()
            except NoSuchElementException:
                pass

            # Click Save button
            self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, '//button[contains(text(),"Save") and contains(text(),"item") ]')))
            self.driver.find_element(
                By.XPATH, '//button[contains(text(),"Save") and contains(text(),"item") ]').click()

            # Click Change Folder Button
            self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, '//span[contains(text(), "Change Folder")]')))
            self.driver.find_element(
                By.XPATH, '//span[contains(text(), "Change Folder")]').click()

            # Click the folder for the folder with the same name as the passed in folder name
            self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, '//span[contains(text(), "More Folders")]')))
            self.driver.find_element(
                By.XPATH, '//span[contains(text(), "More Folders")]').click()
            self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//input[@placeholder='Search folders']")))
            self.driver.find_element(
                By.XPATH, "//input[@placeholder='Search folders']").send_keys(gaiaGpsFolderName)
            self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, '//p[contains(text(), "'+gaiaGpsFolderName+'")]/parent::div/following-sibling::div/button[text()="Move"]')))

            self.driver.find_element(
                By.XPATH, '//p[contains(text(), "'+gaiaGpsFolderName+'")]/parent::div/following-sibling::div/button[text()="Move"]').click()
