import requests
from bs4 import BeautifulSoup

urls = {
    'Hacker News' : 'https://brutalist.report/source/hn?hours=6', # Hacker News
    'The Verge' : 'https://brutalist.report/source/verge?hours=6', # The Verge
    'Engadget' : 'https://brutalist.report/source/engadget?hours=6', # Engadget
    'TechCrunch' : 'https://brutalist.report/source/techcrunch?hours=6', # TechCrunch
    'TechRadar' : 'https://brutalist.report/source/techradar?hours=6' # TechRadar
}

def fetch_headlines():

    headlines = []

    for name, url in urls.items():
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')

        li_tags = soup.find_all('li')

        for tag in li_tags:
            try:
                entry = {
                    'headline' : tag.find('a').get_text(strip=True),
                    'source' : name
                }
                headlines.append(entry)
            except AttributeError as e:
                pass

    return headlines

print(fetch_headlines())