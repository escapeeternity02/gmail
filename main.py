import time
import random
import psycopg2
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from fake_useragent import UserAgent
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from undetected_chromedriver.v2 import Chrome, ChromeOptions

# Set up undetected-chromedriver
options = ChromeOptions()
user_agent = UserAgent().random
options.add_argument(f"user-agent={user_agent}")
options.add_argument("--headless")
options.add_argument("--disable-extensions")

# Set up the proxy (replace with your actual proxy if needed)
proxy = "http://your_proxy_here:port"
options.add_argument(f'--proxy-server={proxy}')

# Launch undetected Chrome driver
driver = Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Connect to PostgreSQL (Render provides you with database credentials)
conn = psycopg2.connect(
    host="your_db_host",
    port="your_db_port",
    user="your_db_user",
    password="your_db_password",
    dbname="your_db_name"
)
cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS gmail_accounts (
        email VARCHAR(255),
        password VARCHAR(255)
    );
""")
conn.commit()

# Wait to simulate human-like behavior
def human_like_delay():
    time.sleep(random.uniform(2, 5))

# Function to create a Gmail account and store email/password in PostgreSQL
def create_and_store_gmail_account():
    # Open Gmail signup page
    driver.get("https://accounts.google.com/signup")
    human_like_delay()

    # Simulate human typing and actions
    first_name = driver.find_element(By.ID, "firstName")
    first_name.send_keys("John")
    human_like_delay()
    last_name = driver.find_element(By.ID, "lastName")
    last_name.send_keys("Doe")
    human_like_delay()
    
    # Create a random username
    username = f"john.doe{random.randint(1000, 9999)}"
    driver.find_element(By.ID, "username").send_keys(username)
    human_like_delay()
    
    # Password and confirmation
    password = "TestPassword1234"
    driver.find_element(By.NAME, "Passwd").send_keys(password)
    human_like_delay()
    driver.find_element(By.NAME, "ConfirmPasswd").send_keys(password)

    # Submit the form (after filling out email/password)
    driver.find_element(By.NAME, "ConfirmPasswd").send_keys(Keys.RETURN)

    # Simulate human scrolling and interactions
    scroll_y = random.randint(100, 500)
    driver.execute_script(f"window.scrollTo(0, {scroll_y});")
    human_like_delay()

    # Save email and password to PostgreSQL
    cursor.execute("""
        INSERT INTO gmail_accounts (email, password)
        VALUES (%s, %s)
    """, (f"{username}@gmail.com", password))
    conn.commit()

    # Output for debugging
    print(f"Created account: {username}@gmail.com with password: {password}")

# Run the function to create and store Gmail account info in PostgreSQL
create_and_store_gmail_account()

# Finish and close the browser
driver.quit()

# Close the database connection
cursor.close()
conn.close()
