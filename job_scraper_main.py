import threading
import time
from worker.worker import start_scraping_worker
import logging
from config.config import setup_logging
from database.database import create_table, count_jobs

# Setup logging for the whole app
setup_logging()

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info("Starting the web scraper worker")
    create_table()

    # Log the total job count before starting
    logger.info("Total jobs in the database: %s", count_jobs())

    # Start the worker thread to run the scraper periodically
    worker_thread = threading.Thread(target=start_scraping_worker, daemon=True)
    worker_thread.start()

    # Keep the main thread alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Shutdown signal received. Shutting down...")
        
        # Set the stop flag or handle the thread shutdown properly
        # Set the stop flag to True if using it in your worker
        stop_worker = True