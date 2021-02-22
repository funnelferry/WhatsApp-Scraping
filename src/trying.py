
import configparser
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome("./chromedriver")
driver.get("http://web.whatsapp.com")

time.sleep(10)

# get the name of all the chat contacts
for chatter in driver.find_elements_by_xpath("//div[@class='']"):
    # now we look for the element with the chat name
    chatter_name = chatter.find_element_by_xpath(".//span[contains(@class, '_1wjpf _3NFp9 _3FXB1')]").text
    print(chatter_name)
    
    # now we get the information in a specific chat
    chatter.find_element_by_xpath(".//div[contains(@class,'_3j7s9')]").click()
    chat_section = driver.find_element_by_xpath("//div[@class='tSmQ1']")
    
    # scroll until the start of conversation
    while not driver.find_elements_by_xpath(".//span[@data-icon='lock-small']"):
        chat_section.send_keys(Keys.CONTROL + Keys.HOME)
        time.sleep(2)
        
    # create text_file to save messages
    chat_file = open("wa_chats/convo-{}.txt".format(chatter_name), 'w+', encoding="utf8")

    # grab all the messages a
    for messages in driver.find_elements_by_xpath(
        "//div[contains(@class,'message-in')] | //div[contains(@class,'message-out')]"):
        
        final_message = ""
        # get message text and emojis
        try:
            message = ""
            emojis = []

            message_container = messages.find_element_by_xpath(
                ".//div[@class='copyable-text']")
            
            message_details = message_container.get_attribute("data-pre-plain-text").replace("]", " -").strip("[")
            final_message += message_details
            
            message = message_container.find_element_by_xpath(
                ".//span[contains(@class,'selectable-text invisible-space copyable-text')]"
            ).text
            final_message += message
            
            for emoji in message_container.find_elements_by_xpath(
                ".//img[contains(@class,'selectable-text invisible-space copyable-text')]"
            ):
                emojis.append(emoji.get_attribute("data-plain-text"))
            final_message.join(emojis)
                
        except NoSuchElementException:  # In case there are only emojis in the message
            try:
                message = ""
                emojis = []
                message_container = messages.find_element_by_xpath(
                    ".//div[@class='copyable-text']")
                message_details = message_container.get_attribute("data-pre-plain-text").replace("]", " -").strip("[")
                final_message += message_details
                for emoji in message_container.find_elements_by_xpath(
                        ".//img[contains(@class,'selectable-text invisible-space copyable-text')]"
                ):
                    emojis.append(emoji.get_attribute("data-plain-text"))
                final_message.join(emojis)
            except NoSuchElementException:
                pass
            
            
        # now, to format the message into a similar style as a whatsapp exported chat
        # format follows the following: dd/mm/yyyy, hh:mm - [username]: [chat_message]
        msg = final_message + "\n"
        chat_file.write(msg)
    chat_file.close()