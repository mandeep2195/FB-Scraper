import os
import pandas as pd
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
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
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

# Initialize logger
logging.basicConfig(level=logging.INFO)

# Initialize the WebDriver (this will be passed to each thread)
def init_driver():
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Read the profile URLs from the Input folder
input_file_path = r'C:\Users\Harry\Desktop\FB-Scraper\Input\facebook_links.txt'
with open(input_file_path, 'r') as file:
    profile_links = file.readlines()
logging.info(f"Profile links loaded: {profile_links}")
if not profile_links:
    logging.error("No profile links found in the input file.")
    exit(1)

# Regex pattern for email addresses
email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'

# Function to extract email and phone number from a profile
def extract_contact_info(profile):
    import time  # Import time if not already imported at the top

    profile = profile.strip()  # Remove any trailing newlines or spaces
    about_page_url = profile + '/about'  # Append '/about' to navigate directly to the About section

    driver = init_driver()  # Initialize a new WebDriver instance for each thread

    try:
        driver.get(about_page_url)

        # Wait for the page to load and the body element to be present
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

        # Press the Escape key to close the login popup
        actions = ActionChains(driver)
        actions.send_keys(Keys.ESCAPE).perform()

        # Initialize email and phone variables
        email = 'N/A'
        phone = 'N/A'

        # Extract email using regex
        page_source = driver.page_source
        email_match = re.search(email_pattern, page_source)
        if email_match:
            email = email_match.group()
            logging.info(f"Extracted email: {email}")

        # Extract phone number using XPath
        try:
            phone_xpath = "//span[contains(text(), '+') and contains(@class, 'x193iq5w')]"
            phone_element = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, phone_xpath))
            )
            phone = phone_element.text.strip()
            logging.info(f"Extracted phone number: {phone}")
        except Exception as e:
            logging.warning(f"Phone number not found for profile {profile}: {str(e)}")

        logging.info(f"Contact Info - Email: {email}, Phone: {phone} for profile: {profile}")

        return [profile, email, phone]

    except Exception as e:
        logging.error(f"Error with profile {profile}: {str(e)}")
        return [profile, 'Error', 'Error']

    finally:
        driver.quit()

    # Add a delay before moving to the next profile
    time.sleep(2)  # Pause for 2 seconds

# Ensure the Output folder exists
output_folder = r"C:\Users\Harry\Desktop\FB-Scraper\Output"
os.makedirs(output_folder, exist_ok=True)

# Use ThreadPoolExecutor to process profiles concurrently
with ThreadPoolExecutor(max_workers=4) as executor:
    results = list(executor.map(extract_contact_info, profile_links))

# Save the results to an Excel file
timestamp = datetime.now().strftime('%d_%b_%Y_%I_%M_%p')
output_file_path = os.path.join(output_folder, f'facebook_contact_data_{timestamp}.xlsx')

logging.info(f"Saving file to {output_file_path}")

df = pd.DataFrame(results, columns=['Profile URL', 'Email', 'Phone'])
df.to_excel(output_file_path, index=False)

logging.info(f"Data saved to {output_file_path}")
