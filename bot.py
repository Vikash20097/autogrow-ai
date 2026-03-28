#!/usr/bin/env python3
"""
Instagram Auto-Poster Bot
Using Selenium WebDriver for automated Instagram posting
"""

import os
import time
import random
import sqlite3
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('instagram_bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class InstagramBot:
    def __init__(self, username, password, headless=False):
        """
        Initialize Instagram Bot
        
        Args:
            username (str): Instagram username
            password (str): Instagram password
            headless (bool): Run browser in headless mode
        """
        self.username = username
        self.password = password
        self.driver = None
        self.wait = None
        self.headless = headless
        self.base_url = "https://www.instagram.com"
        
    def setup_driver(self):
        """Setup Chrome WebDriver with options"""
        try:
            chrome_options = Options()
            
            if self.headless:
                chrome_options.add_argument("--headless")
            
            # Add common Chrome arguments for better compatibility
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            # Set user agent to avoid detection
            chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
            
            # Install and setup ChromeDriver
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            
            # Set window size
            self.driver.set_window_size(1080, 720)
            
            # Wait setup
            self.wait = WebDriverWait(self.driver, 10)
            
            logger.info("Chrome WebDriver initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to setup WebDriver: {e}")
            return False
    
    def random_delay(self, min_seconds=2, max_seconds=5):
        """Add random delay for human-like behavior"""
        delay = random.uniform(min_seconds, max_seconds)
        logger.info(f"Waiting for {delay:.2f} seconds...")
        time.sleep(delay)
    
    def safe_click(self, element, description="element"):
        """Safely click an element with retry logic"""
        max_retries = 3
        for attempt in range(max_retries):
            try:
                self.random_delay(1, 3)
                element.click()
                logger.info(f"Successfully clicked {description}")
                return True
            except Exception as e:
                logger.warning(f"Attempt {attempt + 1} to click {description} failed: {e}")
                if attempt < max_retries - 1:
                    self.random_delay(2, 4)
                else:
                    logger.error(f"Failed to click {description} after {max_retries} attempts")
                    return False
        return False
    
    def safe_send_keys(self, element, text, description="field"):
        """Safely send keys to an element with retry logic"""
        max_retries = 3
        for attempt in range(max_retries):
            try:
                self.random_delay(1, 2)
                element.clear()
                element.send_keys(text)
                logger.info(f"Successfully entered text in {description}")
                return True
            except Exception as e:
                logger.warning(f"Attempt {attempt + 1} to send keys to {description} failed: {e}")
                if attempt < max_retries - 1:
                    self.random_delay(2, 4)
                else:
                    logger.error(f"Failed to send keys to {description} after {max_retries} attempts")
                    return False
        return False
    
    def login(self):
        """Login to Instagram"""
        try:
            logger.info("Opening Instagram...")
            self.driver.get(self.base_url)
            self.random_delay(3, 5)
            
            # Wait for login page to load
            try:
                username_field = self.wait.until(
                    EC.presence_of_element_located((By.NAME, "username"))
                )
                password_field = self.wait.until(
                    EC.presence_of_element_located((By.NAME, "password"))
                )
                login_button = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
                )
            except TimeoutException:
                logger.error("Login page elements not found")
                return False
            
            # Enter credentials
            logger.info("Entering login credentials...")
            if not self.safe_send_keys(username_field, self.username, "username field"):
                return False
            
            if not self.safe_send_keys(password_field, self.password, "password field"):
                return False
            
            # Click login
            if not self.safe_click(login_button, "login button"):
                return False
            
            self.random_delay(3, 6)
            
            # Handle "Save Info" popup if it appears
            try:
                save_info_button = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Not Now')]")),
                    timeout=5
                )
                self.safe_click(save_info_button, "save info not now button")
            except TimeoutException:
                logger.info("No save info popup appeared")
            
            # Handle notifications popup if it appears
            try:
                not_now_button = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Not Now')]")),
                    timeout=5
                )
                self.safe_click(not_now_button, "notifications not now button")
            except TimeoutException:
                logger.info("No notifications popup appeared")
            
            # Verify login success by checking if we're on the homepage
            try:
                self.wait.until(
                    EC.presence_of_element_located((By.XPATH, "//a[@href='/explore/']"))
                )
                logger.info("Login successful!")
                return True
            except TimeoutException:
                logger.error("Login verification failed")
                return False
                
        except Exception as e:
            logger.error(f"Login failed: {e}")
            return False
    
    def get_latest_post_from_db(self):
        """Fetch latest pending post from database"""
        try:
            # Connect to the existing database
            db_path = os.path.join(os.path.dirname(__file__), 'instance', 'autogrow.db')
            
            if not os.path.exists(db_path):
                logger.error(f"Database not found at {db_path}")
                return None
            
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Get the latest pending post
            cursor.execute("""
                SELECT id, caption, image, platform, category, priority, schedule_time, status
                FROM post 
                WHERE status = 'pending' 
                ORDER BY created_at DESC 
                LIMIT 1
            """)
            
            post_data = cursor.fetchone()
            conn.close()
            
            if post_data:
                post = {
                    'id': post_data[0],
                    'caption': post_data[1],
                    'image': post_data[2],
                    'platform': post_data[3],
                    'category': post_data[4],
                    'priority': post_data[5],
                    'schedule_time': post_data[6],
                    'status': post_data[7]
                }
                logger.info(f"Found post: {post['caption'][:50]}...")
                return post
            else:
                logger.info("No pending posts found in database")
                return None
                
        except Exception as e:
            logger.error(f"Failed to fetch post from database: {e}")
            return None
    
    def upload_post(self, image_path, caption):
        """Upload a post to Instagram"""
        try:
            logger.info("Starting post upload...")
            
            # Click on create post button (+ icon)
            try:
                create_button = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//div[@role='button' and @aria-label='New post']"))
                )
                if not self.safe_click(create_button, "create post button"):
                    return False
            except TimeoutException:
                # Alternative selector for create button
                try:
                    create_button = self.wait.until(
                        EC.element_to_be_clickable((By.XPATH, "//span[@aria-label='New post']"))
                    )
                    if not self.safe_click(create_button, "create post button (alternative)"):
                        return False
                except TimeoutException:
                    logger.error("Could not find create post button")
                    return False
            
            self.random_delay(2, 4)
            
            # Upload image file
            try:
                file_input = self.wait.until(
                    EC.presence_of_element_located((By.XPATH, "//input[@type='file']"))
                )
                
                # Make file input visible if needed
                self.driver.execute_script("arguments[0].style.display = 'block';", file_input)
                
                if not self.safe_send_keys(file_input, image_path, "file input"):
                    return False
                
                self.random_delay(3, 5)
                
            except TimeoutException:
                logger.error("File input not found")
                return False
            
            # Click Next button
            try:
                next_button = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Next')]"))
                )
                if not self.safe_click(next_button, "next button"):
                    return False
                self.random_delay(2, 4)
            except TimeoutException:
                logger.error("Next button not found")
                return False
            
            # Add caption
            try:
                caption_field = self.wait.until(
                    EC.presence_of_element_located((By.XPATH, "//textarea[@aria-label='Write a caption…']"))
                )
                
                # Add hashtags based on category
                hashtags = self.get_hashtags_for_category(caption, post.get('category', 'general'))
                
                if not self.safe_send_keys(caption_field, hashtags, "caption field"):
                    return False
                
                self.random_delay(1, 3)
                
            except TimeoutException:
                logger.error("Caption field not found")
                return False
            
            # Click Share button
            try:
                share_button = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Share')]"))
                )
                if not self.safe_click(share_button, "share button"):
                    return False
                
                self.random_delay(3, 6)
                
                # Wait for upload to complete
                try:
                    self.wait.until(
                        EC.invisibility_of_element_located((By.XPATH, "//button[contains(text(), 'Share')]")),
                        timeout=30
                    )
                    logger.info("Post uploaded successfully!")
                    return True
                except TimeoutException:
                    logger.warning("Post upload may still be in progress")
                    return True
                    
            except TimeoutException:
                logger.error("Share button not found")
                return False
                
        except Exception as e:
            logger.error(f"Post upload failed: {e}")
            return False
    
    def get_hashtags_for_category(self, caption, category):
        """Generate hashtags based on category"""
        hashtag_map = {
            'gym': '#gym #fitness #workout #motivation #fitlife',
            'salon': '#salon #beauty #hair #makeup #style #glamour',
            'cafe': '#cafe #coffee #food #lunch #brunch #foodie',
            'business': '#business #entrepreneur #startup #success #motivation #hustle',
            'fashion': '#fashion #style #outfit #trending #ootd #fashionista',
            'travel': '#travel #wanderlust #adventure #explore #vacation #travelgram',
            'tech': '#tech #technology #innovation #gadgets #programming #coding',
            'health': '#health #wellness #lifestyle #fit #nutrition #healthy',
            'education': '#education #learning #knowledge #study #school #university',
            'general': '#instagood #photooftheday #instadaily #picoftheday #instamood'
        }
        
        base_hashtags = hashtag_map.get(category.lower(), hashtag_map['general'])
        
        # Add some general hashtags
        general_hashtags = " #follow #like #share"
        
        return f"{caption}\n\n{base_hashtags}{general_hashtags}"
    
    def mark_post_as_posted(self, post_id):
        """Mark post as posted in database"""
        try:
            db_path = os.path.join(os.path.dirname(__file__), 'instance', 'autogrow.db')
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            cursor.execute(
                "UPDATE post SET status = 'posted' WHERE id = ?",
                (post_id,)
            )
            conn.commit()
            conn.close()
            
            logger.info(f"Marked post {post_id} as posted")
            return True
            
        except Exception as e:
            logger.error(f"Failed to update post status: {e}")
            return False
    
    def run(self):
        """Main execution method"""
        try:
            logger.info("Starting Instagram Bot...")
            
            # Setup WebDriver
            if not self.setup_driver():
                return False
            
            # Login to Instagram
            if not self.login():
                logger.error("Login failed, exiting...")
                return False
            
            # Get latest post from database
            post = self.get_latest_post_from_db()
            if not post:
                logger.info("No posts to upload, exiting...")
                return True
            
            # Check if image exists
            image_path = os.path.join(os.path.dirname(__file__), 'static', 'uploads', post['image'])
            if not os.path.exists(image_path):
                logger.error(f"Image file not found: {image_path}")
                return False
            
            # Upload post
            if self.upload_post(image_path, post['caption']):
                # Mark as posted
                self.mark_post_as_posted(post['id'])
                logger.info("Post uploaded and marked as completed successfully!")
            else:
                logger.error("Post upload failed")
                return False
            
            # Wait before closing
            self.random_delay(3, 5)
            
            return True
            
        except Exception as e:
            logger.error(f"Bot execution failed: {e}")
            return False
        
        finally:
            # Cleanup
            if self.driver:
                self.driver.quit()
                logger.info("Browser closed")

def main():
    """Main function to run the bot"""
    # Configuration - Replace with your Instagram credentials
    INSTAGRAM_USERNAME = "your_instagram_username"
    INSTAGRAM_PASSWORD = "your_instagram_password"
    
    # Create bot instance
    bot = InstagramBot(
        username=INSTAGRAM_USERNAME,
        password=INSTAGRAM_PASSWORD,
        headless=False  # Set to True for headless mode
    )
    
    # Run the bot
    success = bot.run()
    
    if success:
        logger.info("Bot completed successfully!")
    else:
        logger.error("Bot failed!")

if __name__ == "__main__":
    main()