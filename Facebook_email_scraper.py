import os
import pandas as pd
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains  # Import ActionChains
from selenium.webdriver.common.keys import Keys  # Import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import logging

# Set up Chrome options for headless mode
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--enable-unsafe-swiftshader')  # Enable SwiftShader
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])  # Suppress logging

# Initialize logger
logging.basicConfig(level=logging.INFO)


# Initialize the WebDriver (this will be passed to each thread)
def init_driver():
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)


# Read the profile URLs from the Input folder
input_file_path = os.path.join('Input', 'facebook_links.txt')
with open(input_file_path, 'r') as file:
    profile_links = file.readlines()

# Regex pattern for email addresses
email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'  # Pattern for email addresses


# Function to extract email from a profile
def extract_email(profile):
    profile = profile.strip()  # Remove any trailing newlines or spaces
    about_page_url = profile + '/about'  # Append '/about' to navigate directly to the About section

    driver = init_driver()  # Initialize a new WebDriver instance for each thread

    try:
        driver.get(about_page_url)

        # Wait for the page to load and the email element to be present
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

        # Press the Escape key to close the login popup
        actions = ActionChains(driver)
        actions.send_keys(Keys.ESCAPE).perform()

        # Initialize email variable
        email = 'N/A'

        # Get the page source and find the email address using regex
        page_source = driver.page_source
        email_match = re.search(email_pattern, page_source)
        if email_match:
            email = email_match.group()
            logging.info(f"Email found: {email} for profile: {profile}")

        return [profile, email]

    except Exception as e:
        logging.error(f"Error with profile {profile}: {str(e)}")
        return [profile, 'Error']

    finally:
        driver.quit()


# Ensure the Output folder exists
os.makedirs('Output', exist_ok=True)

# Use ThreadPoolExecutor to process profiles concurrently
with ThreadPoolExecutor(max_workers=4) as executor:
    results = list(executor.map(extract_email, profile_links))

# Save the results to an Excel file
timestamp = datetime.now().strftime('%d_%b_%Y_%I_%M_%p')
output_file_path = os.path.join('Output', f'facebook_data_{timestamp}.xlsx')

df = pd.DataFrame(results, columns=['Profile URL', 'Email'])
df.to_excel(output_file_path, index=False)

logging.info(f"Data saved to {output_file_path}")
