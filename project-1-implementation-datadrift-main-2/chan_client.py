# 4chan api client that has minimal functionality to collect data

import logging
import requests

# logger setup
logger = logging.getLogger("4chan client")
logger.propagate = False
logger.setLevel(logging.INFO)
sh = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
sh.setFormatter(formatter)
logger.addHandler(sh)

class ChanClient:
    API_BASE = "http://a.4cdn.org"

    # Get JSON for a given thread on any board
    def get_thread(self, board, thread_number):
        request_pieces = [board, "thread", f"{thread_number}.json"]
        api_call = self.build_request(request_pieces)
        return self.execute_request(api_call)

    # Get the catalog for a given board
    def get_catalog(self, board):
        request_pieces = [board, "catalog.json"]
        api_call = self.build_request(request_pieces)
        return self.execute_request(api_call)

    # Build the API request URL
    def build_request(self, request_pieces):
        return "/".join([self.API_BASE] + request_pieces)

    # Make the HTTP request and handle errors
    def execute_request(self, api_call):
        try:
            resp = requests.get(api_call, timeout=30)  # 30 seconds timeout
            resp.raise_for_status()
            logger.info(f"Success: {resp.status_code}")
            return resp.json()  # Return parsed JSON data
        except requests.exceptions.HTTPError as http_err:
            logger.error(f"HTTP error: {http_err}")
        except requests.exceptions.RequestException as req_err:
            logger.error(f"Request error: {req_err}")
        except ValueError as json_err:
            logger.error(f"JSON decode error: {json_err}")
        return None

# Test script for the ChanClient
if __name__ == "__main__":
    client = ChanClient()
    
    # Fetch and print the catalog for the /fit/ board
    catalog = client.get_catalog("fit")
    if catalog:
        for page in catalog:
            for thread in page.get("threads", []):
                thread_number = thread['no']
                title = thread.get('sub', 'No Title')
                print(f"Thread Number: {thread_number} - Title: {title}")

                # Optionally, fetch the thread data itself
                thread_data = client.get_thread("fit", thread_number)
                if thread_data:
                    print(f"Thread {thread_number} content: {thread_data}")
