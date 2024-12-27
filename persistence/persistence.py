import csv
import os
import logging
from config.config import CSV_FILE

logger = logging.getLogger(__name__)

def save_to_csv(job_data):
    """Save job listings to CSV file."""
    file_exists = os.path.isfile(CSV_FILE)

    with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=job_data[0].keys())
        if not file_exists:
            writer.writeheader()  # Write header only if file is empty
        writer.writerows(job_data)
        logger.info(f"Saved {len(job_data)} job listings to CSV.")
