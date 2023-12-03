from bs4 import BeautifulSoup
import requests, re

def preprocess_html(html):
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text()
    text = re.sub('[\n]+', '\n', text)
    return text

def read_html(url):

    if url[:7] != 'http://' and url[:8] != 'https://':
        try: # try default https
            response = requests.get('https://' + url)

            html_content = response.text
            html_data = preprocess_html(html_content)
            return html_data
        except:
            pass

        # try http
        response = requests.get('http://' + url)

        html_content = response.text
        html_data = preprocess_html(html_content)
        return html_data

    response = requests.get(url)

    html_content = response.text
    html_data = preprocess_html(html_content)
    return html_data
