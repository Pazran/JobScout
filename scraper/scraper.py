import requests
from bs4 import BeautifulSoup
import json
import time
import logging
from urllib.parse import urljoin
from collections import OrderedDict
from hashlib import sha256
from config.config import USER_AGENT, BASE_URL, CHECK_ROBOTS
from scraper.robots import is_allowed_by_robots

logger = logging.getLogger(__name__)

def generate_hashed_id(job_info):
    """Generate a hashed unique ID for a job using its key details."""
    raw_id = f"{job_info['jobTitle']}|{job_info['jobCompany']}|{job_info['jobLocation']}"
    hashed_id = sha256(raw_id.encode('utf-8')).hexdigest()
    return hashed_id

def fetch_data(url, check_robots=None):
    """Scrape the page and return the list of job descriptions and related information."""
    headers = {'User-Agent': USER_AGENT}
    logger.debug("Using User-Agent: %s", USER_AGENT)

    # If check_robots is None, use the global configuration (CHECK_ROBOTS)
    if check_robots is None:
        check_robots = CHECK_ROBOTS

    # Check robots.txt if enabled
    if check_robots and not is_allowed_by_robots(url, USER_AGENT, BASE_URL):
        logger.warning("Scraping disallowed by robots.txt for URL: %s", url)
        return []

    retries = 3
    for attempt in range(retries):
        try:
            logger.info("Fetching data from URL: %s", url)
            response = requests.get(url=url, headers=headers, timeout=10)

            if response.status_code == 200:
                logger.info("Successfully fetched the page content.")
                soup = BeautifulSoup(response.text, "html.parser")
                job_listings = soup.select("[data-automation=normalJob]")
                job_data = []

                for job in job_listings:
                    job = job.parent
                    job_info = OrderedDict()

                    try:
                        job_title_element = job.find('a', {'data-automation': 'jobTitle'})
                        sol_meta = json.loads(job["data-search-sol-meta"])
                        token = sol_meta["searchRequestToken"]

                        job_href = job_title_element['href'] if job_title_element and job_title_element.has_attr('href') else None
                        job_href_with_token = "#".join([str(job_href), str(token)])

                        job_info['jobTitle'] = job_title_element.get_text(strip=True) if job_title_element else None
                        job_info['jobCompany'] = job.find('a', {'data-automation': 'jobCompany'}).get_text(strip=True) if job.find('a', {'data-automation': 'jobCompany'}) else None
                        job_info['jobLocation'] = ", ".join([loc.get_text(strip=True) for loc in job.find_all('a', {'data-automation': 'jobLocation'})]) if job.find_all('a', {'data-automation': 'jobLocation'}) else None
                        job_info['jobSalary'] = (job.find('span', {'data-automation': 'jobSalary'}).get_text(strip=True)).replace("\\xa", "") if job.find('span', {'data-automation': 'jobSalary'}) else None
                        job_info['jobCategory'] = (job.find('a', {'data-automation': 'jobClassification'}).get_text(strip=True)).replace("(", "").replace(")", "") if job.find('a', {'data-automation': 'jobClassification'}) else None
                        job_info['jobSubCategory'] = job.find('a', {'data-automation': 'jobSubClassification'}).get_text(strip=True) if job.find('a', {'data-automation': 'jobSubClassification'}) else None
                        job_info['jobListingDate'] = job.find('span', {'data-automation': 'jobListingDate'}).get_text(strip=True) if job.find('span', {'data-automation': 'jobListingDate'}) else None
                        job_info['uniqueId'] = generate_hashed_id(job_info)  # Generate hashed uniqueId
                        job_info['jobURL'] = urljoin(BASE_URL, job_href_with_token) if job_href else None

                        if job_info['jobTitle'] is not None:
                            job_data.append(job_info)

                    except json.JSONDecodeError as e:
                        logger.error("Error decoding JSON data for job: %s", e)
                        continue
                    except Exception as e:
                        logger.error("Error while parsing job data: %s", e)
                        continue

                if job_data:
                    logger.info(f"Found {len(job_data)} job listings.")
                    return job_data
                else:
                    logger.warning("No job listings found on the page.")
                    return []

            else:
                logger.error("Failed to retrieve data, status code: %s", response.status_code)
                time.sleep(5)

        except requests.exceptions.RequestException as e:
            logger.error("Error during request: %s", e)
            time.sleep(5)
        except Exception as e:
            logger.error("Error while parsing the page: %s", e)
            break

    logger.error("Failed to fetch data after multiple attempts.")
    return []
