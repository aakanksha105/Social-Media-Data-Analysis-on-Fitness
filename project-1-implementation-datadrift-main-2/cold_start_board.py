import logging
from pyfaktory import Client, Consumer, Job, Producer
import time
import random
import sys
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

logger = logging.getLogger("faktory test")
logger.propagate = False
logger.setLevel(logging.INFO)
sh = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
sh.setFormatter(formatter)
logger.addHandler(sh)

if __name__ == "__main__":
    boards = ["fit", "pol"]  # Include both /fit/ and /pol/ boards
    logger.info(f"Cold starting catalog crawl for boards {boards}")

    # Default url for a Faktory server running locally
    FAKTORY_SERVER_URL = os.getenv("FAKTORY_SERVER_URL")

    for board in boards:
        logger.info(f"Starting cold start for board {board}")
        
        with Client(faktory_url=FAKTORY_SERVER_URL, role="producer") as client:
            producer = Producer(client=client)
            job = Job(jobtype="crawl-catalog", args=(board,), queue="crawl-catalog")
            try:
                producer.push(job)
                logger.info(f"Job for crawling catalog of board {board} has been pushed.")
            except Exception as e:
                logger.error(f"Failed to push job for board {board}: {e}")
