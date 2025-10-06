from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions

def setup():
    options = ChromeOptions()
    options.headless = True
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.google.com")
    input("Press Enter to quit...") 
    driver.quit()
    return driver

if __name__ == "__main__":
    setup()