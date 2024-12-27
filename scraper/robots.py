from urllib.parse import urljoin
from urllib.robotparser import RobotFileParser
import logging

logger = logging.getLogger(__name__)

def is_allowed_by_robots(url, user_agent, base_url):
    """Check if the URL is allowed based on robots.txt rules."""
    robot_parser = RobotFileParser()
    robots_url = urljoin(base_url, '/robots.txt')
    robot_parser.set_url(robots_url)
    robot_parser.read()
    allowed = robot_parser.can_fetch(user_agent, url)
    logger.debug("Checking robots.txt for URL: %s - Allowed: %s", url, allowed)
    return allowed
