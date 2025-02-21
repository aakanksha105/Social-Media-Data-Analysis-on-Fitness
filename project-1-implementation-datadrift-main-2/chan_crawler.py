from chan_client import ChanClient
import logging
from pyfaktory import Client, Consumer, Job, Producer
import psycopg2
from psycopg2.extras import Json
from psycopg2.extensions import register_adapter
import os
import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Logger setup
logger = logging.getLogger("4chan crawler")
logger.setLevel(logging.INFO)
sh = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
sh.setFormatter(formatter)
logger.addHandler(sh)

# Register adapter for JSON data in PostgreSQL
register_adapter(dict, Json)

# Load environment variables
load_dotenv()

# Load necessary environment variables
FAKTORY_SERVER_URL = os.getenv("FAKTORY_SERVER_URL")
DATABASE_URL = os.getenv("DATABASE_URL")

def thread_numbers_from_catalog(catalog):
    return [thread["no"] for page in catalog for thread in page.get("threads", [])]

def find_dead_threads(previous_catalog_thread_numbers, current_catalog_thread_numbers):
    return set(previous_catalog_thread_numbers).difference(current_catalog_thread_numbers)

def crawl_thread(board, thread_number):
    chan_client = ChanClient()
    thread_data = chan_client.get_thread(board, thread_number)
    
    logger.info(f"Thread: {board}/{thread_number}/: {thread_data}")

    if thread_data:
        conn = psycopg2.connect(dsn=DATABASE_URL)
        cur = conn.cursor()

        # Insert thread data into DB
        for post in thread_data.get("posts", []):
            post_number = post["no"]
            cur.execute(
                "INSERT INTO posts (board, thread_number, post_number, data) VALUES (%s, %s, %s, %s) RETURNING id",
                (board, thread_number, post_number, post)
            )
            conn.commit()
            db_id = cur.fetchone()[0]
            logging.info(f"Inserted DB id: {db_id}")

        cur.close()
        conn.close()
    else:
        logger.error(f"Failed to fetch thread {thread_number}.")

def crawl_catalog(board, previous_catalog_thread_numbers=[]):
    chan_client = ChanClient()
    current_catalog = chan_client.get_catalog(board)
    if not current_catalog:
        logger.error("Failed to fetch catalog.")
        return

    current_catalog_thread_numbers = thread_numbers_from_catalog(current_catalog)
    dead_threads = find_dead_threads(previous_catalog_thread_numbers, current_catalog_thread_numbers)
    logger.info(f"Dead threads: {dead_threads}")

    crawl_thread_jobs = []
    with Client(faktory_url=FAKTORY_SERVER_URL, role="producer") as client:
        producer = Producer(client=client)
        for thread in current_catalog_thread_numbers:
            job = Job(jobtype="crawl-thread", args=(board, thread), queue="crawl-thread")
            crawl_thread_jobs.append(job)

        producer.push_bulk(crawl_thread_jobs)

    # Schedule the next catalog crawl
    with Client(faktory_url=FAKTORY_SERVER_URL, role="producer") as client:
        producer = Producer(client=client)
        run_at = (datetime.datetime.utcnow() + datetime.timedelta(minutes=5)).isoformat()[:-7] + "Z"
        job = Job(jobtype="crawl-catalog", args=(board, current_catalog_thread_numbers), queue="crawl-catalog", at=run_at)
        producer.push(job)

if __name__ == "__main__":
    with Client(faktory_url=FAKTORY_SERVER_URL, role="consumer") as client:
        consumer = Consumer(client=client, queues=["crawl-catalog", "crawl-thread"], concurrency=5)
        consumer.register("crawl-catalog", crawl_catalog)
        consumer.register("crawl-thread", crawl_thread)
        consumer.run()
