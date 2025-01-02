
# Facebook Email Scraper

## Description
This script is designed to extract email addresses from Facebook profile URLs using Selenium and a headless Chrome WebDriver. It takes a list of profile links from a text file, navigates to the About section of each profile, and uses regex to extract email addresses from the page source. The results are saved to an Excel file in the Output folder.

## Prerequisites
Before running this script, ensure you have the following installed:
- Python 3.7 or higher
- Required Python packages (install using the command below)

## Installation
1. Clone this repository or download the script.
2. Install the necessary Python packages:
   ```bash
   pip install -r requirements.txt
   ```
   Dependencies :
   ```plaintext
   pandas
   selenium
   webdriver_manager
   ```
3.  Folder structure:
   ```
   FB-Scraper/
   ├── Input/
   │   └── facebook_links.txt
   ├── Output/
   │   └── facebook_data<timestamp>.xlsx
   ├── Facebook_email_scraper.py 
   ├── LICENSE 
   ├── README.md (This File.) 
   └── requirements.txt 

   ```

## Usage
1. Add the Facebook profile URLs (one per line) to `Input/facebook_links.txt`.
2. Run the script:
   ```bash
   python Facebook_email_scraper.py
   ```
3. The script will save the extracted emails in an Excel file in the `Output` folder with a timestamped filename (e.g., `facebook_data_01_Jan_2025_12_00_PM.xlsx`).

## Features
- Headless Chrome WebDriver for seamless scraping.
- Multi-threading with `ThreadPoolExecutor` for faster processing.
- Email extraction using regex.

## Logs
The script logs information about the process and any errors encountered. Logs are displayed in the console.

## Notes
- This script does not bypass Facebook's authentication mechanisms.
- Ensure compliance with Facebook's terms of service when using this script.

## License
- This project is licensed under the GNU General Public License v3.0.
