import os
import psycopg2
from psycopg2.extras import Json
from dotenv import load_dotenv
from pyfaktory import Client, Job, Producer
import logging
import time
from reddit_client import RedditClient

# Load environment variables
load_dotenv()

# Logger setup
logger = logging.getLogger("Reddit Crawler")
logger.setLevel(logging.INFO)
sh = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
sh.setFormatter(formatter)
logger.addHandler(sh)

# Reddit API credentials and subreddits
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
USER_AGENT = os.getenv("USER_AGENT")
FITNESS_SUBREDDITS = os.getenv("FITNESS_SUBREDDITS").split(",")
POLITICS_SUBREDDITS = os.getenv("POLITICS_SUBREDDITS").split(",")
DATABASE_URL = os.getenv("DATABASE_URL")
FAKTORY_SERVER_URL = os.getenv("FAKTORY_SERVER_URL")

# Initialize the Reddit client
reddit_client = RedditClient(USER_AGENT, FAKTORY_SERVER_URL)

# Track the last processed post ID to ensure we're only fetching new posts
last_processed_post_id = {}

def store_reddit_comments(post_id, comments, category):
    """Store Reddit post comments into the correct table based on category"""
    try:
        conn = psycopg2.connect(dsn=DATABASE_URL)
        cur = conn.cursor()

        for comment in comments:
            comment_data = comment.get('data', {})
            comment_id = comment_data.get('id')
            subreddit = comment_data.get('subreddit', '')  # Ensure subreddit is present

            # Check if comment already exists before inserting
            cur.execute("SELECT 1 FROM reddit_comments WHERE comment_id = %s", (comment_id,))
            if cur.fetchone():
                logger.info(f"Comment {comment_id} already exists. Skipping insert.")
                continue  # Skip if comment already exists

            if category == 'fitness':
                cur.execute(
                    "INSERT INTO reddit_comments (post_id, subreddit, comment_id, data) VALUES (%s, %s, %s, %s) RETURNING comment_id",
                    (post_id, subreddit, comment_id, Json(comment_data))
                )
            elif category == 'politics':
                cur.execute(
                    "INSERT INTO reddit_politics_comments (post_id, subreddit, comment_id, data) VALUES (%s, %s, %s, %s) RETURNING comment_id",
                    (post_id, subreddit, comment_id, Json(comment_data))
                )

        conn.commit()
        logger.info(f"Inserted comments for post {post_id}")
    except Exception as e:
        logger.error(f"Error storing Reddit comments: {str(e)}")
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

def store_reddit_data(post_data, category):
    """Store Reddit post data into the PostgreSQL database"""
    try:
        post_id = post_data['id']
        subreddit = post_data.get('subreddit')
        if not post_id or not subreddit:
            logger.error(f"Post data is missing 'id' or 'subreddit' field: {post_data}")
            return

        conn = psycopg2.connect(dsn=DATABASE_URL)
        cur = conn.cursor()

        # Check if post already exists
        cur.execute(
            "SELECT 1 FROM reddit_posts WHERE subreddit = %s AND post_id = %s",
            (subreddit, post_id)
        )
        if cur.fetchone():
            logger.info(f"Post {post_id} in r/{subreddit} already exists. Skipping insert.")
            return  # Skip if the post already exists

        created_utc = post_data.get('created_utc')
        if created_utc:
            created_utc = float(created_utc)  

        if category == 'fitness':
            cur.execute(
                "INSERT INTO reddit_posts (post_id, subreddit, title, content, created_utc, author, url, num_comments, score, data) "
                "VALUES (%s, %s, %s, %s, to_timestamp(%s), %s, %s, %s, %s, %s) RETURNING post_id",
                (post_id, subreddit, post_data.get('title'), post_data.get('content'),
                 created_utc, post_data.get('author'), post_data.get('url'),
                 post_data.get('num_comments'), post_data.get('score'), Json(post_data))
            )
        elif category == 'politics':
            cur.execute(
                "INSERT INTO reddit_politics_posts (post_id, subreddit, title, content, created_utc, author, url, num_comments, score, data) "
                "VALUES (%s, %s, %s, %s, to_timestamp(%s), %s, %s, %s, %s, %s) RETURNING post_id",
                (post_id, subreddit, post_data.get('title'), post_data.get('content'),
                 created_utc, post_data.get('author'), post_data.get('url'),
                 post_data.get('num_comments'), post_data.get('score'), Json(post_data))
            )

        conn.commit()
        db_id = cur.fetchone()[0]  # Return the post_id after insert
        logger.info(f"Inserted Reddit post with DB post_id: {db_id}")
    except Exception as e:
        logger.error(f"Error storing Reddit post data: {str(e)}")
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

def fetch_and_store_reddit_data(subreddits, category):
    """Fetch and store posts and comments from a list of subreddits (fitness or politics)"""
    for subreddit in subreddits:
        logger.info(f"Fetching posts from r/{subreddit}")
        posts = reddit_client.get_posts(subreddit)
        
        if posts:
            for post in posts['data']['children']:
                post_data = post['data']
                post_id = post_data['id']

                # Skip already processed posts (real-time, new posts)
                if post_id <= last_processed_post_id.get(subreddit, ''):
                    continue

                store_reddit_data(post_data, category)

                # Fetch comments for each post
                comments = reddit_client.get_comments(post_id, subreddit)
                if comments:
                    store_reddit_comments(post_id, comments[1]['data']['children'], category)

                last_processed_post_id[subreddit] = post_id  # Update the last processed post ID

def schedule_reddit_crawl():
    """Schedule the next Reddit crawl using Faktory"""
    with Client(faktory_url=FAKTORY_SERVER_URL, role="producer") as client:
        producer = Producer(client=client)

        for subreddit in FITNESS_SUBREDDITS:
            job = Job(jobtype="crawl-reddit", args=(subreddit, 'fitness'), queue="crawl-reddit")
            producer.push(job)

        for subreddit in POLITICS_SUBREDDITS:
            job = Job(jobtype="crawl-reddit", args=(subreddit, 'politics'), queue="crawl-reddit")
            producer.push(job)

if __name__ == "__main__":
    while True:
        fetch_and_store_reddit_data(FITNESS_SUBREDDITS, 'fitness')
        fetch_and_store_reddit_data(POLITICS_SUBREDDITS, 'politics')
        time.sleep(60)  # Wait for 1 minute before fetching new posts
