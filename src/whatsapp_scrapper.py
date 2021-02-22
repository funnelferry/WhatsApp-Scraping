"""
Importing the libraries that we are going to use
for loading the settings file and scraping the website
"""
import csv
import pdb
import time
from selenium import webdriver
from selenium.common.exceptions import (NoSuchElementException,
                                        StaleElementReferenceException)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys


class WhatsappScrapper():
    def __init__(self, page, browser, browser_path):
        self.page = page
        self.browser = browser
        self.browser_path = browser_path
        self.driver = self.load_driver()

        # Open the web page with the given browser
        self.driver.get(self.page)

    def load_driver(self):
        """
        Load the Selenium driver depending on the browser
        (Edge and Safari are not running yet)
        """
        driver = None
        if self.browser == 'firefox':
            firefox_profile = webdriver.FirefoxProfile(
                self.browser_path)
            driver = webdriver.Firefox(firefox_profile)
        elif self.browser == 'chrome':
            chrome_options = webdriver.ChromeOptions()
            if self.browser_path:
                chrome_options.add_argument('user-data-dir=' +
                                            self.browser_path)
            driver = webdriver.Chrome(options=chrome_options)
        elif self.browser == 'safari':
            pass
        elif self.browser == 'edge':
            pass

        return driver

    def open_conversation(self, name):
        """
        Function that search the specified user by the 'name' and opens the conversation.
        """

        while True:
            for chatter in self.driver.find_elements_by_xpath("//div[@id='pane-side']/div/div/div/div"):
                chatter_path = ".//span[@title='{}']".format(
                    name)

                # Wait until the chatter box is loaded in DOM
                try:
                    WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located(
                            (By.XPATH, "//span[contains(@title,'{}')]".format(
                                name)))
                    )
                except StaleElementReferenceException:
                    WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located(
                            (By.XPATH, "//span[contains(@title,'{}')]".format(
                                name)))
                    )

                try:
                    chatter_name = chatter.find_element_by_xpath(
                        chatter_path).text
                    if chatter_name == name:
                        chatter.find_element_by_xpath(
                            ".//div/div").click()
                        return True
                except Exception as e:
                    pass

    def scroll_n_save(self, n):
        """
        Reading the last message that you got in from the chatter
        Params:
        n = number of scrolls to go above in chat
        """
        i = 0

        while(i<n):
            chat_section = self.driver.find_element_by_xpath(
                "//div[@aria-label='Message list. Press right arrow key on a message to open message context menu.']"
            )
            chat_section.send_keys(Keys.CONTROL + Keys.HOME)
            time.sleep(2)
            i = i+1

        all_messages = []

        for messages in self.driver.find_elements_by_xpath(
        "//div[contains(@class,'message-in')] | //div[contains(@class,'message-out')]"):
            final_message = ""
            # get message text and emojis
            try:
                message = ""
                emojis = ""

                message_container = messages.find_element_by_xpath(
                    ".//div[@class='copyable-text']")
                
                message_details = message_container.get_attribute("data-pre-plain-text").replace("]", ",").strip("[")
                message_info = message_details.split(', ')
                message_info[2] = message_info[2][:-2]
                final_message += message_details
                
                message = message_container.find_element_by_xpath(
                    ".//span[contains(@class,'selectable-text copyable-text')]"
                ).text
                final_message += message
                
                for emoji in message_container.find_elements_by_xpath(
                    ".//img[contains(@class,'selectable-text copyable-text')]"
                ):
                    emojis += (emoji.get_attribute("data-plain-text"))
                message += emojis
                message_info.append(message)
                all_messages.append(message_info)
                    
            except NoSuchElementException:  # In case there are only emojis in the message
                try:
                    message = ""
                    emojis = ""
                    message_container = messages.find_element_by_xpath(
                        ".//div[@class='copyable-text']")
                    # message_details = message_container.get_attribute("data-pre-plain-text").replace("]", " -").strip("[")
                    message_details = message_container.get_attribute("data-pre-plain-text").replace("]", ",").strip("[")
                    message_info = message_details.split(', ')
                    message_info[2] = message_info[2][:-2]
                    final_message += message_details
                    for emoji in message_container.find_elements_by_xpath(
                            ".//img[contains(@class,'selectable-text copyable-text')]"
                    ):
                        emojis += (emoji.get_attribute("data-plain-text"))
                    message_info.append(emojis)
                    all_messages.append(message_info)
                except NoSuchElementException:
                    pass
        
        fields = ['Timestamp', 'Date', 'SentBy', 'Message']
        with open('GFG.csv', 'w') as f: 
      
            # using csv.writer method from CSV package 
            write = csv.writer(f) 
            
            write.writerow(fields) 
            write.writerows(all_messages) 