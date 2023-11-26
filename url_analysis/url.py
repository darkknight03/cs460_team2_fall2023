import re
import whois
from datetime import datetime
import requests

# Define heuristics and their weights
# ref: https://drive.google.com/file/d/1gGAMknkZAiK8m01vtpQJebwuTdoxAMVP/view?usp=sharing, pp.26
heuristics = {
    'Domain Age': 8,
    'URL Length': 4,
    'Contains IP Address': 1,
    'SSL Certificate': 2
}

# Sample URL for analysis
url = "https://example-phishing-url.com/login.php"

# Define functions to calculate criteria values
def domain_age(url):
    try:
        # Extract the domain from the URL
        domain = url.split("//")[-1].split("/")[0]

        # Perform a WHOIS lookup to get domain information
        domain_info = whois.whois(domain)

        # Extract the creation date from the WHOIS data
        creation_date = domain_info.creation_date

        if isinstance(creation_date, list):
            creation_date = creation_date[0]

        # Calculate domain age
        if creation_date:
            today = datetime.now()
            age = (today - creation_date).days
            # if age of domain < 6 months
            if ((age/30) < 6):
              age = 1
            else:
              age = 0
            return age
    
    except Exception as e:
        print("dang")
        return None

# Get the domain age
domain_age = domain_age(url)

#if domain_age is not None:
#    print(f"The domain age of '{url}' is {domain_age} days.")
#else:
#    print(f"Unable to retrieve domain age for '{url}'.")
#


def get_url_length(url):
    if len(url) < 54:
        length = 0
    else:
        length = 1
    return length

def contains_ip_address(url):
    return int(bool(re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', url)))

def has_ssl_certificate(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            if response.url.startswith("https://"):
                return 1 # 1 for has ssl certificate
            else:
                return 0 # 0 for does not have ssl certificate
        else:
            print(f"HTTP request failed with status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
    

def keyword_match(url):
    return int("login" in url)  # 1 if keyword exists, 0 if not



# Calculate criteria values
criteria = {
    'Domain Age': get_domain_age(url),
    'URL Length': get_url_length(url),
    'Contains IP Address': contains_ip_address(url),
    'SSL Certificate': has_ssl_certificate(url)
    #'Keyword Match': keyword_match(url)
}

# Calculate the phishing score
phishing_score = sum(heuristics[heuristic] * criteria[heuristic] for heuristic in heuristics)

# Define a threshold (adjust as needed)
threshold = 8

# Determine if the URL is potentially phishing
is_phishing = phishing_score < threshold

# Output the result
if is_phishing:
    print(f"The URL '{url}' is classified as potentially phishing.")
else:
    print(f"The URL '{url}' is likely not phishing.")

