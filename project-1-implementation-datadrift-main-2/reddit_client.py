import logging
import requests
import time
from pyfaktory import Client, Job, Producer
from datetime import datetime, timedelta
import os

# Logger setup
logger = logging.getLogger("Reddit Client")
logger.setLevel(logging.INFO)
sh = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
sh.setFormatter(formatter)
logger.addHandler(sh)

class RedditClient:
    API_BASE = "https://www.reddit.com"

    def __init__(self, user_agent, faktory_url):
        """Initialize RedditClient with a user-agent and Faktory URL"""
        self.user_agent = user_agent
        self.faktory_url = faktory_url
        logger.info("RedditClient initialized with User-Agent: %s", self.user_agent)

    def get_posts(self, subreddit, limit=10, retry_count=10):
        """Fetch the latest posts from a given subreddit"""
        url = f"{self.API_BASE}/r/{subreddit}/new.json?limit={limit}"
        headers = {'User-Agent': self.user_agent}
        for i in range(retry_count):
            try:
                response = requests.get(url, headers=headers, timeout=30)
                response.raise_for_status()  # Check if the request was successful
                logger.info(f"Successfully fetched posts from r/{subreddit}")
                return response.json()  # Return the JSON data containing posts
            except requests.exceptions.RequestException as e:
                if response.status_code == 429:  # If it's a 429 error (rate limit exceeded)
                    # Exponential backoff logic: Wait longer before retrying
                    backoff_time = 2 ** i  # Exponential backoff (2^i)
                    logger.warning(f"Rate limit exceeded for r/{subreddit}. Retrying in {backoff_time} seconds...")
                    time.sleep(backoff_time)
                    self.reschedule_job(subreddit, backoff_time)
                else:
                    logger.error(f"Error fetching posts from r/{subreddit}: {e}")
                    return None
        logger.error(f"Max retries reached for fetching posts from r/{subreddit}. Skipping...")
        return None

    def get_comments(self, post_id, subreddit, retry_count=5):
        """Fetch comments for a specific Reddit post"""
        url = f"{self.API_BASE}/r/{subreddit}/comments/{post_id}.json"
        headers = {'User-Agent': self.user_agent}
        for i in range(retry_count):
            try:
                response = requests.get(url, headers=headers, timeout=30)
                response.raise_for_status()
                logger.info(f"Successfully fetched comments for post {post_id} from r/{subreddit}")
                return response.json()
            except requests.exceptions.RequestException as e:
                if response.status_code == 429:  # If it's a 429 error
                    backoff_time = 2 ** i  # Exponential backoff (2^i)
                    logger.warning(f"Rate limit exceeded for r/{subreddit} on post {post_id}. Retrying in {backoff_time} seconds...")
                    time.sleep(backoff_time)
                    self.reschedule_job(subreddit, backoff_time, post_id)
                else:
                    logger.error(f"Error fetching comments for post {post_id} in r/{subreddit}: {e}")
                    return None
        logger.error(f"Max retries reached for fetching comments for post {post_id}. Skipping...")
        return None

    def reschedule_job(self, subreddit, delay, post_id=None):
        """Reschedule a failed job in Faktory"""
        try:
            with Client(faktory_url=self.faktory_url, role="producer") as client:
                producer = Producer(client=client)
                if post_id:
                    job = Job(jobtype="crawl-comments", args=(subreddit, post_id), queue="crawl-comments", at=(datetime.utcnow() + timedelta(seconds=delay)).strftime('%Y-%m-%dT%H:%M:%S') + ".000Z")
                else:
                    job = Job(jobtype="crawl-posts", args=(subreddit,), queue="crawl-posts", at=(datetime.utcnow() + timedelta(seconds=delay)).strftime('%Y-%m-%dT%H:%M:%S') + ".000Z")
                producer.push(job)
                logger.info(f"Job for {subreddit} rescheduled with a delay of {delay} seconds.")
        except Exception as e:
            logger.error(f"Failed to reschedule job for {subreddit} due to: {e}")

