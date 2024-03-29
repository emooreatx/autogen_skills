import os
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.common.by import By

def search_and_extract_content(search_query, save_path='./', filename='search_results.json'):
    binary_path = '/opt/chromedriver' if os.path.exists('/opt/chromedriver') else None
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    service = Service(ChromeDriverManager(path=binary_path).install()) if binary_path is not None else Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        # Navigate to Google
        driver.get('https://www.google.com')
        time.sleep(2)  # Wait for the page to load

        # Find the search box, enter the search query, and submit
        search_box = driver.find_element(By.NAME, 'q')
        search_box.send_keys(search_query)
        search_box.submit()
        time.sleep(5)  # Wait for search results to load

        page_text = driver.find_element(By.TAG_NAME, 'body').text  
        links = driver.find_elements(By.TAG_NAME, 'a')  
        urls = {link.text: link.get_attribute('href') for link in links if link.text and link.get_attribute('href')}  
  
        # Extract image links and alt text  
        images = driver.find_elements(By.TAG_NAME, 'img')  
        image_info = {img.get_attribute('src'): img.get_attribute('alt') for img in images if img.get_attribute('src')}  

        content = {
            'text': page_text,
            'urls': urls,
            'images': image_info
        }

        # Ensure save_path exists
        if not os.path.exists(save_path):
            os.makedirs(save_path)

        # Save the extracted content
        with open(os.path.join(save_path, filename), 'w', encoding='utf-8') as file:
            json.dump(content, file, indent=4)

    except WebDriverException as e:
        print(f'Error occurred: {e}')
    finally:
        driver.quit()
