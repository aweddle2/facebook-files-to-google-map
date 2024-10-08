from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from dotenv import load_dotenv
import shutil

import time
import os

load_dotenv()


def getFileElements():
    return driver.find_elements(
        By.XPATH, "//div[@class='x6s0dn4 x78zum5 x1y1aw1k x1sxyh0 xwib8y2 xurb0ha']")


facebookUrl = 'https://www.facebook.com/'
groupId = os.getenv('FACEBOOK_GROUP_ID')
email = os.getenv('FACEBOOK_USERNAME')
password = os.getenv('FACEBOOK_PASSWORD')

groupFilesUrl = facebookUrl+'/groups/'+groupId+'/files/files'
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

driver = webdriver.Chrome(options)
actions = ActionChains(driver)

driver.get(facebookUrl)

emailElement = driver.find_element(By.ID, 'email')
emailElement.send_keys(email)

passElement = driver.find_element(By.ID, 'pass')
passElement.send_keys(password)

loginButton = driver.find_element(By.NAME, 'login')
loginButton.click()

time.sleep(5)

driver.get(groupFilesUrl)

keepScrolling = True
while keepScrolling:
    fileElementCount = len(getFileElements())

    # scroll to the bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)

    newFileElementCount = len(getFileElements())

    # if the count is the same before and after the scroll then we at the bottom
    if (fileElementCount == newFileElementCount):
        keepScrolling = False

for fileElement in getFileElements():
    try:
        # Get the download link
        fileNameLink = fileElement.find_element(By.TAG_NAME, 'a')

        # Get the ellipsis and click it to get the post URL
        elipsisElement = fileElement.find_element(By.TAG_NAME, 'i')
        actions.move_to_element(elipsisElement).perform()

        elipsisElement.click()

        linkElement = driver.find_element(
            By.XPATH, "//div[@class='xu96u03 xm80bdy x10l6tqk x13vifvy']")
        anchorTags = linkElement.find_elements(By.TAG_NAME, 'a')
        # First one is the download link and should be the same as the above a
        downloadATag = anchorTags[0]
        downloadATag.click()
        # Second one is the original post which we will add to the google map once we get there.
        originalPostATag = anchorTags[1]

        print(fileNameLink.text+" : "+originalPostATag.get_attribute('href'))
    except Exception as e:
        # print("error, skipping file")
        # print(e)
        pass


driver.quit()
