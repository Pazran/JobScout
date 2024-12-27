
# JobScout Bot

JobScout Bot is a web scraper that fetches job listings from a website (currently only for Jobstreet), stores them in a SQLite database, and allows periodic and continuous scraping for new job listings. The scraper checks for new jobs, inserts them into the database, and handles job listings in a structured format. It is designed as a modular base that can be easily adapted for other types of content or products. It allows for easy extension to send scraped data to various platforms like Telegram, Discord, or other APIs. This makes it a powerful tool not only for scraping job listings but also for extracting and sharing content related to different products or services. The sky is the limit my friends.

## Demo Video
Watch the demo video for how to use JobScout:

[![JobScout Demo](https://github.com/Pazran/JobScout-Bot/blob/6c291c810cf0fd7dece9d7539f2bea2f6cbe6bca/demo/demo.gif)](https://github.com/Pazran/JobScout-Bot/blob/6c291c810cf0fd7dece9d7539f2bea2f6cbe6bca/demo/demo.gif)

## Features
- Scrapes job listings using BeautifulSoup and requests.
- Stores job data in an SQLite database.
- Supports periodic scraping using threading.
- Provides logging and error handling.
- Easily configurable for different job listing websites.

*NOTES: Currently only support scraping from JobStreet*

## Files
1. **job_scraper_main.py** - Main script to run the job scraper and trigger periodic scraping.
2. **scraper/scraper.py** - Contains the logic for scraping job data from a website.
3. **database/database.py** - Handles database connections, job insertions, and checks for existing jobs.
4. **config/config.py** - Contains configuration settings like URLs, headers, and other parameters.
5. **persistence/persistence.py** - Deals with saving job listings to a CSV file for further use.
6. **worker/worker.py** - Implements the periodic job scraper using threading.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Pazran/job-scraper.git
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure the `URL_TO_SCRAP=` in `config/config.py`. Run the main script to start scraping:
   ```bash
   python job_scraper_main.py
   ```

## Example of Job Scraping
Here is an example of how the scraper works:

```python
from scraper.scraper import fetch_data

# Fetching job data from the given URL
url = "http://jobstreet.com/<JOB TITLE HERE>-jobs"
job_listings = fetch_data(url)

# Printing out the first job listing
print(job_listings[0])
```

### Example Output:
```
{
    'uniqueId': 'job-123',
    'jobTitle': 'Software Developer',
    'jobCompany': 'Company XYZ',
    'jobLocation': 'New York',
    'jobSalary': '$100,000',
    'jobCategory': 'Engineering',
    'jobSubCategory': 'Development',
    'jobListingDate': '2024-01-01',
    'jobURL': 'http://example.com/job-123'
}
```

## Contributing
If you'd like to contribute to this project, feel free to fork it and submit a pull request with improvements, bug fixes, or new features.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
