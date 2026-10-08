import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def main():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1280,1024")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get("http://localhost:5000")
        time.sleep(1)

        driver.find_element(By.ID, "first_name").send_keys("Ada")
        driver.find_element(By.ID, "last_name").send_keys("Lovelace")
        driver.find_element(By.ID, "email").send_keys("ada@example.com")
        driver.find_element(By.ID, "submit_button").click()

        time.sleep(2)
        print(driver.page_source)
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
