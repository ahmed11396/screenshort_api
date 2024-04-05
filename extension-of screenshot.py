from flask import Flask, jsonify
from selenium import webdriver
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

# Path to the ChromeDriver executable
chromedriver_path = '/path/to/chromedriver'

# AWS RDS database credentials
db_username = 'your_db_username'
db_password = 'your_db_password'
db_endpoint = 'your_db_endpoint'
db_name = 'your_db_name'

# Database connection URL
db_url = f'mysql+pymysql://{db_username}:{db_password}@{db_endpoint}/{db_name}'

# Create an engine and sessionmaker
engine = create_engine(db_url)
Session = sessionmaker(bind=engine)

# Define a base class for declarative table definitions
Base = declarative_base()

# Define a table for storing screenshot paths
class Screenshot(Base):
    __tablename__ = 'screenshots'
    id = Column(Integer, primary_key=True)
    path = Column(String(255), nullable=False)

# Create the table in the database
Base.metadata.create_all(engine)

@app.route('/api/take_screenshot', methods=['GET'])
def take_screenshot():
    # Configure Chrome options
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')  # Run Chrome in headless mode (without GUI)

    # Create a Chrome webdriver instance
    driver = webdriver.Chrome(executable_path=chromedriver_path, options=chrome_options)

    # Open the webpage
    url = 'https://www.example.com'
    driver.get(url)

    # Take a screenshot
    screenshot_path = 'screenshots/screenshot.png'
    driver.save_screenshot(screenshot_path)

    # Close the browser
    driver.quit()

    # Add the screenshot path to the database
    session = Session()
    screenshot = Screenshot(path=screenshot_path)
    session.add(screenshot)
    session.commit()
    session.close()

    return jsonify({'message': 'Screenshot taken and saved to database'})

if __name__ == '__main__':
    app.run(debug=True)
