from bs4 import BeautifulSoup
import urllib3



def preprocess_html(html):
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text()
    return text
def read_html(url):
    http = urllib3.PoolManager()
    html_doc = http.request('GET', url)
    html_data = preprocess_html(html_doc)
    return html_data