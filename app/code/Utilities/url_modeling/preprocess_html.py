from bs4 import BeautifulSoup
import requests, re


def preprocess_html(html):
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text()
    text = re.sub('[\n]+', '\n', text)
    return text

def read_html(url):
    response = requests.get(url)

    html_content = response.text
    html_data = preprocess_html(html_content)
    return html_data
