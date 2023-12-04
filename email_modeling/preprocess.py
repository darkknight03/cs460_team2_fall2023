import nltk
import string
from sentence_transformers import SentenceTransformer, util
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
import re

from urllib.parse import urlparse
import dns.resolver, dns.rdatatype
from functools import cache

@cache
def get_hostname_records(hostname):
    ans = ''

    for record in ['A', 'AAAA', 'NS', 'MX']:
        try:
            res = dns.resolver.resolve(hostname, record)

            ans += f'{record}Records:{len(res)},{res.ttl} '
        except Exception:
            pass

    return ans

def get_url_domain(url):
    try:
        return urlparse(url).netloc
    except Exception:
        print("bad url:", url)
        return None

# Download NLTK resources if not already downloaded
nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)

# Load the "all-MiniLM-L12-v2" SBERT model
sbert_model = SentenceTransformer('all-MiniLM-L12-v2')

# Preprocess text data with SBERT embeddings
def preprocess(raw_text, model=sbert_model):
    if isinstance(raw_text, str):
        # Convert text to lowercase
        text = raw_text.lower()

        # Remove punctuation
        text = ''.join([char for char in text if char not in string.punctuation])

        # Tokenize the text
        tokens = nltk.word_tokenize(text)

        # Remove stopwords
        stop_words = set(stopwords.words('english'))
        tokens = [word for word in tokens if word not in stop_words]

        # Apply stemming using Snowball Stemmer (you can choose a different stemmer if preferred)
        stemmer = SnowballStemmer("english")
        tokens = [stemmer.stem(word) for word in tokens]

        # Rejoin tokens into a cleaned text
        cleaned_text = ' '.join(tokens)

        # Linguistic Analysis
        # Check for urgency keywords
        urgency_keywords = ['urgent', 'important', 'immediate', 'action', 'emergency', 'rush', 'quick action', 'respond now', 'instant', 'critical', 'time-sensitive', 'important notice']
        urgency_score = sum(cleaned_text.count(keyword) for keyword in urgency_keywords)

        # Check for persuasive language
        persuasive_keywords = ['free', 'guarantee', 'win', 'limited time', 'exclusive', 'offer', 'exclusive offer', 'guaranteed', 'prize', 'congratulations', 'amazing', 'once-in-a-lifetime', 'limited spots', 'act now']
        persuasive_score = sum(cleaned_text.count(keyword) for keyword in persuasive_keywords)

        # Check for impersonation techniques (e.g., spoofed sender names)
        impersonation_keywords = ['paypal', 'bank', 'irs', 'microsoft', 'apple', 'security verification', 'account suspension', 'account verification', 'account update', 'verify your identity', 'verify your account', 'suspicious activity', 'login attempt']
        impersonation_score = sum(cleaned_text.count(keyword) for keyword in impersonation_keywords)

        # Count the number of URLs
        urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', raw_text)
        num_urls = len(urls)

        # Calculate SBERT embeddings using the "all-MiniLM-L12-v2" model
        sbert_embeddings = model.encode([cleaned_text])

        # Convert SBERT embeddings to a string
        sbert_embeddings_str = ' '.join(map(str, sbert_embeddings[0]))

        # Add scores, URL count, and SBERT embeddings as features
        cleaned_text += f' UrgencyScore:{urgency_score} PersuasiveScore:{persuasive_score} ImpersonationScore:{impersonation_score} NumURLs:{num_urls} SBERT:{sbert_embeddings_str}'

        if len(urls) > 0:
            unique_hostnames = set(filter(lambda x: x is not None, map(get_url_domain, urls)))
            hostname_records = list(map(get_hostname_records, unique_hostnames))
            cleaned_text += ' ' + ''.join(hostname_records)

        return cleaned_text
    else:
        return ''
