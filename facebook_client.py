from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import shutil

import time
import os


class FacebookClient():
    username = ''
    password = ''
    facebookUrl = 'https://www.facebook.com/'
    driver = None

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def __getFileElements(self):
        return self.driver.find_elements(
            By.XPATH, "//div[@class='x6s0dn4 x78zum5 x1y1aw1k x1sxyh0 xwib8y2 xurb0ha']")

    def getFilesForGroup(self, groupId: str, filter=None):

        groupFilesUrl = self.facebookUrl+'/groups/'+groupId+'/files/files'
        downloadDirectory = os.getcwd()+'/files/'+groupId

        options = webdriver.ChromeOptions()
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-popup-blocking")
        shutil.rmtree(downloadDirectory, ignore_errors=True)
        os.makedirs(downloadDirectory)
        prefs = {}
        prefs["profile.default_content_settings.popups"] = 0
        prefs["download.default_directory"] = downloadDirectory
        options.add_experimental_option("prefs", prefs)

        self.driver = webdriver.Chrome(options)
        actions = ActionChains(self.driver)

        self.driver.get(self.facebookUrl)

        emailElement = self.driver.find_element(By.ID, 'email')
        emailElement.send_keys(self.username)

        passElement = self.driver.find_element(By.ID, 'pass')
        passElement.send_keys(self.password)

        loginButton = self.driver.find_element(By.NAME, 'login')
        loginButton.click()

        time.sleep(5)

        self.driver.get(groupFilesUrl)

        keepScrolling = True
        while keepScrolling:
            fileElementCount = len(self.__getFileElements())

            # scroll to the bottom
            self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)

            newFileElementCount = len(self.__getFileElements())

            # if the count is the same before and after the scroll then we at the bottom
            if (fileElementCount == newFileElementCount):
                keepScrolling = False

        for fileElement in self.__getFileElements():
            try:
                # Get the download link
                fileNameLink = fileElement.find_element(By.TAG_NAME, 'a')

                # Get the ellipsis and click it to get the post URL
                elipsisElement = fileElement.find_element(By.TAG_NAME, 'i')
                actions.move_to_element(elipsisElement).perform()

                elipsisElement.click()

                linkElement = self.driver.find_element(
                    By.XPATH, "//div[@class='xu96u03 xm80bdy x10l6tqk x13vifvy']")
                anchorTags = linkElement.find_elements(By.TAG_NAME, 'a')
                # First one is the download link and should be the same as the above a
                downloadATag = anchorTags[0]
                downloadATag.click()
                # Second one is the original post which we will add to the google map once we get there.
                originalPostATag = anchorTags[1]

                print(fileNameLink.text+" : " +
                      originalPostATag.get_attribute('href'))
            except Exception as e:
                # print("error, skipping file")
                # print(e)
                pass

        self.driver.quit()
