from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Firefox()
driver.get("http://apphost:5000")

email = driver.find_element_by_name("email")
email.clear()
email.send_keys("dyotamo@gmail.com")

email = driver.find_element_by_name("password")
email.clear()
email.send_keys("passwd")

submit = driver.find_element_by_tag_name("button")
submit.send_keys(Keys.RETURN)

driver.close()
