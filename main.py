import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from fake_useragent import UserAgent
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from undetected_chromedriver import Chrome, ChromeOptions
from flask import Flask, jsonify

# Set up Flask app
app = Flask(__name__)

# List to store created accounts
created_accounts = []

# Set up undetected-chromedriver
options = ChromeOptions()
user_agent = UserAgent().random
options.add_argument(f"user-agent={user_agent}")
options.add_argument("--headless")
options.add_argument("--disable-extensions")

# Launch undetected Chrome driver
driver = Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Function to create a Gmail account
def create_gmail_account():
    # Open Gmail signup page
    driver.get("https://accounts.google.com/signup")
    time.sleep(random.uniform(2, 5))

    # Simulate human typing and actions
    first_name = driver.find_element(By.ID, "firstName")
    first_name.send_keys("John")
    time.sleep(random.uniform(2, 5))

    last_name = driver.find_element(By.ID, "lastName")
    last_name.send_keys("Doe")
    time.sleep(random.uniform(2, 5))

    # Create a random username
    username = f"john.doe{random.randint(1000, 9999)}"
    driver.find_element(By.ID, "username").send_keys(username)
    time.sleep(random.uniform(2, 5))

    # Password and confirmation
    password = "TestPassword1234"
    driver.find_element(By.NAME, "Passwd").send_keys(password)
    time.sleep(random.uniform(2, 5))

    driver.find_element(By.NAME, "ConfirmPasswd").send_keys(password)
    time.sleep(random.uniform(2, 5))

    # Submit the form (after filling out email/password)
    driver.find_element(By.NAME, "ConfirmPasswd").send_keys(Keys.RETURN)

    # Simulate human scrolling and interactions
    scroll_y = random.randint(100, 500)
    driver.execute_script(f"window.scrollTo(0, {scroll_y});")
    time.sleep(random.uniform(2, 5))

    # Save account details to created_accounts list
    account_info = {"email": f"{username}@gmail.com", "password": password}
    created_accounts.append(account_info)

    # Write to a text file (store accounts)
    with open("accounts.txt", "a") as file:
        file.write(f"{account_info['email']} | {account_info['password']}\n")

    # Output for debugging
    print(f"Created account: {username}@gmail.com with password: {password}")

# Create a new Gmail account (can be repeated for multiple accounts)
create_gmail_account()

# Flask route to display accounts as JSON
@app.route('/accounts', methods=['GET'])
def show_accounts():
    return jsonify(created_accounts)

@app.route('/')
def home():
    return "Welcome to the Gmail Automation Service!"

# Run the Flask web server
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8000)

# Finish and close the browser after running the automation
driver.quit()
