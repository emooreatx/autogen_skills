from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

def take_fullpage_screenshot(url, save_path, filename):
    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_argument("--start-maximized")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(url)
        time.sleep(5)

        # Calculate the total height of the page
        total_height = driver.execute_script("return document.body.parentNode.scrollHeight")
        driver.set_window_size(1920, total_height)  # Set the window size to the total height
        time.sleep(2)  # Wait for the page to load after resizing

        # Ensure the directory exists
        os.makedirs(save_path, exist_ok=True)
        full_path = os.path.join(save_path, filename)

        driver.save_screenshot(full_path)
        print(f"Full page screenshot taken and saved as '{full_path}'.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()
