import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from fake_useragent import UserAgent
from flask import Flask, jsonify
import chromedriver_autoinstaller
from undetected_chromedriver.v2 import Chrome, ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager

# Set up Flask app
app = Flask(__name__)

# List to store created accounts
created_accounts = []

# Install Chrome and Chromedriver
chromedriver_autoinstaller.install()  # This will automatically install the correct version of ChromeDriver

# Path to ChromeDriver
chrome_path = chromedriver_autoinstaller.install()  # Path to ChromeDriver

# Set up undetected-chromedriver options
options = ChromeOptions()
user_agent = UserAgent().random
options.add_argument(f"user-agent={user_agent}")
options.add_argument("--headless")  # If you want the browser to run without GUI (headless mode)
options.add_argument("--disable-extensions")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Set binary location for Chrome
options.binary_location = "/usr/bin/google-chrome"  # Render's default Chrome path

# Launch undetected Chrome driver
driver = Chrome(options=options)

# Function to create a Gmail account
def create_gmail_account():
    driver.get("https://accounts.google.com/signup")
    time.sleep(random.uniform(2, 5))

    # Fill out the form
    driver.find_element(By.ID, "firstName").send_keys("John")
    time.sleep(random.uniform(2, 5))

    driver.find_element(By.ID, "lastName").send_keys("Doe")
    time.sleep(random.uniform(2, 5))

    username = f"john.doe{random.randint(1000, 9999)}"
    driver.find_element(By.ID, "username").send_keys(username)
    time.sleep(random.uniform(2, 5))

    password = "TestPassword1234"
    driver.find_element(By.NAME, "Passwd").send_keys(password)
    time.sleep(random.uniform(2, 5))

    driver.find_element(By.NAME, "ConfirmPasswd").send_keys(password)
    time.sleep(random.uniform(2, 5))

    driver.find_element(By.NAME, "ConfirmPasswd").send_keys(Keys.RETURN)
    time.sleep(random.uniform(2, 5))

    # Store account info in created_accounts
    account_info = {"email": f"{username}@gmail.com", "password": password}
    created_accounts.append(account_info)

    # Write account to a text file
    with open("accounts.txt", "a") as file:
        file.write(f"{account_info['email']} | {account_info['password']}\n")

    print(f"Created account: {username}@gmail.com with password: {password}")

# Create a Gmail account (repeatable if needed)
create_gmail_account()

# Flask route to display accounts in JSON format
@app.route('/accounts', methods=['GET'])
def show_accounts():
    return jsonify(created_accounts)

@app.route('/')
def home():
    return "Welcome to the Gmail Automation Service!"

# Run Flask server
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8000)

# After automation ends, close the driver (important for cleanup)
driver.quit()
