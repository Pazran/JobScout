import sqlite3
from config.config import DATABASE_FILE
import logging

logger = logging.getLogger(__name__)

def connect_db():
    """Establish a connection to the SQLite database."""
    return sqlite3.connect(DATABASE_FILE)

def create_table():
    """Create the jobs table if it does not exist."""
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                uniqueId TEXT NOT NULL UNIQUE,
                jobTitle TEXT,
                jobCompany TEXT,
                jobLocation TEXT,
                jobSalary TEXT,
                jobCategory TEXT,
                jobSubCategory TEXT,
                jobListingDate TEXT,
                jobURL TEXT
            )
        ''')
        conn.commit()
        logger.info("Jobs table created or already exists.")
    except sqlite3.Error as e:
        logger.error("Error creating jobs table: %s", e)
    finally:
        conn.close()

def insert_job(job):
    """Insert a job into the database if it does not already exist."""
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO jobs (
                uniqueId, jobTitle, jobCompany, jobLocation, 
                jobSalary, jobCategory, jobSubCategory, 
                jobListingDate, jobURL
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            job['uniqueId'],
            job.get('jobTitle'),
            job.get('jobCompany'),
            job.get('jobLocation'),
            job.get('jobSalary'),
            job.get('jobCategory'),
            job.get('jobSubCategory'),
            job.get('jobListingDate'),
            job.get('jobURL')
        ))
        conn.commit()
        logger.info("Job inserted into the database: %s", job['jobTitle'])
    except sqlite3.IntegrityError:
        logger.warning("Job already exists in the database: %s", job['uniqueId'])
    except sqlite3.Error as e:
        logger.error("Error inserting job into the database: %s", e)
    finally:
        conn.close()

def job_exists(unique_id):
    """Check if a job with the given unique ID exists in the database."""
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('SELECT 1 FROM jobs WHERE uniqueId = ?', (unique_id,))
        exists = cursor.fetchone() is not None
        return exists
    except sqlite3.Error as e:
        logger.error("Error checking if job exists in the database: %s", e)
        return False
    finally:
        conn.close()
    
def count_jobs():
    """Return the total count of jobs in the database."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM jobs')
    count = cursor.fetchone()[0]
    conn.close()
    return count
