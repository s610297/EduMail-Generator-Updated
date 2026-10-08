import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def main():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1280,1200")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    try:
        driver.get('http://localhost:5000')
        time.sleep(1)

        alias_input = driver.find_element(By.ID, 'alias')
        alias_input.send_keys('demouser')
        driver.find_element(By.ID, 'create-inbox').click()
        time.sleep(1)

        inbox_id = driver.find_element(By.ID, 'inbox-id').text
        print('New inbox created:', inbox_id)

        driver.find_element(By.ID, 'send-otp').click()
        time.sleep(1)

        otp = driver.find_element(By.ID, 'otp-code').text
        print('Generated OTP:', otp)

    finally:
        driver.quit()


if __name__ == '__main__':
    main()
