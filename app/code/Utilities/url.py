import re
import whois
from datetime import datetime
import requests
import argparse
import ssl
import certifi
import socket



def get_domain(url):
  domain = url.split("//")[-1].split("/")[0]
  if re.match(r"^www.",domain):
    domain = domain.replace("www.","")
  #print(domain)
  return domain

# url feature:
def url_length(url):
  if len(url) < 54:
      length = 0
  else:
      length = 1
  return length


def contains_ip_address(url):
  return int(bool(re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', url)))

def _ssl_certificate(url):
  domain = get_domain(url)

  flag = 0
  try:
    response = requests.get(url, timeout=1)
    if response.status_code == 200:
      if response.url.startswith("https://"):
        flag = 1
  except:
    return 0

  if flag == 0:
    return 0

  context = ssl.create_default_context(cafile=certifi.where())

  try:
    with socket.create_connection((domain, 443)) as sock:
      with context.wrap_socket(sock, server_hostname=domain) as ssock:
        cert = ssock.getpeercert()

        self_signed = 0
        expired = 0
        # Check if the certificate is self-signed
        if cert['issuer'] == cert['subject']:
          self_signed = 1

        # Check if the certificate has expired
        not_after_str = cert['notAfter']
        not_after = ssl.cert_time_to_seconds(not_after_str)
        if not_after < ssl.time.time():
          expired = 1

        if expired and self_signed:
          return 1 #phishing
        else:
          return 0

  except ssl.CertificateError:
    # failed to verify its own public key
    return 1
  #except ssl.SSLError as e:
      # suspicious, but skip for now
  except:
    return 1


def keyword_match(url):
    return int("login" in url)  # 1 if keyword exists, 0 if not

def special_char(url):
    phishing = 0
    if "_" in url:
        phishing = 1
    if "," in url:
        phishing = 1
    if ";" in url:
        phishing = 1
    return phishing



#domain featur

def domain_exp_date(url):
  try:
    domain = get_domain(url)
    info = whois.whois(domain)
    expiration_date = info.expiration_date

    if isinstance(expiration_date, list):
      expiration_date = min(expiration_date)

    if expiration_date:
      days_until_expiration = (expiration_date - datetime.now()).days
      if days_until_expiration <= 180:
        return 1
      else:
        return 0
    else:
      return 0
  except:
    return 0

def domain_creation_date(url):
  try:
    domain = get_domain(url)
    info = whois.whois(domain)
    creation_date = info.creation_date

    if isinstance(creation_date, list):
      creation_date = min(creation_date)

    if creation_date:
      days_created = (datetime.now()-creation_date).days
      if days_created <= 365:
        return 1
      else:
        return 0
    else:
      return 0
  except:
    return 0

def domain_age(url):
    try:
        domain = get_domain(url)

        # Perform a WHOIS lookup to get domain information
        domain_info = whois.whois(domain)

        # Extract the creation/expiration date from the WHOIS data
        creation_date = domain_info.creation_date
        expiration_date = domain_info.expiration_date

        if isinstance(creation_date, list):
            creation_date = creation_date[0]

        # Calculate domain age
        if creation_date:
            age = (expiration_date - creation_date).days
            # if age of domain < 6 months
            if_phishing = 1
            if ((age/30) < 6):
              if_phishing = 1
            else:
              if_phishing = 0
            return if_phishing
        else:
            return 0
    except:
        return 0

def contains_at(url):
    domain = get_domain(url)
    return int("@" in domain) # return 1 if @ contains (phishing), 0 otherwise

def dots_count(url):
    domain = get_domain(url)
    #The number of dots in the domain part of the URL represents the number of subdomains.
    dot_count = domain.count('.')
    if dot_count <= 3:
        return 0
    else:
        return 1

def slashes_count(url):
    domain = get_domain(url)
    slash_count = domain.count('/')
    if slash_count <= 3:
        return 0
    else:
        return 1


#html features:
def count_redirect_urls(url):
# The more redirect URLs are in a webpage the more malicious the URL is.
    try:
        response = requests.get(url, allow_redirects=True, timeout=2)

        redirect_count = len(response.history)

        if redirect_count <= 1:
            return 0
        else:
            return 1

    except:
        return 0


def right_click_disable(url):
    try:
        response = requests.get(url, allow_redirects=True, timeout=2)
        if re.findall(r"event.button ?== ?2", response.text):
            return 0
        else:
            return 1
    except:
        return 0


def status_bar_change(url):
    try:
        response = requests.get(url, timeout=2)
        if 'window.status' in response.text:
            return 1
        else:
            return 0
    except:
        return 0


# Sample URL for analysis
# url = "https://drive.google.com/file/d/1gGAMknkZAiK8m01vtpQJebwuTdoxAMVP/view?usp=sharing"

#read url to check
def url_analysis(url):
  # parser = argparse.ArgumentParser(description='Process a URL.')
  # parser.add_argument('-url', '--url', type=str, required=True, help='URL to process')
  # args = parser.parse_args()
  # url = args.url


  # Define heuristics and their weights
  # ref: https://drive.google.com/file/d/1gGAMknkZAiK8m01vtpQJebwuTdoxAMVP/view?usp=sharing, pp.26
  heuristics = {
      #'URL Length': 0,
      #'Contains IP Address': 0.09,
      'SSL Certificate': 3,
      #'Keyword Match': 0.1,
      'Special Char': 1,
      'Domain Age': 4,
      'Contains At': 1,
      'Dots Count': 1,
    # 'Slashes Count': 0,
      #'Redirect URLs': 0,
      'Right Click Disable': 1,
      #'Status Bar Change': 0,
      'Exp Date': 2,
      'Creation_Date': 5
  }

  # Calculate criteria values
  criteria = {
  #  'URL Length': url_length(url),
    #'Contains IP Address': contains_ip_address(url),
    'SSL Certificate': _ssl_certificate(url),
    #'Keyword Match': keyword_match(url),
    'Special Char': special_char(url),
    'Domain Age': domain_age(url),
    'Contains At': contains_at(url),
    'Dots Count': dots_count(url),
  #   'Slashes Count': slashes_count(url),
    #'Redirect URLs': count_redirect_urls(url),
    'Right Click Disable': right_click_disable(url),
  #  'Status Bar Change': status_bar_change(url)
    'Exp Date': domain_exp_date(url),
    'Creation_Date': domain_creation_date(url)
    }


  # Calculate the phishing score
  phishing_score = sum(heuristics[heuristic] * criteria[heuristic] for heuristic in heuristics)

  # a threshold (adjust as needed)
  threshold = 2.9

  # Determine if the URL is potentially phishing
  is_phishing = phishing_score > threshold

  # Output the result
  if is_phishing:
      # print(f"The URL '{url}' is classified as potentially phishing.")
      return True
  else:
      # print(f"The URL '{url}' is likely not phishing.")
      return False

